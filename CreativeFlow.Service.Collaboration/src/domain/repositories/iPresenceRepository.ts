/**
 * @file iPresenceRepository.ts
 * @description Defines the interface for presence management.
 */

import { Participant } from '../participant';

/**
 * Defines the contract (interface) for managing user presence information.
 * Presence is volatile data indicating which users are active in which documents.
 * This is typically implemented with a fast in-memory store like Redis.
 */
export interface IPresenceRepository {
    /**
     * Marks a user as active in a specific document's session.
     * @param documentId The ID of the document.
     * @param participant The participant to mark as present.
     * @returns A promise that resolves when the operation is complete.
     */
    setUserPresence(documentId: string, participant: Participant): Promise<void>;

    /**
     * Removes a user's presence from a document's session.
     * @param documentId The ID of the document.
     * @param userId The ID of the user to remove.
     * @returns A promise that resolves when the operation is complete.
     */
    removeUserPresence(documentId: string, userId: string): Promise<void>;

    /**
     * Gets all active (present) users for a given document.
     * @param documentId The ID of the document.
     * @returns A promise that resolves to an array of present Participant objects.
     */
    getPresentUsers(documentId: string): Promise<Participant[]>;

    /**
     * Associates a socket ID with a user and document for quick lookup on disconnect.
     * @param socketId The unique socket connection ID.
     * @param userId The user's ID.
     * @param documentId The document ID.
     * @returns A promise that resolves when the tracking entry is created.
     */
    trackSocket(socketId: string, userId: string, documentId: string): Promise<void>;

    /**
     * Removes a socket tracking entry and returns the associated user and document info.
     * This is typically called on socket disconnection.
     * @param socketId The socket ID to untrack.
     * @returns A promise that resolves to an object with userId and documentId, or null if not found.
     */
    untrackSocket(socketId: string): Promise<{ userId: string; documentId: string } | null>;
}