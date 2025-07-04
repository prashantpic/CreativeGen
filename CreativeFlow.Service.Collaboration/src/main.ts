/**
 * @file main.ts
 * @description Application entry point. Handles dependency injection and server startup.
 */

// Load environment variables from .env file
import 'dotenv/config';

import { Pool } from 'pg';
import Redis from 'ioredis';
import { createHttpServer } from './interfaces/http/server';
import { SocketIoAdapter } from './infrastructure/realtime/socketIoAdapter';
import { PostgresCollaborationSessionRepository } from './infrastructure/persistence/postgresql/collaborationSessionRepository';
import { RedisPresenceRepository } from './infrastructure/persistence/redis/presenceRepository';
import { SessionManagerService } from './application/sessionManagerService';
import { AuthService } from './interfaces/http/authService';

/**
 * Bootstraps the application.
 * This function initializes all modules, wires up dependencies (Dependency Injection),
 * and launches the server.
 */
async function bootstrap() {
    // --- 1. Validate Environment Variables ---
    const requiredEnv = [
        'POSTGRES_CONNECTION_STRING',
        'REDIS_URL',
        'JWT_SECRET',
        'PORT'
    ];
    for (const v of requiredEnv) {
        if (!process.env[v]) {
            console.error(`FATAL ERROR: Environment variable ${v} is not set.`);
            process.exit(1);
        }
    }

    try {
        // --- 2. Initialize DB and Cache Clients ---
        console.log('Connecting to PostgreSQL...');
        const pgPool = new Pool({ connectionString: process.env.POSTGRES_CONNECTION_STRING });
        // Test connection
        await pgPool.query('SELECT NOW()');
        console.log('PostgreSQL connection successful.');

        console.log('Connecting to Redis...');
        const redisClient = new Redis(process.env.REDIS_URL!);
        // Test connection
        await redisClient.ping();
        console.log('Redis connection successful.');


        // --- 3. Instantiate Infrastructure Repositories ---
        const sessionRepository = new PostgresCollaborationSessionRepository(pgPool);
        const presenceTtl = parseInt(process.env.PRESENCE_TTL_SECONDS || '60', 10);
        const presenceRepository = new RedisPresenceRepository(redisClient, presenceTtl);
        
        // --- 4. Instantiate Application and Auth Services ---
        const sessionManager = new SessionManagerService(sessionRepository);
        const authService = new AuthService(process.env.JWT_SECRET!);

        // --- 5. Instantiate and Start the Server/Adapter ---
        const httpServer = createHttpServer();
        const socketAdapter = new SocketIoAdapter();
        socketAdapter.initialize(httpServer, authService, sessionManager, presenceRepository);
        
        const PORT = process.env.PORT || 3000;
        httpServer.listen(PORT, () => {
            console.log(`🚀 CreativeFlow Collaboration Service is running on port ${PORT}`);
        });

    } catch(error) {
        console.error("Failed to bootstrap the application:", error);
        process.exit(1);
    }
}

// Start the application
bootstrap();