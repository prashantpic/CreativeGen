# Software Design Specification: CreativeFlow.ApiGateway

## 1. Introduction

This document outlines the software design specification for the `CreativeFlow.ApiGateway` repository. The API Gateway is a critical component of the CreativeFlow AI platform, serving as the central entry point for all client requests originating from web applications, mobile applications, and third-party API consumers.

**Purpose:**
The API Gateway is responsible for:
*   Request routing to appropriate backend microservices.
*   Enforcing security policies, including JWT-based authentication for platform users and API key-based authentication for developer APIs.
*   Implementing rate limiting and basic quota management.
*   SSL/TLS termination for secure communication.
*   Providing a unified and consistent API front for disparate backend services, decoupling clients from the internal microservice architecture.
*   Optionally performing basic input validation and response caching.

**Scope:**
This SDS covers the design and implementation of the Nginx configuration files and Lua scripts that constitute the API Gateway. It details how these components fulfill the requirements related to routing, security, rate limiting, and operational aspects of the gateway.

**Technology Stack:**
*   **Core Engine:** OpenResty 1.25.3.1 (which bundles Nginx 1.25.3, LuaJIT, and core `lua-resty-*` libraries).
*   **Scripting Language:** Lua 5.1 (via LuaJIT).
*   **Nginx Modules:**
    *   `ngx_http_ssl_module`: For SSL/TLS termination.
    *   `ngx_http_proxy_module`: For reverse proxying requests to upstream services.
    *   `ngx_http_upstream_module`: For defining backend service pools and load balancing.
    *   `ngx_http_limit_req_module`: For request rate limiting.
    *   `ngx_http_rewrite_module` (and `ngx_http_lua_module` via OpenResty): For request processing and custom logic.
    *   `ngx_http_headers_module`: For manipulating HTTP headers.
    *   `ngx_http_map_module`: For creating mappings between variables.
*   **Lua Libraries (via OpenResty):**
    *   `lua-resty-core`: Core Nginx Lua API.
    *   `lua-cjson`: Fast JSON encoding/decoding.
    *   `lua-resty-jwt`: For JWT validation (if custom Lua validation is preferred over Nginx Plus JWT module or external auth service).
    *   `lua-resty-http`: For making HTTP subrequests (e.g., to an auth service for complex API key validation or introspection).
    *   `lua-jsonschema` (or similar): For advanced input validation if `enable_advanced_input_validation_lua` is true.

## 2. Architectural Overview

The API Gateway is built upon OpenResty, a high-performance web platform based on Nginx and LuaJIT. Nginx's event-driven architecture provides efficient request handling, while Lua scripting allows for flexible and powerful custom logic execution at various request processing phases.

**Key Architectural Patterns:**
*   **API Gateway Pattern:** Centralized request handling and policy enforcement.
*   **Reverse Proxy Pattern:** Nginx proxies requests to appropriate backend microservices.
*   **Load Balancer Pattern:** Nginx upstreams distribute load across instances of backend services.
*   **Modular Configuration:** Nginx configuration is broken down into smaller, manageable files for better organization and maintainability. Lua scripts encapsulate specific functionalities like JWT validation or API key checking.

**Request Lifecycle (Simplified):**
1.  Client request arrives at the API Gateway (Nginx).
2.  SSL/TLS termination is handled.
3.  Request matches a `server` block (e.g., `api.creativeflow.ai`).
4.  Security policies (headers, CORS) are applied.
5.  Request matches a `location` block based on the URI.
6.  Authentication:
    *   If JWT is required: `jwt_validator.lua` (or Nginx JWT module) is invoked.
    *   If API Key is required: `api_key_validator.lua` is invoked.
7.  Rate Limiting: `limit_req` directive enforces configured limits based on IP or validated API key tier.
8.  Input Validation (Optional): If `enable_advanced_input_validation_lua` is true for the route, `input_validator.lua` may be invoked.
9.  Request is proxied to the configured upstream service using `proxy_pass`.
10. Response from the upstream service is received.
11. Response headers may be modified.
12. Response is sent back to the client.

**Feature Toggles:**
Feature toggles (`enable_advanced_input_validation_lua`, `enable_complex_api_key_lua_validation`) will be managed via environment variables accessible to Lua scripts using `os.getenv("TOGGLE_NAME")`. Lua scripts will check these environment variables to conditionally execute specific logic paths.

## 3. File Specifications

### 3.1. `nginx.conf`

*   **Purpose:** Main Nginx global configuration file. Initializes core Nginx settings, worker processes, event handling, and defines the HTTP context, including global logging and inclusion of modular configurations.
*   **Directives and Blocks:**
    *   `user <nginx_user> <nginx_group>;`: Specifies the user and group for worker processes (e.g., `nginx nginx` or `www-data www-data`).
    *   `worker_processes auto;`: Sets the number of worker processes (auto-detect based on CPU cores is common).
    *   `error_log /var/log/nginx/error.log warn;`: Defines the global error log file and logging level.
    *   `pid /var/run/nginx.pid;`: Specifies the PID file location.
    *   `events { worker_connections 1024; }`: Configures event processing model and maximum connections per worker.
    *   `http { ... }`: Defines the HTTP server settings.
*   **HTTP Block Details:**
    *   `include /etc/nginx/mime.types;`: Includes MIME type definitions.
    *   `default_type application/octet-stream;`: Default MIME type.
    *   `log_format main_ext '$remote_addr - $remote_user [$time_local] "$request" ' ...;`: Defines a detailed log format. (See section 3.1.1 for specific format).
    *   `access_log /var/log/nginx/access.log main_ext;`: Specifies the global access log.
    *   `sendfile on;`: Enables efficient file transfer.
    *   `tcp_nopush on;`: Optimizes TCP packet transmission.
    *   `keepalive_timeout 65;`: Sets keep-alive connection timeout.
    *   `gzip on;`: Enables GZIP compression (configurable).
    *   `include /etc/nginx/conf.d/*.conf;`: Loads all modular configuration files from `conf.d`.
    *   `client_max_body_size 50m;`: Sets a reasonable max request body size (e.g., for file uploads via API).
*   **Logic Flow:** Initializes Nginx master and worker processes. Sets global defaults for HTTP request handling and logging. Delegates specific server and location configurations to files in `conf.d`.
*   **Requirements Addressed:** Section 5.1 (API Gateway Role), Section 5.2.2 (API Gateway Component).

#### 3.1.1. `main_ext` Log Format
The `main_ext` log format should be defined as follows to capture essential information for debugging and analytics:
nginx
log_format main_ext '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for" '
                   'rt=$request_time urt="$upstream_response_time" "$upstream_addr" '
                   'cs=$upstream_cache_status jwt_sub="$jwt_subject" api_key_id="$api_key_id"';

*   `$jwt_subject`: To be set by `jwt_validator.lua` (e.g., `ngx.var.jwt_subject = claims.sub`).
*   `$api_key_id`: To be set by `api_key_validator.lua` (e.g., `ngx.var.api_key_id = validated_key_info.id`).

### 3.2. `conf.d/00-main-server.conf`

*   **Purpose:** Defines the primary server block that listens for HTTPS requests, handles SSL/TLS termination, sets server-specific defaults, and includes further route-specific configurations.
*   **Directives and Blocks:**
    *   `server { ... }`: Main server configuration block.
*   **Server Block Details:**
    *   `listen 443 ssl http2;`: Listen on port 443 for HTTPS and enable HTTP/2.
    *   `listen [::]:443 ssl http2;`: Listen on port 443 for IPv6 HTTPS and enable HTTP/2.
    *   `server_name api.creativeflow.ai www.api.creativeflow.ai;`: Define server names. (Consider if `www.` prefix is needed for an API).
    *   `ssl_certificate /etc/nginx/ssl/creativeflow.ai.pem;`: Path to the SSL public certificate.
    *   `ssl_certificate_key /etc/nginx/ssl/creativeflow.ai.key;`: Path to the SSL private key.
    *   `ssl_protocols TLSv1.2 TLSv1.3;`: Specify allowed SSL/TLS protocols.
    *   `ssl_prefer_server_ciphers on;`: Server chooses cipher.
    *   `ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';`: Recommended strong ciphers.
    *   `ssl_session_cache shared:SSL:10m;`: Shared SSL session cache.
    *   `ssl_session_timeout 1d;`: SSL session timeout.
    *   `ssl_session_tickets off;`: Disable SSL session tickets for better forward secrecy (optional, trade-off).
    *   `add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;`: HSTS header.
    *   `include /etc/nginx/conf.d/02-security_policies.conf;`: Include global security headers and CORS. (Note: `02-security_policies.conf` might be better structured to be included here, or directly define its content if it's server-wide).
    *   `include /etc/nginx/conf.d/10-health_check.conf;`: Includes the health check location block.
    *   `include /etc/nginx/conf.d/routes/*.conf;`: Includes all API route configurations.
    *   `location / { return 404; }`: Default handler for unmatched routes.
    *   `error_page 401 /401.json; location = /401.json { internal; root /usr/share/nginx/html/errors; }`: Custom error pages for JSON APIs. Similar for 403, 404, 429, 50x.
*   **Logic Flow:** Acts as the main entry point for HTTPS traffic. Terminates SSL, applies common security settings, and then delegates request handling to more specific location blocks defined in included route files.
*   **Requirements Addressed:** Section 5.2.2 (API Gateway Component - SSL Termination).

### 3.3. `conf.d/01-upstreams.conf`

*   **Purpose:** Defines named upstream groups for all backend microservices. This allows Nginx to load balance requests across multiple instances of each service and manage their availability.
*   **Directives and Blocks:**
    *   `upstream <service_name> { ... }`: Defines an upstream block for a service.
*   **Upstream Block Details (Example for `auth_service`):**
    *   `upstream auth_service {`
        *   `# least_conn; # Example load balancing algorithm`
        *   `server auth_service_host1:port; # e.g., auth-svc-01.internal:8080`
        *   `server auth_service_host2:port; # e.g., auth-svc-02.internal:8080`
        *   `# server auth_service_host3:port backup; # Example backup server`
        *   `keepalive 32; # Number of keepalive connections to each upstream server`
        *   `# health_check interval=5s fails=3 passes=2 uri=/health; # If using Nginx Plus or active health checks`
    *   }`
*   **List of Upstreams (to be defined based on project microservices):**
    *   `auth_service` (REPO-AUTH-SERVICE-001)
    *   `user_profile_service` (REPO-USERPROFILE-SERVICE-001)
    *   `creative_mgmt_service` (REPO-CREATIVEMGMT-SERVICE-001)
    *   `ai_generation_orchestration_service` (REPO-AIGEN-ORCH-SERVICE-001)
    *   `billing_adapter_service` (REPO-SUBBILLING-ADAPTER-001)
    *   `developer_api_platform_service` (REPO-DEVPLATFORM-SERVICE-001)
    *   `collaboration_service` (REPO-COLLABORATION-SERVICE-001)
    *   `notification_service` (REPO-NOTIFICATION-SERVICE-001)
    *   `social_publishing_service` (REPO-SOCIALPUB-SERVICE-001)
    *   `mlops_platform_service` (REPO-MLOPS-SERVICE-001)
    *   *Add other services as they are defined.*
*   **Load Balancing Strategy:** Default is round-robin. `least_conn` can be considered. `ip_hash` for session persistence if strictly needed, but ideally services are stateless.
*   **Health Checks:** If not using Nginx Plus, active health checks for open-source Nginx would require custom Lua scripting with `ngx.timer.at` and shared dictionaries, or relying on `max_fails` and `fail_timeout` for passive health checking.
*   **Logic Flow:** Provides a pool of backend servers for each microservice. Nginx uses the specified load balancing algorithm to distribute requests. Handles server failures based on `max_fails` and `fail_timeout`.
*   **Requirements Addressed:** Section 5.2.2 (API Gateway Component - Routing to upstreams), REQ-017.

### 3.4. `conf.d/02-security_policies.conf`

*   **Purpose:** Centralizes common HTTP security headers and CORS (Cross-Origin Resource Sharing) policies. These are typically included in the main `server` block.
*   **Directives:**
    *   `add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;` (Moved to `00-main-server.conf` as it's HTTPS specific)
    *   `add_header X-Content-Type-Options "nosniff" always;`
    *   `add_header X-Frame-Options "SAMEORIGIN" always;`
    *   `add_header X-XSS-Protection "1; mode=block" always;`
    *   `add_header Referrer-Policy "strict-origin-when-cross-origin" always;`
    *   `add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' wss://api.creativeflow.ai; frame-ancestors 'self';" always;` (Example CSP, needs careful tuning for actual application needs, especially if using CDNs for assets or third-party scripts).
*   **CORS Configuration (Example for a specific path, can be global or location-specific):**
    *   Use a `map` to whitelist origins for `Access-Control-Allow-Origin`.
    nginx
    # In http block of nginx.conf or a global include
    map $http_origin $cors_origin {
        default "";
        "~^https?://(localhost|app\.creativeflow\.ai|staging-app\.creativeflow\.ai)" $http_origin;
    }

    # In 02-security_policies.conf or specific location blocks
    # For OPTIONS preflight requests
    if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' $cors_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,X-API-Key' always;
        add_header 'Access-Control-Max-Age' 1728000; # 20 days
        add_header 'Content-Type' 'text/plain charset=UTF-8';
        add_header 'Content-Length' 0;
        return 204;
    }

    # For actual requests
    add_header 'Access-Control-Allow-Origin' $cors_origin always;
    add_header 'Access-Control-Allow-Credentials' 'true' always; # If credentials (cookies, auth headers) are used
    add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range,X-Request-ID' always; # Expose custom headers
    
*   **Logic Flow:** These directives are applied to responses sent by the server, enhancing security and controlling cross-origin access. The CORS logic handles preflight OPTIONS requests and adds necessary headers to actual requests from allowed origins.
*   **Requirements Addressed:** SEC-005 (API Protection - Security Headers, CORS).

### 3.5. `conf.d/03-rate_limiting_policies.conf`

*   **Purpose:** Defines named rate limiting zones using the `limit_req_zone` directive. These zones are then applied in specific `location` blocks to control request rates.
*   **Directives:**
    *   `limit_req_zone $binary_remote_addr zone=per_ip_general:20m rate=10r/s;`
        *   `key`: `$binary_remote_addr` (limits per IP).
        *   `zone=per_ip_general:20m`: Shared memory zone name and size (20MB).
        *   `rate=10r/s`: Allow 10 requests per second on average per IP.
    *   `limit_req_zone $api_key_id zone=per_api_key_free:10m rate=1r/s;` (Example for a "Free" tier API key)
    *   `limit_req_zone $api_key_id zone=per_api_key_pro:10m rate=10r/s;` (Example for a "Pro" tier API key)
    *   `limit_req_zone $api_key_id zone=per_api_key_enterprise:10m rate=50r/s;` (Example for an "Enterprise" tier API key)
    *   `limit_req_zone $jwt_subject zone=per_user_actions:10m rate=5r/s;` (Example for limiting specific actions per authenticated user).
    *   `limit_req_status 429;`: Sets the HTTP status code for rate-limited requests. This should be in the `http` or `server` block.
*   **Variables for Keys:**
    *   `$api_key_id`: This variable will be set by `api_key_validator.lua` (e.g., `ngx.var.api_key_id = validated_key_info.key_id .. "_" .. validated_key_info.tier_id`).
    *   `$jwt_subject`: This variable will be set by `jwt_validator.lua` (e.g., `ngx.var.jwt_subject = claims.sub`).
*   **Logic Flow:** Defines shared memory zones to track request counts against specified keys (IP, API key ID, JWT subject). The `rate` parameter determines the average allowed rate. These zones are referenced by `limit_req` directives in `location` blocks.
*   **Requirements Addressed:** SEC-005 (Rate limiting), REQ-018 (Rate limiting and quota management).

### 3.6. `conf.d/04-caching_policies.conf` (Optional)

*   **Purpose:** Configures proxy caching for responses from certain backend services to improve performance and reduce origin load. This is optional as per current requirements but good practice.
*   **Directives:**
    *   `proxy_cache_path /var/cache/nginx/api_responses levels=1:2 keys_zone=api_responses_cache:50m inactive=30m max_size=500m use_temp_path=off;`
        *   Defines cache storage path, directory levels, zone name and size, inactivity timeout, max cache size. `use_temp_path=off` avoids unnecessary disk writes.
    *   `proxy_cache_key "$scheme$request_method$host$request_uri$is_args$args";` (Example cache key).
    *   `proxy_cache_valid 200 302 10m;` (Cache 200/302 responses for 10 minutes).
    *   `proxy_cache_valid 404 1m;` (Cache 404s for 1 minute).
    *   `proxy_cache_use_stale error timeout invalid_header updating http_500 http_502 http_503 http_504;` (Serve stale cache on errors).
*   **Logic Flow:** Defines cache zones and parameters. Specific `location` blocks can then use `proxy_cache <zone_name>;` to enable caching for their proxied responses. Cache bypass and purging mechanisms would need to be considered.
*   **Requirements Addressed:** (None explicitly, but contributes to NFR-001 Performance).

### 3.7. `conf.d/10-health_check.conf`

*   **Purpose:** Provides a simple, unauthenticated health check endpoint for the API Gateway itself, typically used by external load balancers or monitoring systems.
*   **Directives and Blocks:**
    *   `location = /health { ... }`: Specific location for health check.
*   **Location Block Details:**
    *   `access_log off;`: Disable access logging for health checks.
    *   `return 200 "OK";`
    *   `# Or more advanced: content_by_lua_block { ngx.say("OK") }`
*   **Logic Flow:** Any request to `/health` will immediately return a 200 OK response with "OK" in the body.
*   **Requirements Addressed:** Implied for operational health monitoring (DEP-005).

### 3.8. Route Configuration Files (`conf.d/routes/*.conf`)

#### 3.8.1. `conf.d/routes/auth_api.conf` (Example)

*   **Purpose:** Routes requests prefixed with `/api/v1/auth/` to the `auth_service` upstream.
*   **Directives and Blocks:**
    *   `location /api/v1/auth/ { ... }`: Matches the base path for auth services.
*   **Location Block Details:**
    *   `# Public endpoints (e.g., login, register, refresh token, password reset initiate)`
    *   `location /api/v1/auth/login {`
        *   `limit_req zone=per_ip_general burst=5 nodelay;`
        *   `proxy_set_header Host $host;`
        *   `proxy_set_header X-Real-IP $remote_addr;`
        *   `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
        *   `proxy_set_header X-Forwarded-Proto $scheme;`
        *   `proxy_pass http://auth_service/login;`
    *   `}`
    *   `location /api/v1/auth/register {`
        *   `limit_req zone=per_ip_general burst=3 nodelay;`
        *   `proxy_pass http://auth_service/register; # Headers as above`
    *   `}`
    *   `# Protected endpoints (e.g., logout, change password - require JWT)`
    *   `location /api/v1/auth/logout {`
        *   `access_by_lua_file /etc/nginx/lua/jwt_validator.lua; # Ensures valid JWT`
        *   `limit_req zone=per_user_actions burst=5 nodelay; # Use $jwt_subject based zone`
        *   `proxy_pass http://auth_service/logout; # Headers as above`
    *   `}`
*   **Logic Flow:** Matches specific auth-related paths. Applies appropriate rate limiting. For protected endpoints, invokes `jwt_validator.lua`. Proxies requests to the `auth_service` upstream, setting necessary proxy headers.
*   **Requirements Addressed:** REQ-017, SEC-001.

#### 3.8.2. `conf.d/routes/protected_api_example.conf` (Generic Template for Microservices)

*   **Purpose:** Serves as a template or example for routing requests to various protected backend microservices, demonstrating JWT validation, rate limiting, and proxying. This structure will be replicated and adapted for `user_profile_api.conf`, `creative_mgmt_api.conf`, etc.
*   **Directives and Blocks (Example for `/api/v1/user-profiles/`):**
    *   `location /api/v1/user-profiles/ {`
        *   `# Phase 1: Authentication & Authorization`
        *   `access_by_lua_file /etc/nginx/lua/jwt_validator.lua;`
        *   `# jwt_validator.lua should populate ngx.ctx.authenticated_user or specific headers`
        *   `# Optionally, an authorization Lua script could be called here based on ngx.ctx`

        *   `# Phase 2: Rate Limiting (User-specific if JWT validated)`
        *   `# Define map in http block or 03-rate_limiting_policies.conf`
        *   `# map $jwt_user_tier $user_rate_limit_zone {`
        *   `#   default per_ip_general;`
        *   `#   free    per_user_free_tier;`
        *   `#   pro     per_user_pro_tier;`
        *   `# }`
        *   `# Assume jwt_validator.lua sets ngx.var.jwt_user_tier`
        *   `# limit_req zone=$user_rate_limit_zone burst=10 nodelay;`
        *   `limit_req zone=per_ip_general burst=20 nodelay; # Fallback or general limit`

        *   `# Phase 3: Input Validation (Optional, feature-toggled)`
        *   `# Assuming a Lua variable $needs_validation is set based on endpoint`
        *   `# content_by_lua_block {`
        *   `#    local needs_validation = ngx.var.needs_validation == "1"`
        *   `#    local toggle_enabled = os.getenv("ENABLE_ADVANCED_INPUT_VALIDATION_LUA") == "true"`
        *   `#    if needs_validation and toggle_enabled then`
        *   `#        local validator = require "input_validator"`
        *   `#        local schema_name = "user_profile_update_schema" -- map this dynamically`
        *   `#        local ok, err = validator.validate_current_request(schema_name)`
        *   `#        if not ok then`
        *   `#            ngx.status = ngx.HTTP_BAD_REQUEST`
        *   `#            ngx.say(require("cjson").encode({errors = err}))`
        *   `#            return ngx.exit(ngx.HTTP_BAD_REQUEST)`
        *   `#        end`
        *   `#    end`
        *   `#    ngx.exec("@actual_proxy_user_profiles"); -- Proceed to proxy if valid`
        *   `# }`

        *   `# Phase 4: Proxying to Upstream (use named location for complex pre-proxy logic)`
        *   `# location @actual_proxy_user_profiles {`
        *   `#     internal;`
        *   `proxy_set_header Host $host;`
        *   `proxy_set_header X-Real-IP $remote_addr;`
        *   `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
        *   `proxy_set_header X-Forwarded-Proto $scheme;`
        *   `# Pass authenticated user info to backend`
        *   `proxy_set_header X-User-ID $jwt_user_id; # Set by jwt_validator.lua`
        *   `proxy_set_header X-User-Roles $jwt_user_roles; # Set by jwt_validator.lua`
        *   `proxy_pass http://user_profile_service/user-profiles/;`
        *   `# }`
    *   `}`
*   **Logic Flow:**
    1.  Matches a base path for a microservice.
    2.  Invokes `jwt_validator.lua` for authentication.
    3.  Applies rate limiting (could be user-specific or IP-based).
    4.  Optionally, complex input validation via Lua if enabled.
    5.  Proxies the request to the appropriate upstream service, passing necessary headers (original host, client IP, authenticated user details from JWT claims).
*   **Requirements Addressed:** REQ-017, SEC-001 (JWT validation), SEC-005 (rate limiting, input validation).

#### 3.8.3. `conf.d/routes/developer_api.conf`

*   **Purpose:** Routes requests for the external developer API (prefixed e.g., `/developer/v1/`), enforces API key authentication, and applies API key-specific rate limits/quotas.
*   **Directives and Blocks (Example for `/developer/v1/creations/`):**
    *   `location /developer/v1/creations/ {`
        *   `# Phase 1: API Key Authentication & Authorization`
        *   `access_by_lua_file /etc/nginx/lua/api_key_validator.lua;`
        *   `# api_key_validator.lua should populate ngx.var.api_key_id and ngx.var.api_key_tier`

        *   `# Phase 2: Rate Limiting based on API Key Tier`
        *   `# Define map in http block or 03-rate_limiting_policies.conf`
        *   `map $api_key_tier $developer_api_rate_limit_zone {`
        *   `  default       per_ip_general; # Fallback if no valid tier`
        *   `  "free"        per_api_key_free;`
        *   `  "pro"         per_api_key_pro;`
        *   `  "enterprise"  per_api_key_enterprise;`
        *   `}`
        *   `limit_req zone=$developer_api_rate_limit_zone burst=5 nodelay; # burst value adjusted per tier logic`

        *   `# Phase 3: Proxying to Upstream`
        *   `proxy_set_header Host $host;`
        *   `proxy_set_header X-Real-IP $remote_addr;`
        *   `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
        *   `proxy_set_header X-Forwarded-Proto $scheme;`
        *   `proxy_set_header X-Client-ID $api_key_client_id; # Set by api_key_validator.lua`
        *   `proxy_pass http://developer_api_platform_service/creations/;`
    *   `}`
*   **Logic Flow:**
    1.  Matches developer API paths.
    2.  Invokes `api_key_validator.lua` to validate the API key (typically from `X-API-Key` header).
    3.  The Lua script sets Nginx variables like `$api_key_id` and `$api_key_tier`.
    4.  Applies rate limiting using a zone determined by the `$api_key_tier` via the `map` directive.
    5.  Proxies the request to the `developer_api_platform_service` upstream, passing client identity information.
*   **Requirements Addressed:** REQ-017, REQ-018, SEC-001 (API Key Auth), SEC-005 (Rate limiting).

### 3.9. Lua Scripts (`lua/*.lua`)

#### 3.9.1. `lua/jwt_validator.lua`

*   **Purpose:** Validates JWT tokens found in the `Authorization` header for protected API endpoints.
*   **Key Functions:**
    *   `function M.authenticate()`
        *   **Input:** None (reads from `ngx.req.get_headers()`).
        *   **Output:** None (exits with error on failure, or allows request to proceed).
        *   **Logic:**
            1.  Retrieve `Authorization` header.
            2.  Check if header exists and starts with "Bearer ". Extract token. If not, `ngx.exit(ngx.HTTP_UNAUTHORIZED)`.
            3.  Load JWT library (e.g., `local jwt = require "resty.jwt"`).
            4.  Define JWT validation options (algorithms, issuer, audience). These should be configurable via environment variables (e.g., `JWT_ISSUER`, `JWT_AUDIENCE`).
            5.  Get JWT secret or public key:
                *   Symmetric (HS256): `local secret = os.getenv("JWT_SECRET_KEY")`.
                *   Asymmetric (RS256, ES256):
                    *   `local jwks_uri = os.getenv("JWKS_URI")`.
                    *   Fetch JWKS from `jwks_uri` using `lua-resty-http` (cached using `ngx.shared.dict` for performance, with a TTL).
                    *   Find the correct key from JWKS based on `kid` in JWT header.
            6.  Verify token: `local ok, err_or_claims = jwt:verify(secret_or_jwk, token_string, jwt_options)`.
            7.  If `not ok` or claims are invalid (e.g., expired):
                *   `ngx.log(ngx.ERR, "JWT validation failed: ", err_or_claims)`
                *   `ngx.header["WWW-Authenticate"] = 'Bearer realm="CreativeFlow AI", error="invalid_token", error_description="' .. tostring(err_or_claims) .. '"'`
                *   `return ngx.exit(ngx.HTTP_UNAUTHORIZED)`
            8.  If valid:
                *   `ngx.var.jwt_subject = err_or_claims.sub` (or other claims as needed for logging/upstream).
                *   `ngx.var.jwt_user_id = err_or_claims.user_id`
                *   `ngx.var.jwt_user_roles = table.concat(err_or_claims.roles or {}, ",")`
                *   `ngx.var.jwt_user_tier = err_or_claims.tier`
                *   Optionally store full claims in `ngx.ctx.jwt_claims = err_or_claims`.
        *   **Error Handling:** Logs errors, returns `401 Unauthorized` with `WWW-Authenticate` header.
*   **Required Libraries:** `resty.jwt`, `resty.http` (for JWKS), `cjson`, `ngx.shared.dict` (for JWKS caching).
*   **Configuration:** Environment variables for `JWT_SECRET_KEY` (if symmetric), `JWKS_URI` (if asymmetric), `JWT_ISSUER`, `JWT_AUDIENCE`.
*   **Security:** Crucial for protecting APIs. Key management for secrets/JWKS URI is vital.
*   **Requirements Addressed:** SEC-001 (Auth enforcement).

#### 3.9.2. `lua/api_key_validator.lua`

*   **Purpose:** Validates API keys provided in the `X-API-Key` header for developer API access.
*   **Key Functions:**
    *   `function M.authenticate()`
        *   **Input:** None (reads `X-API-Key` from `ngx.req.get_headers()`).
        *   **Output:** None (exits with error on failure, or allows request).
        *   **Logic:**
            1.  Retrieve `X-API-Key` header. If missing, `ngx.exit(ngx.HTTP_UNAUTHORIZED)`.
            2.  `local api_key = ngx.req.get_headers()["X-API-Key"]`.
            3.  Validation Strategy:
                *   **Simple (toggle `ENABLE_COMPLEX_API_KEY_LUA_VALIDATION` is false):**
                    *   Load valid API keys and their tiers/client IDs from a shared dictionary (`ngx.shared.dict.api_keys`) or a file (reloaded periodically).
                    *   `local key_info = ngx.shared.dict.api_keys:get(api_key)`.
                    *   If `key_info` is nil or invalid, `ngx.exit(ngx.HTTP_UNAUTHORIZED)`.
                    *   `key_info` should be a JSON string like `{"client_id": "...", "tier": "pro"}`.
                *   **Complex (toggle `ENABLE_COMPLEX_API_KEY_LUA_VALIDATION` is true):**
                    *   Make an HTTP subrequest to an internal API key validation service (e.g., Auth service endpoint `/internal/validate-api-key`).
                    *   `local http = require "resty.http"`
                    *   `local httpc = http.new()`
                    *   `local res, err = httpc:request_uri(os.getenv("API_KEY_VALIDATION_ENDPOINT"), { method = "POST", body = cjson.encode({api_key = api_key}), headers = { ["Content-Type"] = "application/json" } })`
                    *   If `err` or `res.status >= 400`, log error and `ngx.exit(ngx.HTTP_UNAUTHORIZED)` or `ngx.HTTP_INTERNAL_SERVER_ERROR`.
                    *   Parse `res.body` for `key_info` (client ID, tier, permissions).
                    *   Cache validation results in `ngx.shared.dict.api_key_cache` with a TTL to reduce load on the validation service.
            4.  If API key is valid:
                *   `ngx.var.api_key_id = key_info.client_id` (or a hash of the key itself for logging).
                *   `ngx.var.api_key_tier = key_info.tier`.
                *   `ngx.var.api_key_client_id = key_info.client_id`.
                *   Optionally set other headers based on `key_info.permissions`.
        *   **Error Handling:** Logs errors, returns `401 Unauthorized` or `403 Forbidden`.
*   **Required Libraries:** `cjson`, `resty.http` (for complex validation), `ngx.shared.dict` (for caching/simple list).
*   **Configuration:** Environment variables for `API_KEY_VALIDATION_ENDPOINT` (if complex), `ENABLE_COMPLEX_API_KEY_LUA_VALIDATION`. Shared dictionary configuration in `nginx.conf` (e.g., `lua_shared_dict api_keys 10m; lua_shared_dict api_key_cache 5m;`).
*   **Security:** Protects developer APIs. Secure communication with validation service if used.
*   **Requirements Addressed:** SEC-001, REQ-018.

#### 3.9.3. `lua/input_validator.lua` (Optional, based on feature toggle)

*   **Purpose:** Performs advanced request payload validation against JSON schemas for specific API endpoints.
*   **Key Functions:**
    *   `function M.validate_current_request(schema_name_or_id)`
        *   **Input:** `schema_name_or_id` (string) - identifier to load the correct JSON schema.
        *   **Output:** `boolean (ok), table (errors_or_nil)`
        *   **Logic:**
            1.  Check feature toggle `os.getenv("ENABLE_ADVANCED_INPUT_VALIDATION_LUA")`. If not "true", return `true`.
            2.  `ngx.req.read_body()` must have been called prior to this script if it's in `access_by_lua_file`. If in `content_by_lua_block`, it can call it.
            3.  `local body_data = ngx.req.get_body_data()`. If no body for POST/PUT, handle appropriately (may be an error or allowed).
            4.  Parse `body_data` to a Lua table using `cjson.decode()`. Handle parse errors.
            5.  Load JSON schema:
                *   `local schema_content = load_schema_from_file_or_cache(schema_name_or_id)` (Helper function). Schemas can be stored in `/etc/nginx/lua/schemas/` and cached in `ngx.shared.dict`.
                *   `local schema_table = cjson.decode(schema_content)`.
            6.  `local jsonschema = require "jsonschema"` (or chosen library).
            7.  `local validator = jsonschema.new(schema_table)`.
            8.  `local ok, errors = validator:validate(parsed_body_lua_table)`.
            9.  Return `ok, errors`.
    *   `function load_schema_from_file_or_cache(schema_name)` (Internal helper)
        *   Loads schema from a shared dictionary cache first. If not found, reads from a file (e.g., `/etc/nginx/lua/schemas/<schema_name>.json`), caches it, and returns.
*   **Required Libraries:** `cjson`, `jsonschema` (e.g., `lua-jsonschema` by kivilahtio).
*   **Configuration:** Schemas stored as JSON files. Shared dictionary for schema caching (`lua_shared_dict json_schemas_cache 1m;`).
*   **Integration:** Called from `location` blocks using `access_by_lua_file` or `content_by_lua_block` where advanced validation is needed. The calling location block must handle the return status from `M.validate_current_request` and terminate the request with HTTP 400 if validation fails.
*   **Requirements Addressed:** SEC-005 (input validation at gateway).

### 3.10. SSL Certificate Files

#### 3.10.1. `ssl/creativeflow.ai.pem`

*   **Purpose:** The SSL/TLS public certificate chain file for `api.creativeflow.ai`.
*   **Content:** Server's public certificate concatenated with any necessary intermediate CA certificates, in PEM format.
*   **Management:** Must be obtained from a trusted Certificate Authority (CA). Regular renewal is required before expiration.
*   **Security:** While public, its integrity is vital.
*   **Requirements Addressed:** Section 5.2.2 (SSL Termination).

#### 3.10.2. `ssl/creativeflow.ai.key`

*   **Purpose:** The SSL/TLS private key corresponding to `creativeflow.ai.pem`.
*   **Content:** Server's private key in PEM format.
*   **Management:** Must be kept highly secure and confidential. File permissions should restrict access strictly to the Nginx master process user (e.g., root) and the Nginx worker process user. Regular renewal should accompany certificate renewal.
*   **Security:** Compromise of this key allows decryption of traffic.
*   **Requirements Addressed:** Section 5.2.2 (SSL Termination).

## 4. Core Functionalities Implementation Details

### 4.1. Request Routing
*   Implemented using Nginx `location` blocks matching URI patterns.
*   `proxy_pass` directive routes requests to `upstream` blocks.
*   Upstream blocks define backend service instances and load balancing strategy.
*   Relevant files: `nginx.conf` (includes), `00-main-server.conf` (server entry), `01-upstreams.conf`, `conf.d/routes/*.conf`.

### 4.2. Authentication
*   **JWT Authentication (for platform users):**
    *   Handled by `lua/jwt_validator.lua`.
    *   Expects "Bearer <token>" in `Authorization` header.
    *   Validates signature, expiration, issuer, audience.
    *   Uses public keys (via JWKS URI) or shared secret (from secure config).
    *   Sets Nginx variables (`$jwt_subject`, `$jwt_user_id`, `$jwt_user_roles`, `$jwt_user_tier`) on success for upstream services and logging.
    *   Applied in `location` blocks for protected resources.
*   **API Key Authentication (for developers):**
    *   Handled by `lua/api_key_validator.lua`.
    *   Expects API key in `X-API-Key` header.
    *   Validates key against a secure store (e.g., Redis cache populated from DB, or via subrequest to auth service if `ENABLE_COMPLEX_API_KEY_LUA_VALIDATION` is true).
    *   Sets Nginx variables (`$api_key_id`, `$api_key_tier`, `$api_key_client_id`) on success.
    *   Applied in `location` blocks for developer API routes.
*   **Requirements Addressed:** SEC-001.

### 4.3. Authorization
*   Basic authorization can be inferred from successfully validated JWT claims (roles, tier) or API key permissions (tier).
*   `jwt_validator.lua` and `api_key_validator.lua` make user roles/tier available as Nginx variables.
*   More granular authorization logic is expected to reside within the backend microservices, which will consume the user/client identity passed by the gateway.
*   The gateway's role is primarily authentication and coarse-grained checks (e.g., is this a "pro" tier user?).

### 4.4. Rate Limiting
*   Implemented using Nginx `limit_req_zone` and `limit_req` directives.
*   Zones defined in `conf.d/03-rate_limiting_policies.conf` based on IP address, API key tier (`$api_key_tier` variable), or JWT subject (`$jwt_subject` variable).
*   `limit_req` applied in specific `location` blocks with appropriate `burst` and `nodelay` parameters.
*   `limit_req_status 429;` for rate-limited responses.
*   **Dynamic Tier-Based Rate Limiting for API Keys:**
    nginx
    # In http block or 03-rate_limiting_policies.conf
    map $api_key_tier $developer_api_rate_limit_zone {
        default       per_ip_general;     # Fallback if tier not identified or key invalid
        "free"        per_api_key_free;
        "pro"         per_api_key_pro;
        "enterprise"  per_api_key_enterprise;
    }

    # In conf.d/routes/developer_api.conf location block for an endpoint
    # access_by_lua_file /etc/nginx/lua/api_key_validator.lua; # This script sets ngx.var.api_key_tier
    limit_req zone=$developer_api_rate_limit_zone burst=5 nodelay; # Example burst
    
*   **Requirements Addressed:** SEC-005, REQ-018.

### 4.5. SSL/TLS Termination
*   Handled by the main `server` block in `conf.d/00-main-server.conf`.
*   Uses `ssl_certificate`, `ssl_certificate_key`, `ssl_protocols`, `ssl_ciphers`.
*   Enforces HTTPS.
*   **Requirements Addressed:** Section 5.2.2.

### 4.6. Security Policies (Headers, CORS)
*   Configured in `conf.d/02-security_policies.conf` and included in the main server block.
*   Uses `add_header` for security headers (HSTS, X-Content-Type-Options, X-Frame-Options, CSP, etc.).
*   Manages CORS using `Access-Control-Allow-*` headers, potentially with a `map` for dynamic origin whitelisting.
*   **Requirements Addressed:** SEC-005.

### 4.7. Input Validation (Basic & Advanced)
*   **Basic:** Nginx can perform some basic validation (e.g., request method checks, path validation implicitly).
*   **Advanced (Feature Toggled):** `lua/input_validator.lua` can be used for JSON schema validation of request bodies for specific POST/PUT endpoints if `ENABLE_ADVANCED_INPUT_VALIDATION_LUA` is true and the location block is configured to call it.
*   **Requirements Addressed:** SEC-005.

### 4.8. Health Checks
*   A simple `/health` endpoint is defined in `conf.d/10-health_check.conf` for gateway liveness checks.
*   Upstream health checks are passive by default (`max_fails`, `fail_timeout` in `upstream` blocks). Active health checks require Nginx Plus or custom Lua scripting.

### 4.9. Logging
*   Global access and error logs defined in `nginx.conf`.
*   Custom log format `main_ext` includes request time, upstream response time, upstream address, cache status, and variables set by Lua scripts (e.g., `$jwt_subject`, `$api_key_id`) for better traceability.
*   Lua scripts should use `ngx.log(ngx.ERR, "message")` for detailed error logging.

## 5. Configuration Management

*   All Nginx `.conf` files and Lua `.lua` scripts will be version-controlled in Git.
*   Sensitive information (SSL private keys, JWT secrets, API key validation service credentials) MUST NOT be stored in Git.
    *   SSL keys will be securely deployed to the server.
    *   Lua scripts will retrieve secrets from environment variables (e.g., `os.getenv("JWT_SECRET_KEY")`) or from files mounted from a secure secrets management system (e.g., HashiCorp Vault) at runtime. Nginx environment variables can be set in the Nginx service unit or Docker entrypoint.
*   Infrastructure as Code (Ansible) will be used to deploy and manage Nginx configurations and Lua scripts, ensuring consistency across environments (as per PMDT-011, PMDT-012). Ansible will manage the placement of SSL files and setting of environment variables for Nginx/OpenResty.

## 6. Deployment Considerations

*   The API Gateway will be deployed on dedicated Linux servers (Ubuntu 22.04 LTS) running OpenResty.
*   Deployment will be automated using Ansible through the CI/CD pipeline.
*   High availability will be achieved by deploying multiple instances of the API Gateway behind a load balancer (though Nginx itself can also act as a software load balancer for its own instances if needed, this usually refers to an external LB). The upstreams configuration handles backend HA.
*   Configuration reloads (`nginx -s reload`) should be used for applying changes with zero downtime.
*   Monitoring of Nginx/OpenResty metrics (connections, request rates, error rates, Lua context switches, shared dictionary usage) via Prometheus (e.g., using `nginx-lua-prometheus` or `nginx-vts-exporter`).

## 7. Lua Script Environment and Dependencies

*   Lua scripts will execute within the OpenResty Nginx worker processes using LuaJIT.
*   **Shared Dictionaries:** Configure necessary shared dictionaries in `nginx.conf` `http` block:
    nginx
    http {
        # ... other http configs ...
        lua_shared_dict jwt_jwks_cache 10m;      # For caching JWKS
        lua_shared_dict api_keys_static 5m;    # For simple API key list if used
        lua_shared_dict api_key_validation_cache 5m; # For caching results from complex API key validation
        lua_shared_dict json_schemas_cache 1m; # For caching JSON schemas for input validation

        # ... include conf.d ...
    }
    
*   **Lua Package Path:** Ensure `lua_package_path` and `lua_package_cpath` in `nginx.conf` are correctly set to include paths for `lua-resty-*` libraries and custom Lua modules. Typically, OpenResty handles this by default for its bundled libraries.
    nginx
    # In http block of nginx.conf
    # Default OpenResty paths usually work, but can be explicit if needed
    # lua_package_path "/usr/local/openresty/lualib/?.lua;;";
    # lua_package_cpath "/usr/local/openresty/lualib/?.so;;";
    

## 8. Error Handling Strategy

*   **Nginx Level:**
    *   Default error pages for 4xx and 5xx errors (e.g., `error_page 404 /404.html;`). For APIs, JSON responses are preferred:
        nginx
        error_page 401 /errors/401.json;
        error_page 403 /errors/403.json;
        error_page 404 /errors/404.json;
        error_page 429 /errors/429.json;
        error_page 500 502 503 504 /errors/50x.json;

        location /errors/ {
            internal;
            root /usr/share/nginx/html; # Path to static JSON error files
            default_type application/json;
        }
        # Example 401.json: { "error": "Unauthorized", "message": "Authentication required." }
        
    *   Specific error handling for rate limiting (`limit_req_status 429`).
*   **Lua Script Level:**
    *   Scripts performing validation (JWT, API key, input) should return appropriate HTTP status codes upon failure (e.g., `ngx.exit(ngx.HTTP_UNAUTHORIZED)`, `ngx.exit(ngx.HTTP_BAD_REQUEST)`).
    *   Log detailed error information using `ngx.log(ngx.ERR, ...)`.
    *   For JSON APIs, Lua scripts should construct a JSON error response body if exiting.
    lua
    -- Example in Lua for error
    ngx.status = ngx.HTTP_BAD_REQUEST
    local cjson = require "cjson.safe"
    ngx.header.content_type = "application/json; charset=utf-8"
    ngx.say(cjson.encode({ error = "validation_failed", messages = validation_errors }))
    return ngx.exit(ngx.status)
    
*   **Upstream Errors:** Nginx `proxy_next_upstream` directive can be configured to retry requests on certain errors from upstream services. Custom error pages can be served if all upstreams fail.

This Software Design Specification provides a comprehensive guide for the development and configuration of the CreativeFlow.ApiGateway. It details the structure, logic, and integration points necessary to fulfill its role as a secure, reliable, and performant entry point to the platform's microservices.