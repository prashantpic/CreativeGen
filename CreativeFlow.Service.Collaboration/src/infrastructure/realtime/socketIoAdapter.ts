/**
 * @file socketIoAdapter.ts
 * @description Bridge between the Socket.IO server and the application layer.
 */

import { Server as HttpServer } from 'http';
import { Server as SocketIoServer, Socket } from 'socket.io';
import { SessionManagerService } from '../../application/sessionManagerService';
import { IPresenceRepository } from '../../domain/repositories/iPresenceRepository';
import { Participant } from '../../domain/participant';
import { AuthService } from '../../interfaces/http/authService';

// Extend the Socket type to include our custom userId property
interface AuthenticatedSocket extends Socket {
    userId?: string;
}

/**
 * Encapsulates all Socket.IO-specific logic, acting as the primary bridge
 * between the network and the application layer. It handles connection lifecycle,
 * event routing, and authentication.
 */
export class SocketIoAdapter {
    private io: SocketIoServer;

    /**
     * Initializes the Socket.IO server, attaches it to the HTTP server,
     * and configures middleware and event handlers.
     * @param httpServer The main HTTP server instance.
     * @param authService The service for JWT validation.
     * @param sessionManager The service for managing collaboration sessions.
     * @param presenceRepo The repository for managing user presence.
     */
    public initialize(
        httpServer: HttpServer,
        authService: AuthService,
        sessionManager: SessionManagerService,
        presenceRepo: IPresenceRepository
    ): void {
        this.io = new SocketIoServer(httpServer, {
            cors: {
                origin: "*", // Configure for your specific origins in production
                methods: ["GET", "POST"]
            }
        });

        // Authentication middleware
        this.io.use(async (socket: AuthenticatedSocket, next) => {
            const token = socket.handshake.auth.token;
            if (!token) {
                return next(new Error('Authentication error: No token provided.'));
            }
            try {
                const decoded = await authService.verifyToken(token);
                socket.userId = decoded.userId;
                next();
            } catch (error) {
                console.error('Socket authentication failed:', error.message);
                return next(new Error('Authentication error: Invalid token.'));
            }
        });

        // Main connection handler
        this.io.on('connection', (socket: AuthenticatedSocket) => {
            console.log(`User connected: ${socket.userId} with socket ID: ${socket.id}`);
            this.setupEventHandlers(socket, sessionManager, presenceRepo);
        });
    }

    private setupEventHandlers(
        socket: AuthenticatedSocket,
        sessionManager: SessionManagerService,
        presenceRepo: IPresenceRepository
    ): void {
        const userId = socket.userId!;

        socket.on('join-session', async ({ documentId }: { documentId: string }) => {
            try {
                const session = await sessionManager.getSession(documentId);
                const participant = new Participant(userId, socket.id);

                session.addParticipant(participant);
                await presenceRepo.setUserPresence(documentId, participant);
                await presenceRepo.trackSocket(socket.id, userId, documentId);

                socket.join(documentId);

                socket.emit('session-joined', {
                    documentState: session.getSnapshot(),
                    participants: await presenceRepo.getPresentUsers(documentId),
                });

                socket.to(documentId).emit('user-joined', participant);
            } catch (error) {
                console.error(`Error on join-session for user ${userId} in doc ${documentId}:`, error);
                socket.emit('session-error', { message: 'Failed to join session.', code: 'JOIN_FAILED' });
            }
        });

        socket.on('document-update', async ({ documentId, update }: { documentId: string, update: Uint8Array }) => {
            try {
                await sessionManager.applyUpdate(documentId, update, socket.id);
                socket.to(documentId).emit('document-update', update);
            } catch (error) {
                 console.error(`Error on document-update for user ${userId} in doc ${documentId}:`, error);
            }
        });
        
        socket.on('sync-request', async ({ documentId, stateVector }: { documentId: string, stateVector: Uint8Array }) => {
            try {
                const session = await sessionManager.getSession(documentId);
                const diff = session.getDiff(stateVector);
                socket.emit('sync-reply', diff);
            } catch (error) {
                 console.error(`Error on sync-request for user ${userId} in doc ${documentId}:`, error);
            }
        });

        socket.on('presence-update', ({ documentId, presenceState }: { documentId: string, presenceState: Record<string, any> }) => {
            socket.to(documentId).emit('presence-update', { userId, presenceState });
        });

        socket.on('disconnect', async () => {
            console.log(`User disconnected: ${userId} with socket ID: ${socket.id}`);
            const socketInfo = await presenceRepo.untrackSocket(socket.id);
            if (socketInfo) {
                const { userId: disconnectedUserId, documentId } = socketInfo;
                await presenceRepo.removeUserPresence(documentId, disconnectedUserId);
                
                const session = await sessionManager.getSession(documentId);
                session.removeParticipant(disconnectedUserId);

                this.io.to(documentId).emit('user-left', { userId: disconnectedUserId });
                
                await sessionManager.closeSessionIfEmpty(documentId);
            }
        });
    }
}