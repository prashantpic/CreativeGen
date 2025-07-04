/**
 * @file collaborationSessionRepository.ts
 * @description PostgreSQL implementation of the ICollaborationSessionRepository interface.
 */

import { Pool, PoolClient } from 'pg';
import { ICollaborationSessionRepository } from '../../../domain/repositories/iCollaborationSessionRepository';

/**
 * Provides a concrete implementation for persisting and retrieving collaboration session
 * snapshots using a PostgreSQL database.
 */
export class PostgresCollaborationSessionRepository implements ICollaborationSessionRepository {
    /**
     * @param dbPool The Node-Postgres connection pool.
     */
    constructor(private readonly dbPool: Pool) {}

    /**
     * Retrieves the latest document snapshot from the database.
     * @param documentId The unique identifier of the document.
     * @returns A promise that resolves to the snapshot as a Uint8Array, or null if not found.
     */
    public async findSnapshotById(documentId: string): Promise<Uint8Array | null> {
        const query = 'SELECT document_state FROM collaboration_documents WHERE id = $1';
        try {
            const result = await this.dbPool.query(query, [documentId]);
            if (result.rows.length > 0) {
                // pg returns Buffer for bytea, which is a subclass of Uint8Array
                return result.rows[0].document_state as Uint8Array;
            }
            return null;
        } catch (error) {
            console.error(`Error finding snapshot for document ${documentId}:`, error);
            throw error;
        }
    }

    /**
     * Saves or updates the document snapshot in the database using an UPSERT operation.
     * @param documentId The unique identifier of the document.
     * @param snapshot The binary snapshot of the document state.
     * @returns A promise that resolves when the operation is complete.
     */
    public async save(documentId: string, snapshot: Uint8Array): Promise<void> {
        const query = `
            INSERT INTO collaboration_documents (id, document_state, updated_at)
            VALUES ($1, $2, NOW())
            ON CONFLICT (id) DO UPDATE 
            SET document_state = EXCLUDED.document_state, 
                updated_at = NOW();
        `;
        try {
            await this.dbPool.query(query, [documentId, snapshot]);
        } catch (error) {
            console.error(`Error saving snapshot for document ${documentId}:`, error);
            throw error;
        }
    }

    /**
     * Deletes a document session and its snapshot from the database.
     * @param documentId The unique identifier of the document to delete.
     * @returns A promise that resolves when the operation is complete.
     */
    public async delete(documentId: string): Promise<void> {
        const query = 'DELETE FROM collaboration_documents WHERE id = $1';
        try {
            await this.dbPool.query(query, [documentId]);
        } catch (error) {
            console.error(`Error deleting document ${documentId}:`, error);
            throw error;
        }
    }
}