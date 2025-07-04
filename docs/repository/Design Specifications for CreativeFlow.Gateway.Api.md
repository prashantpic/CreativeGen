# Software Design Specification (SDS): CreativeFlow.Gateway.Api

## 1. Introduction

### 1.1. Purpose
This document outlines the software design for the **CreativeFlow API Gateway (`CreativeFlow.Gateway.Api`)**. The API Gateway serves as the single, secure entry point for all external client requests to the CreativeFlow AI platform, including the Web PWA, mobile applications, and third-party developer integrations. Its primary responsibilities are to route requests to the appropriate backend microservices, enforce security policies, manage traffic, and provide a unified interface to the backend architecture.

### 1.2. Scope
This specification covers the design and implementation of the API Gateway using **OpenResty (Nginx with Lua)**. It includes:
- Request routing and load balancing configuration.
- SSL/TLS termination.
- Implementation of authentication mechanisms (JWT and API Key validation).
- Rate limiting and Cross-Origin Resource Sharing (CORS) policies.
- WebSocket proxying for real-time services.
- Modular configuration structure for maintainability and scalability.

## 2. System Architecture & Design Principles

The API Gateway is designed based on the following principles:

- **Performance and Low Latency:** Nginx and LuaJIT are chosen for their high performance and low memory footprint, making them ideal for handling a large volume of concurrent requests at the edge.
- **Extensibility and Customization:** OpenResty allows for custom logic to be written in Lua, enabling sophisticated handling of authentication, authorization, and request transformation directly at the gateway layer, reducing latency and load on backend services.
- **Modularity and Maintainability:** The configuration is broken down into logical, modular files (`upstreams`, `policies`, domain-specific `routes`). This approach, based on Nginx's `include` directive, makes the gateway configuration easier to understand, manage, and scale as the number of services and routes grows.
- **Security First:** The gateway acts as a critical security enforcement point. It validates all incoming credentials and applies security policies before any request reaches the internal network, protecting backend services from unauthenticated traffic and common threats.
- **Centralized Cross-Cutting Concerns:** Common concerns like authentication, rate limiting, and logging are handled centrally at the gateway, simplifying the logic required in individual backend microservices.

## 3. Component Specification

The API Gateway is implemented through a series of Nginx configuration files and Lua scripts.

### 3.1. Nginx Configuration Files

#### 3.1.1. `nginx.conf` (Main Configuration)
This is the root configuration file for the OpenResty server.
- **Purpose:** To initialize the server process and load all other configuration modules.
- **Directives:**
    - `user nginx;`: Sets the worker process user.
    - `worker_processes auto;`: Automatically detects the number of CPU cores for optimal performance.
    - `error_log /var/log/nginx/error.log warn;`: Defines the global error log.
    - `pid /var/run/nginx.pid;`: Specifies the process ID file.
    - `http {}` block:
        - `include /etc/nginx/mime.types;`: Loads MIME type mappings.
        - `default_type application/octet-stream;`: Sets a default MIME type.
        - `log_format main '...'`: Defines a custom log format including upstream response times and custom headers (e.g., User ID).
        - `sendfile on;`: Enables efficient file sending.
        - `keepalive_timeout 65;`: Sets the keep-alive connection timeout.
        - `include /etc/nginx/conf.d/*.conf;`: The most critical directive, loading all subsequent configuration files.

#### 3.1.2. `conf.d/00-upstreams.conf` (Upstream Services)
- **Purpose:** To define named server pools for each backend microservice, enabling load balancing.
- **Structure:**
    - Contains one `upstream` block per backend service.
    - **Example (`auth_service`):**
      nginx
      upstream auth_service {
          least_conn; # Distributes load to the server with the least active connections
          server auth_service_1.internal:8000 max_fails=3 fail_timeout=30s;
          server auth_service_2.internal:8000 max_fails=3 fail_timeout=30s;
          keepalive 32; # Keep-alive connections to upstream servers
      }
      
    - **Upstreams to define:**
        - `auth_service` (for Authentication & User Management)
        - `creative_management_service`
        - `aigeneration_orchestration_service`
        - `subscription_billing_service`
        - `api_developer_service`
        - `collaboration_service` (for WebSockets)
        - `notification_service` (for WebSockets)

#### 3.1.3. `conf.d/01-policies.conf` (Global Policies)
- **Purpose:** To centralize definitions for rate limiting and CORS policies.
- **Structure:**
    - **Rate Limiting:**
      nginx
      # General limit for authenticated users, based on user ID passed from Lua
      limit_req_zone $http_x_user_id zone=user_api_limit:10m rate=20r/s;
      
      # Stricter limit for login attempts by IP to prevent brute-forcing
      limit_req_zone $binary_remote_addr zone=login_limit:10m rate=10r/m;
      
      # Limit for third-party developers based on their API key
      limit_req_zone $http_x_api_key zone=developer_api_limit:10m rate=5r/s;
      
    - **CORS Handling:**
      nginx
      # Map to control CORS headers
      map $http_origin $cors_header {
          "~https://(.*\.)?creativeflow\.ai" "$http_origin";
          default "";
      }
      

#### 3.1.4. `conf.d/10-gateway.conf` (Main Virtual Server)
- **Purpose:** To define the primary virtual server that listens for traffic, handles SSL, and includes all routing logic.
- **Structure:**
  nginx
  # Redirect HTTP to HTTPS
  server {
      listen 80;
      server_name api.creativeflow.ai;
      return 301 https://$host$request_uri;
  }

  server {
      listen 443 ssl http2;
      server_name api.creativeflow.ai;

      # SSL Configuration
      ssl_certificate /path/to/fullchain.pem;
      ssl_certificate_key /path/to/privkey.pem;
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';
      ssl_prefer_server_ciphers on;

      # Default location block for unmatched routes
      location / {
          return 404 '{"error": "Not Found"}';
      }

      # Include all domain-specific route configurations
      include /etc/nginx/conf.d/routes/*.conf;
  }
  

#### 3.1.5. Route Configuration Files (`conf.d/routes/*.conf`)
These files contain the specific `location` blocks for routing.

- **`auth.conf`:**
  - `location /api/v1/auth/register`: Proxies to `auth_service`.
  - `location /api/v1/auth/login`: Applies `login_limit` rate limit and proxies to `auth_service`.
  - `location /api/v1/profiles/`: Requires JWT auth via `auth_jwt.lua`, applies `user_api_limit`, proxies to `auth_service`.

- **`creative_services.conf`:**
  - `location ~ ^/api/v1/(workbenches|projects|assets)`: Requires JWT auth via `auth_jwt.lua`, applies `user_api_limit`, proxies to `creative_management_service`.
  - `location /api/v1/generate/`: Requires JWT auth, applies `user_api_limit`, proxies to `aigeneration_orchestration_service`.

- **`api_platform.conf`:**
  - `location /public-api/v1/`: Requires API Key auth via `auth_apikey.lua`, applies `developer_api_limit`, proxies to `api_developer_service`.

- **`realtime_services.conf`:**
  - **Purpose:** To enable WebSocket proxying.
  - **Structure:**
    nginx
    location /ws/ {
        # JWT auth is still required to establish the connection
        access_by_lua_file /etc/nginx/lua/auth_jwt.lua;

        # WebSocket proxy settings
        proxy_pass http://notification_service; # Or collaboration_service based on path
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
    

### 3.2. Lua Scripts (`lua/*.lua`)

#### 3.2.1. `lua/auth_jwt.lua` (JWT Validation)
- **Purpose:** To validate JWTs for authenticated users.
- **Libraries:**
    - `resty.jwt` for JWT parsing and verification.
    - `cjson` for JSON operations.
- **Logic:**
    1.  **Extract Token:** Retrieve the token from the `Authorization: Bearer <token>` header. If not present or malformed, return `401 Unauthorized`.
    2.  **Get Secret:** Load the JWT secret key from a secure source (e.g., an environment variable `JWT_SECRET`).
    3.  **Verify Signature & Claims:** Use `jwt:verify()` to check the signature. The library automatically validates standard claims like `nbf` (not before) and `exp` (expiration). Check `iss` (issuer) and `aud` (audience) claims against expected values. If verification fails, return `401 Unauthorized`.
    4.  **Forward Claims:** If valid, extract `sub` (user ID) and `roles` from the token payload.
    5.  **Set Request Headers:** Use `ngx.req.set_header()` to add `X-User-ID` and `X-User-Roles` headers to the request before passing it to the upstream service. This allows backend services to trust the user's identity without re-validating the JWT.

#### 3.2.2. `lua/auth_apikey.lua` (API Key Validation)
- **Purpose:** To validate API keys for third-party developers.
- **Libraries:**
    - `resty.http` for making subrequests.
    - `resty.redis` (optional, for caching).
- **Logic:**
    1.  **Extract Key:** Retrieve the API key from the `X-API-Key` request header. If not present, return `401 Unauthorized`.
    2.  **Cache Lookup (Optional):**
        - Create a cache key from the API key.
        - Attempt to retrieve key details (e.g., associated User ID, rate limit plan, permissions) from a local Redis cache.
        - If found in cache and valid, proceed to step 5.
    3.  **Validation Subrequest:**
        - If not in cache, create a new internal HTTP request (`ngx.location.capture`) to an internal endpoint on the `api_developer_service` (e.g., `/internal/api/v1/keys/validate`).
        - This endpoint will validate the key against the database and return user/permission details.
    4.  **Process Subrequest Response:**
        - If the subrequest returns `200 OK`, cache the response in Redis with a TTL (e.g., 5 minutes) and proceed.
        - If it returns `401` or `403`, return the same status code to the client.
        - If it returns any other error, return `500 Internal Server Error`.
    5.  **Forward Claims:** If the key is valid, add `X-User-ID` and `X-API-Key` headers to the original request for the upstream service. This allows the API service to identify the user without re-validating the key.

## 4. Error Handling
- The main `10-gateway.conf` will define custom error pages using the `error_page` directive for common status codes like `401`, `403`, `404`, `429`, and `50x`.
- These pages will return a standardized JSON error response, e.g., `{"status": 404, "error": "Not Found", "requestId": "..."}`.
- A request ID (`$request_id`) will be generated for each request and included in logs and error responses to facilitate troubleshooting.

## 5. Logging
- A custom `log_format` named `gateway` will be defined in the main `http` block.
- **Format Definition:**
  nginx
  log_format gateway '$remote_addr - $remote_user [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for" '
                     'rt=$request_time uct="$upstream_connect_time" uht="$upstream_header_time" urt="$upstream_response_time" '
                     'uid="$http_x_user_id" apikey="$http_x_api_key"';
  
- All `server` blocks will use `access_log /path/to/access.log gateway;` to ensure consistent, rich logging for analysis and monitoring.

## 6. Environment Configuration
- **Mechanism:** Environment-specific values (e.g., upstream hostnames, JWT secrets, database connection strings for Lua scripts) will be passed into the Docker container as environment variables at startup.
- **Implementation:**
    - Nginx configurations can reference these variables using OpenResty's `env` directive or by using a startup script that substitutes placeholders in `.conf` files.
    - Lua scripts will use `os.getenv("VAR_NAME")` to read these values.
- This approach ensures that the same container image can be deployed across different environments (Dev, Staging, Production) without modification, adhering to the principles of Infrastructure as Code.