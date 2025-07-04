/**
 * @file server.ts
 * @description Main HTTP server setup using Express.
 */

import express, { Express, Request, Response } from 'express';
import { createServer, Server as HttpServer } from 'http';

/**
 * Creates and configures the underlying HTTP server. While this service is
 * primarily for WebSockets, an HTTP server is needed as a base for Socket.IO
 * and for standard operational endpoints like health checks.
 *
 * @returns An instance of http.Server.
 */
export function createHttpServer(): HttpServer {
    const app: Express = express();

    // Define a health check endpoint for monitoring and load balancers.
    app.get('/health', (req: Request, res: Response) => {
        res.status(200).json({ status: 'OK' });
    });

    return createServer(app);
}