# Architecture Design Specification

# 1. Patterns

## 1.1. Request-Reply (Synchronous)
### 1.1.2. Type
RequestReply

### 1.1.3. Implementation
Synchronous HTTP/REST communication, primarily routed via the API Gateway to backend microservices (e.g., Python/FastAPI services).

### 1.1.4. Applicability
Essential for client-to-service interactions (web/mobile frontends to backend) and some service-to-service calls where an immediate response is required. Examples include fetching user profiles (UAPM-1-003), managing brand kits (UAPM-1-004), and other CRUD operations on platform resources.

## 1.2. API Gateway
### 1.2.2. Type
APIGateway

### 1.2.3. Implementation
A dedicated service layer (e.g., Nginx with OpenResty/Lua, Kong, or a custom solution) acting as the single entry point. Integrates with the Authentication & Authorization Service for token validation (REQ-2-004).

### 1.2.4. Applicability
Centralizes access to backend microservices from all clients (web, mobile, third-party API users). Handles request routing, authentication, authorization, rate limiting (REQ-7-003, UAPM-1-008), and API key validation (REQ-2-005).

## 1.3. Message Queue
### 1.3.2. Type
MessageQueue

### 1.3.3. Implementation
RabbitMQ is used for point-to-point asynchronous messaging.

### 1.3.4. Applicability
Decouples long-running or resource-intensive tasks. Specifically used for the AI Generation Orchestration Service to publish creative generation jobs to be consumed by the n8n Workflow Engine (REQ-3-010).

## 1.4. Publish-Subscribe
### 1.4.2. Type
PublishSubscribe

### 1.4.3. Implementation
RabbitMQ for backend event propagation (e.g., to the Notification Service). WebSockets (via Notification Service) for real-time updates to web/mobile clients. HTTP Webhooks for notifying external API consumers.

### 1.4.4. Applicability
Broadcasting events to multiple interested consumers. Used for AI generation status/completion notifications (REQ-3-011, REQ-3-012), real-time collaboration updates (REQ-5-001 related), push notifications to mobile (REQ-8-006), and API developer webhook notifications (REQ-7-004).

## 1.5. Saga (Orchestration-based)
### 1.5.2. Type
Saga

### 1.5.3. Implementation
Orchestrated by an initiating service (e.g., Python/FastAPI) which manages a sequence of local transactions across services and executes compensating transactions in case of failures. Asynchronous steps within a saga may leverage RabbitMQ.

### 1.5.4. Applicability
Managing data consistency for distributed transactions spanning multiple microservices. Essential for business processes like user registration (UAPM-1-001: account creation, email verification, profile setup) and complex subscription lifecycle changes (REQ-6-006: updating user records, Odoo, payment gateway status).

## 1.6. Circuit Breaker
### 1.6.2. Type
CircuitBreaker

### 1.6.3. Implementation
Client-side libraries (e.g., `pybreaker` in Python services) that wrap calls to external third-party services.

### 1.6.4. Applicability
Enhancing system resilience by preventing repeated calls to failing external dependencies. Applied to interactions with AI services (OpenAI, Stability AI as per AISIML-005), payment gateways (Stripe, PayPal), and social media platform APIs (SMPIO-008).

## 1.7. CQRS (Command Query Responsibility Segregation)
### 1.7.2. Type
CQRS

### 1.7.3. Implementation
Separate logical (and potentially physical) paths for command (write) operations and query (read) operations. Read paths can utilize PostgreSQL read replicas (REQ-DA-013) or dedicated, denormalized read models updated asynchronously.

### 1.7.4. Applicability
Optimizing read performance and scalability for query-intensive features like user-facing dashboards displaying usage analytics (UAPM-1-005, REQ-WCI-005) and detailed usage reports for Pro+ users (REQ-6-009).

## 1.8. Backend for Frontend (BFF)
### 1.8.2. Type
BackendForFrontend

### 1.8.3. Implementation
One or more specialized backend services (e.g., Python/FastAPI or Node.js) or specific configurations/routing logic within the API Gateway, designed to cater to the unique needs of different frontend clients.

### 1.8.4. Applicability
Providing tailored API endpoints and data aggregations for distinct frontend experiences, specifically the web application (React, REQ-WCI series) and the native mobile applications (Flutter, REQ-8 series), optimizing data transfer and client-side logic.

## 1.9. Remote Procedure Invocation (RPC - Odoo Specific)
### 1.9.2. Type
RemoteProcedureInvocation

### 1.9.3. Implementation
XML-RPC or JSON-RPC communication from the `Subscription & Billing Service (Odoo Adapter)` to the `Odoo ERP Platform`, facilitated by a Python OdooRPC client library.

### 1.9.4. Applicability
Direct, synchronous (typically) integration with the Odoo ERP system for core business operations such as subscription management, billing, invoicing, and customer support ticket interactions (REQ-6-019, REQ-9-001).



---

