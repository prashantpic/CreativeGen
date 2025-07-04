/**
 * @file collaborationSession.ts
 * @description Defines the CollaborationSession aggregate root.
 */

import * as Y from 'yjs';
import { Participant } from './participant';

/**
 * Aggregate root representing the shared state of a document's collaboration session.
 * It encapsulates the CRDT document state (Y.Doc) and manages the list of active participants.
 */
export class CollaborationSession {
    /** The core Yjs document instance holding the shared state. */
    private doc: Y.Doc;
    /** A map of connected participants, keyed by userId. */
    private participants: Map<string, Participant>;

    /**
     * Creates an instance of a CollaborationSession.
     * @param id The unique identifier for the session, which is the documentId.
     * @param snapshot An optional binary snapshot to initialize the document state.
     */
    constructor(public readonly id: string, snapshot?: Uint8Array) {
        this.participants = new Map<string, Participant>();
        this.doc = new Y.Doc();

        if (snapshot) {
            Y.applyUpdate(this.doc, snapshot);
        }
    }

    /**
     * Adds a participant to the session.
     * @param participant The participant to add.
     */
    addParticipant(participant: Participant): void {
        this.participants.set(participant.userId, participant);
    }

    /**
     * Removes a participant from the session by their user ID.
     * @param userId The ID of the user to remove.
     */
    removeParticipant(userId: string): void {
        this.participants.delete(userId);
    }

    /**
     * Retrieves a participant by their user ID.
     * @param userId The ID of the user to retrieve.
     * @returns The participant if found, otherwise undefined.
     */
    getParticipant(userId: string): Participant | undefined {
        return this.participants.get(userId);
    }

    /**
     * Gets the current number of active participants in the session.
     * @returns The number of participants.
     */
    getParticipantCount(): number {
        return this.participants.size;
    }
    
    /**
     * Applies a CRDT update to the internal Y.Doc.
     * @param update The CRDT update payload from a client.
     * @param transactionOrigin The origin of the transaction, used to prevent echoing updates to the sender.
     */
    applyUpdate(update: Uint8Array, transactionOrigin: any): void {
        Y.applyUpdate(this.doc, update, transactionOrigin);
    }

    /**
     * Returns the state vector of the document. This is used by clients to
     * determine what updates they are missing.
     * @returns The encoded state vector as a Uint8Array.
     */
    getStateVector(): Uint8Array {
        return Y.encodeStateVector(this.doc);
    }

    /**
     * Creates a differential update for a client based on their provided state vector.
     * This allows clients to sync up by only receiving the changes they don't have.
     * @param stateVector The client's current state vector.
     * @returns The encoded differential update as a Uint8Array.
     */
    getDiff(stateVector: Uint8Array): Uint8Array {
        return Y.encodeStateAsUpdate(this.doc, stateVector);
    }

    /**
     * Creates a full snapshot of the document's current state.
     * This is used to initialize new clients or for persistence.
     * @returns The encoded full document state as a Uint8Array.
     */
    getSnapshot(): Uint8Array {
        return Y.encodeStateAsUpdate(this.doc);
    }
}