/**
 * @file iCollaborationSessionRepository.ts
 * @description Defines the interface for collaboration session persistence.
 */

/**
 * Defines the contract (interface) for persisting and retrieving CollaborationSession data.
 * This abstraction decouples the domain logic from specific data storage technologies like PostgreSQL.
 */
export interface ICollaborationSessionRepository {
    /**
     * Retrieves the latest document state snapshot from persistence.
     * @param documentId The unique identifier of the document.
     * @returns A promise that resolves to the snapshot as a Uint8Array, or null if not found.
     */
    findSnapshotById(documentId: string): Promise<Uint8Array | null>;

    /**
     * Saves or updates the document state snapshot in persistence.
     * @param documentId The unique identifier of the document.
     * @param snapshot The binary snapshot of the document state (Y.Doc).
     * @returns A promise that resolves when the operation is complete.
     */
    save(documentId: string, snapshot: Uint8Array): Promise<void>;

    /**
     * Deletes a document session and its snapshot from persistence.
     * @param documentId The unique identifier of the document to delete.
     * @returns A promise that resolves when the operation is complete.
     */
    delete(documentId: string): Promise<void>;
}