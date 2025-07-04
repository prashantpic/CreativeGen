/**
 * @file authService.ts
 * @description Mock/Stub service for handling JWT validation.
 */

import { verify, JwtPayload } from 'jsonwebtoken';

/**
 * Represents a service responsible for handling authentication, specifically
 * JWT validation. In a real system, this might be more complex, involving
 * fetching public keys, etc.
 */
export class AuthService {
    /**
     * @param jwtSecret The secret key for verifying JWT signatures.
     */
    constructor(private readonly jwtSecret: string) {
        if (!jwtSecret) {
            throw new Error("JWT_SECRET is not defined. Cannot initialize AuthService.");
        }
    }

    /**
     * Verifies a JWT and extracts the user ID.
     * @param token The JWT string to verify.
     * @returns A promise that resolves with an object containing the user ID.
     * @throws An error if the token is invalid or expired.
     */
    public verifyToken(token: string): Promise<{ userId: string }> {
        return new Promise((resolve, reject) => {
            verify(token, this.jwtSecret, (err, decoded) => {
                if (err) {
                    return reject(err);
                }
                const payload = decoded as JwtPayload;
                if (!payload || typeof payload.userId !== 'string') {
                    return reject(new Error('Invalid token payload'));
                }
                resolve({ userId: payload.userId });
            });
        });
    }
}