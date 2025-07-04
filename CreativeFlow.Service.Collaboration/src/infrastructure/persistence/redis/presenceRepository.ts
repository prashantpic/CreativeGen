/**
 * @file presenceRepository.ts
 * @description Redis implementation of the IPresenceRepository interface.
 */

import { Redis } from 'ioredis';
import { IPresenceRepository } from '../../../domain/repositories/iPresenceRepository';
import { Participant } from '../../../domain/participant';

/**
 * Provides a concrete implementation for managing real-time user presence
 * using Redis for high performance and automatic expiration of stale data.
 */
export class RedisPresenceRepository implements IPresenceRepository {
    /**
     * @param redisClient The ioredis client instance.
     * @param presenceTtlSeconds The time-to-live for socket tracking keys.
     */
    constructor(
        private readonly redisClient: Redis,
        private readonly presenceTtlSeconds: number
    ) {}

    private getPresenceKey(documentId: string): string {
        return `presence:${documentId}`;
    }

    private getSocketKey(socketId: string): string {
        return `socket:${socketId}`;
    }

    /**
     * Marks a user as active in a document's session using a Redis Hash.
     * @param documentId The ID of the document.
     * @param participant The participant to mark as present.
     */
    public async setUserPresence(documentId: string, participant: Participant): Promise<void> {
        const key = this.getPresenceKey(documentId);
        const value = JSON.stringify(participant);
        await this.redisClient.hset(key, participant.userId, value);
    }

    /**
     * Removes a user's presence from a document's session hash.
     * @param documentId The ID of the document.
     * @param userId The ID of the user to remove.
     */
    public async removeUserPresence(documentId: string, userId: string): Promise<void> {
        const key = this.getPresenceKey(documentId);
        await this.redisClient.hdel(key, userId);
    }

    /**
     * Gets all active users in a document by fetching all fields from the hash.
     * @param documentId The ID of the document.
     * @returns A promise resolving to an array of Participants.
     */
    public async getPresentUsers(documentId: string): Promise<Participant[]> {
        const key = this.getPresenceKey(documentId);
        const results = await this.redisClient.hvals(key);
        return results.map(p => JSON.parse(p) as Participant);
    }

    /**
     * Associates a socket ID with a user and document for quick lookup on disconnect.
     * A TTL is set to automatically clean up stale socket tracking entries.
     * @param socketId The unique socket connection ID.
     * @param userId The user's ID.
     * @param documentId The document ID.
     */
    public async trackSocket(socketId: string, userId: string, documentId: string): Promise<void> {
        const key = this.getSocketKey(socketId);
        const value = `${userId}:${documentId}`;
        await this.redisClient.set(key, value, 'EX', this.presenceTtlSeconds);
    }

    /**
     * Removes a socket tracking entry and returns the associated user and document info.
     * This is an atomic operation to prevent race conditions.
     * @param socketId The socket ID to untrack.
     * @returns A promise resolving to user/document info, or null if not found.
     */
    public async untrackSocket(socketId: string): Promise<{ userId: string; documentId: string } | null> {
        const key = this.getSocketKey(socketId);
        // Use a MULTI/EXEC transaction to get and delete atomically
        const result = await this.redisClient.multi().get(key).del(key).exec();
        
        if (!result || !result[0] || result[0][1] === null) {
            return null;
        }

        const value = result[0][1] as string;
        const [userId, documentId] = value.split(':');
        
        if (!userId || !documentId) {
            return null;
        }

        return { userId, documentId };
    }
}