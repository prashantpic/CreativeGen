# Software Design Specification: CreativeFlow.ApiGateway.Nginx

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `CreativeFlow.ApiGateway.Nginx` repository. This component serves as the central API Gateway for the CreativeFlow AI platform. It is responsible for routing client requests, enforcing security policies (authentication, authorization, rate limiting), SSL/TLS termination, and providing a unified entry point to the backend microservices.

### 1.2 Scope
The scope of this SDS covers the design and implementation of the API Gateway using OpenResty 1.25.3.1 (which includes Nginx 1.25.3). This includes:
- Nginx configuration for server blocks, location routing, upstreams, SSL, and rate limiting.
- Lua scripts for custom logic such as JWT validation, API key validation, CORS handling, and structured error responses.
- Integration points with upstream microservices, particularly the Authentication Service (`REPO-AUTH-SERVICE-001`).
- Containerization using Docker for deployment.
- Logging and monitoring configurations.

### 1.3 Definitions, Acronyms, and Abbreviations
- **API Gateway:** A server that acts as a single entry point into an application's microservices.
- **Nginx:** A high-performance web server, reverse proxy, and load balancer.
- **OpenResty:** A web platform based on Nginx and LuaJIT, extending Nginx with Lua scripting.
- **Lua:** A lightweight, multi-paradigm programming language.
- **JWT:** JSON Web Token.
- **API Key:** A secret token for authenticating API requests.
- **SSL/TLS:** Secure Sockets Layer / Transport Layer Security.
- **CORS:** Cross-Origin Resource Sharing.
- **IaC:** Infrastructure as Code.
- **SDS:** Software Design Specification.
- **SRS:** Software Requirements Specification.
- **CI/CD:** Continuous Integration / Continuous Deployment.

## 2. System Overview
The `CreativeFlow.ApiGateway.Nginx` is a critical component in the CreativeFlow AI microservices architecture. It sits behind Cloudflare and acts as the reverse proxy for all incoming client requests from the Web PWA, mobile applications, and third-party API consumers.

**Key Responsibilities:**
-   **Request Routing:** Directs traffic to the appropriate backend microservices based on request paths.
-   **Authentication & Authorization:** Validates JWTs and API keys, primarily by delegating to the Authentication Service. It passes identity context to upstream services.
-   **Rate Limiting:** Protects backend services from abuse and ensures fair usage.
-   **SSL/TLS Termination:** Handles HTTPS requests, decrypting traffic.
-   **CORS Handling:** Manages Cross-Origin Resource Sharing policies.
-   **Load Balancing:** Distributes load across instances of upstream services.
-   **Centralized Logging:** Provides a common point for logging all incoming requests.

**Diagrammatic Representation:**

[Clients (Web/Mobile/API)] -> [Cloudflare (CDN, WAF)] -> [CreativeFlow.ApiGateway.Nginx] -> [Backend Microservices]
                                                                  |
                                                                  v
                                                        [Authentication Service]


## 3. Functional Requirements & Design

This section details the design of each file within the repository.

### 3.1 `nginx.conf` (Main Configuration)
This is the root configuration file that bootstraps the Nginx server.

**Purpose:** Initialize the Nginx server, define global settings, and include all other configuration modules.
**Logic:**
-   **`user` & `worker_processes`:** Define the user Nginx runs as (e.g., `nginx`) and the number of worker processes (e.g., `auto`).
-   **`events` block:** Configure `worker_connections` for handling concurrent connections.
-   **`http` block:**
    -   Set up a custom `log_format` named `json_combined` to produce structured JSON logs, including variables like `$remote_addr`, `$request`, `$status`, `$body_bytes_sent`, `$http_referer`, `$http_user_agent`, `$request_time`, `$upstream_response_time`, and a custom `$correlation_id`.
    -   Define `access_log` and `error_log` paths.
    -   Enable `gzip` compression for text-based content types.
    -   Include `mime.types` file.
    -   Set `lua_package_path` to point to the `lua/?.lua;;` directory.
    -   Include `conf.d/gateway.conf`.

### 3.2 `upstreams/` Directory (Service Discovery & Load Balancing)
This directory will contain `.conf` files, each defining an upstream group for a backend microservice. This centralizes service locations and facilitates load balancing.

**File Template (`<service_name>.conf`):**
nginx
# /upstreams/auth_service.conf
upstream auth_service {
    least_conn; # Use least connections load balancing
    server auth_service_instance_1:8000;
    server auth_service_instance_2:8000;
    # Keepalive connections to upstream
    keepalive 32;
}

**Required Files:**
-   `auth_service.conf`
-   `user_management_service.conf`
-   `creative_management_service.conf`
-   *(And so on for every backend service defined in the architecture)*

### 3.3 `policies/` Directory (Security and Rate Limiting)

#### 3.3.1 `policies/ratelimit.conf`
**Purpose:** Define shared memory zones for rate limiting.
**Logic:**
-   Use `limit_req_zone` to define multiple zones:
    -   **`ip_limit`:** Keyed by `$binary_remote_addr`. A low rate for anonymous/unauthenticated traffic.
    -   **`user_limit`:** Keyed by `$authenticated_user_id` (a variable set by the `auth.lua` script). A more generous rate for logged-in UI users.
    -   **`apikey_limit`:** Keyed by `$http_x_api_key`. A rate specific to API key usage, potentially with different tiers.

#### 3.3.2 `policies/security.conf`
**Purpose:** Define common security headers to be applied to responses.
**Logic:**
-   Use `add_header` directives to set headers:
    -   `Strict-Transport-Security "max-age=31536000; includeSubDomains" always;`
    -   `X-Content-Type-Options "nosniff" always;`
    -   `X-Frame-Options "DENY" always;`
    -   `X-XSS-Protection "1; mode=block" always;`
    -   A strict `Content-Security-Policy` (CSP) header.

### 3.4 `conf.d/gateway.conf` (Primary Server Configuration)
**Purpose:** Defines the main server block, handles SSL, and includes all routing and policy logic.
**Logic:**
-   **Server Block 1 (HTTP to HTTPS Redirect):**
    -   `listen 80;`
    -   `server_name api.creativeflow.example.com;`
    -   `return 301 https://$host$request_uri;`
-   **Server Block 2 (HTTPS Gateway):**
    -   `listen 443 ssl http2;`
    -   `server_name api.creativeflow.example.com;`
    -   **SSL Configuration:**
        -   `ssl_certificate` and `ssl_certificate_key` paths.
        -   Define `ssl_protocols TLSv1.2 TLSv1.3;`
        -   Define `ssl_ciphers` with a modern, secure suite.
    -   **Includes:**
        -   `include policies/ratelimit.conf;`
        -   `include policies/security.conf;`
        -   `include locations/*.conf;`
    -   **Custom Error Pages:**
        -   `error_page` directives for 4xx and 5xx status codes to point to a location handled by `error_handler.lua`.
        -   `location @error_handler { content_by_lua_block { require("error_handler").handle() } }`

### 3.5 `locations/` Directory (Routing Logic)

#### 3.5.1 `locations/auth.conf`
**Purpose:** Route public authentication-related endpoints.
**Logic:**
-   `location /auth/` block.
    -   Applies the `ip_limit` rate limit.
    -   Uses `proxy_pass http://auth_service;`
    -   Sets required proxy headers (`Host`, `X-Real-IP`, etc.).

#### 3.5.2 `locations/api.conf`
**Purpose:** Secure and route all protected API endpoints. This is the core of the gateway's logic.
**Logic:**
-   `location /api/v1/` block.
    -   **Authentication Enforcement:**
        -   `access_by_lua_block { require("auth_handler").authenticate_request() }`
        -   This Lua script will validate the JWT/API Key and, on failure, will exit with a 401/403 status. On success, it will populate `ngx.ctx` and `ngx.var` with user details.
    -   **Rate Limiting:**
        -   `limit_req zone=user_limit burst=20;` or `limit_req zone=apikey_limit burst=50;` based on auth type (can be determined in Lua).
    -   **Proxy Headers:**
        -   Set standard headers: `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`.
        -   Set custom context headers from Lua variables: `proxy_set_header X-User-ID $authenticated_user_id;`, `proxy_set_header X-User-Roles $authenticated_user_roles;`.
    -   **CORS Handling:**
        -   `header_filter_by_lua_block { require("cors_handler").add_cors_headers() }` to add CORS headers to actual responses.
    -   **Nested Locations for Routing:**
        -   `location /api/v1/users/ { proxy_pass http://user_management_service; }`
        -   `location /api/v1/creatives/ { proxy_pass http://creative_management_service; }`
        -   ... and so on for all other services.

### 3.6 `lua/` Directory (Custom Logic)

#### 3.6.1 `lua/auth.lua`
**Purpose:** Handle JWT and API Key validation by calling the Authentication Service.
**Logic:**
lua
-- File: lua/auth.lua

-- Requires resty.http for making outbound requests and cjson for JSON
local http = require "resty.http"
local cjson = require "cjson"

local M = {}

-- Load from env vars for flexibility
local AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL") or "http://auth_service"

-- Private function to call the auth service
local function call_auth_service(token_or_key, validation_endpoint)
    local httpc = http.new()
    -- Set timeouts for resilience
    httpc:set_timeout(1000) -- 1 second

    local res, err = httpc:request_uri(AUTH_SERVICE_URL .. validation_endpoint, {
        method = "POST",
        body = cjson.encode(token_or_key),
        headers = {
            ["Content-Type"] = "application/json",
            ["X-Correlation-ID"] = ngx.req.get_headers()["X-Correlation-ID"] or ngx.var.request_id
        }
    })

    if not res then
        ngx.log(ngx.ERR, "Failed to connect to auth service: ", err)
        return nil, ngx.HTTP_SERVICE_UNAVAILABLE, "Auth service is currently unavailable."
    end

    if res.status ~= 200 then
        ngx.log(ngx.WARN, "Auth service returned non-200 status: ", res.status)
        -- Attempt to decode error message from auth service
        local err_body, _ = cjson.decode(res.body)
        local err_msg = (err_body and err_body.error and err_body.error.message) or "Invalid credentials."
        return nil, res.status, err_msg
    end

    return cjson.decode(res.body)
end

-- Main function called by Nginx
function M.authenticate_request()
    local auth_header = ngx.req.get_headers()["Authorization"]
    local api_key = ngx.req.get_headers()["X-API-Key"]

    local validation_result, status_code, err_msg

    if auth_header then
        local token = string.match(auth_header, "^[Bb]earer%s+(.+)$")
        if not token then
            return require("error_handler").handle(ngx.HTTP_UNAUTHORIZED, "Malformed Authorization header.")
        end
        validation_result, status_code, err_msg = call_auth_service({ token = token }, "/auth/validate-jwt")

    elseif api_key then
        validation_result, status_code, err_msg = call_auth_service({ apikey = api_key }, "/auth/validate-apikey")
        
    else
        return require("error_handler").handle(ngx.HTTP_UNAUTHORIZED, "Authentication credentials were not provided.")
    end
    
    -- Check result
    if not validation_result or not validation_result.valid then
        return require("error_handler").handle(status_code or ngx.HTTP_UNAUTHORIZED, err_msg or "Invalid credentials.")
    end

    -- Success: Set variables for upstream and other modules (e.g., rate limiting)
    ngx.var.authenticated_user_id = validation_result.user_id or "unknown"
    ngx.var.authenticated_user_roles = (validation_result.roles and cjson.encode(validation_result.roles)) or "[]"
    
    ngx.log(ngx.INFO, "User ", ngx.var.authenticated_user_id, " authenticated successfully.")
end

return M


#### 3.6.2 Other Lua Scripts
-   **`lua/cors_handler.lua`:** Implements `handle_preflight()` and `add_cors_headers()` to manage CORS policies dynamically based on the requesting origin.
-   **`lua/error_handler.lua`:** Implements a single function `handle()` which reads `ngx.status`, generates a standard JSON error payload (e.g., `{"error": {"status": 401, "message": "Unauthorized"}}`), sets the correct `Content-Type` header, and exits.

### 3.7 `Dockerfile`
**Purpose:** Create a portable Docker image for the gateway.
**Logic:**
dockerfile
# Stage 1: (Optional) Build stage for any custom Lua modules if needed
# FROM openresty/openresty:1.25.3.1-0-jammy as builder
# RUN ...

# Stage 2: Final production image
FROM openresty/openresty:1.25.3.1-0-jammy

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom configurations
COPY nginx.conf /etc/nginx/nginx.conf
COPY mime.types /etc/nginx/mime.types
COPY conf.d/ /etc/nginx/conf.d/
COPY upstreams/ /etc/nginx/upstreams/
COPY locations/ /etc/nginx/locations/
COPY policies/ /etc/nginx/policies/

# Copy Lua scripts
COPY lua/ /usr/local/openresty/lualib/creativeflow/

# Expose ports
EXPOSE 80 443

# Command to start Nginx in the foreground
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]

This Dockerfile creates a lean, production-ready image containing the OpenResty server and all necessary custom configurations and scripts. It is designed to be configured further via environment variables passed during container startup.