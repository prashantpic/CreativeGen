/**
 * @file sessionManagerService.ts
 * @description Application service to manage the lifecycle of in-memory CollaborationSession instances.
 */

import { CollaborationSession } from '../domain/collaborationSession';
import { ICollaborationSessionRepository } from '../domain/repositories/iCollaborationSessionRepository';

/**
 * Manages the lifecycle of in-memory `CollaborationSession` instances. It acts as a
 * coordinator between real-time updates and persistent storage, handling session
 * creation, caching, and debounced saving to the database.
 */
export class SessionManagerService {
    /** In-memory cache of active collaboration sessions, keyed by documentId. */
    private activeSessions: Map<string, CollaborationSession> = new Map();

    /** Timers for debouncing persistence saves, keyed by documentId. */
    private persistenceTimers: Map<string, NodeJS.Timeout> = new Map();

    /** The delay in milliseconds for debouncing persistence saves. */
    private readonly persistenceDebounceMs: number;

    /**
     * @param sessionRepository The repository for session persistence.
     */
    constructor(private readonly sessionRepository: ICollaborationSessionRepository) {
        this.persistenceDebounceMs = parseInt(process.env.PERSISTENCE_DEBOUNCE_MS || '10000', 10);
    }

    /**
     * Retrieves a session. If not in memory, it loads from the repository.
     * If not in the repository, it creates a new one. The session is cached in memory.
     * @param documentId The ID of the document.
     * @returns A promise that resolves to the CollaborationSession instance.
     */
    public async getSession(documentId: string): Promise<CollaborationSession> {
        if (this.activeSessions.has(documentId)) {
            return this.activeSessions.get(documentId)!;
        }

        const snapshot = await this.sessionRepository.findSnapshotById(documentId);
        const session = new CollaborationSession(documentId, snapshot);
        this.activeSessions.set(documentId, session);
        return session;
    }

    /**
     * Applies a document update to the session and schedules a persistence save.
     * @param documentId The ID of the document.
     * @param update The CRDT update payload.
     * @param origin The origin of the update (e.g., socket ID) to prevent echoing.
     */
    public async applyUpdate(documentId: string, update: Uint8Array, origin: any): Promise<void> {
        const session = await this.getSession(documentId);
        session.applyUpdate(update, origin);
        this.schedulePersistence(documentId);
    }

    /**
     * Manages a debounced save operation. If a timer for a documentId already exists,
     * it is reset. Otherwise, a new timer is set.
     * @param documentId The ID of the document to schedule for saving.
     */
    public schedulePersistence(documentId: string): void {
        if (this.persistenceTimers.has(documentId)) {
            clearTimeout(this.persistenceTimers.get(documentId)!);
        }

        const timer = setTimeout(() => {
            this.persistSession(documentId).catch(error => {
                console.error(`Failed to persist session ${documentId}:`, error);
            });
        }, this.persistenceDebounceMs);

        this.persistenceTimers.set(documentId, timer);
    }

    /**
     * Persists the current state of a session to the database.
     * @param documentId The ID of the document session to persist.
     */
    public async persistSession(documentId: string): Promise<void> {
        // Clear the timer associated with this persistence task
        if (this.persistenceTimers.has(documentId)) {
            clearTimeout(this.persistenceTimers.get(documentId)!);
            this.persistenceTimers.delete(documentId);
        }

        const session = this.activeSessions.get(documentId);
        if (!session) {
            console.warn(`Attempted to persist non-active session: ${documentId}`);
            return;
        }

        const snapshot = session.getSnapshot();
        await this.sessionRepository.save(documentId, snapshot);
        console.log(`Session ${documentId} persisted successfully.`);
    }

    /**
     * Checks if a session has any participants. If not, it persists the session
     * one last time and removes it from the active sessions map to free up memory.
     * @param documentId The ID of the document session to check.
     */
    public async closeSessionIfEmpty(documentId: string): Promise<void> {
        const session = this.activeSessions.get(documentId);
        if (session && session.getParticipantCount() === 0) {
            console.log(`Last participant left session ${documentId}. Closing and persisting.`);
            await this.persistSession(documentId);
            this.activeSessions.delete(documentId);
            console.log(`Session ${documentId} closed and removed from memory.`);
        }
    }
}