/**
 * @file participant.ts
 * @description Defines the Participant entity representing a user in a session.
 */

/**
 * Represents a user participating in a collaboration session.
 * Holds user-specific information relevant to the session, like their user ID,
 * current socket connection, and presence state (e.g., cursor position).
 */
export class Participant {
    /**
     * @param userId The unique ID of the user.
     * @param socketId The unique ID of their current WebSocket connection.
     * @param presenceState An object for cursor position or other presence-related metadata.
     */
    constructor(
        public readonly userId: string,
        public readonly socketId: string,
        public presenceState: Record<string, any> = {}
    ) {}
}