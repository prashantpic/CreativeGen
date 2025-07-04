# Specification

# 1. Files

- **Path:** nginx.conf  
**Description:** Main Nginx configuration file. Sets global worker processes, events, and includes the primary HTTP configuration block. This file is the entry point for the Nginx server.  
**Template:** Nginx Configuration  
**Dependency Level:** 4  
**Name:** nginx  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Nginx Server Initialization
    
**Requirement Ids:**
    
    
**Purpose:** To bootstrap the Nginx server process and include all other necessary configuration files for the API Gateway and Load Balancer.  
**Logic Description:** Defines global settings like `user`, `worker_processes`, and the `events` block. Contains the main `http` block which sets up logging formats, gzip settings, and includes `mime.types` and the `conf.d/*.conf` files to load the actual server configurations.  
**Documentation:**
    
    - **Summary:** The root configuration file for the Nginx instance, responsible for loading all subsequent configurations and defining global server behavior.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** mime.types  
**Description:** Standard Nginx MIME type mapping file. Maps file extensions to MIME types to ensure the browser correctly interprets content.  
**Template:** Nginx Configuration  
**Dependency Level:** 0  
**Name:** mime  
**Type:** Configuration  
**Relative Path:** .  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Type Mapping
    
**Requirement Ids:**
    
    
**Purpose:** To provide a standard mapping of file extensions to their corresponding MIME types, used by Nginx to set the `Content-Type` header.  
**Logic Description:** Contains a list of key-value pairs where the key is the MIME type and the value is a space-separated list of file extensions. This file is included by `nginx.conf`.  
**Documentation:**
    
    - **Summary:** A standard Nginx helper file for MIME type definitions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/gateway.conf  
**Description:** The primary server block configuration for the API Gateway. Defines listen ports, SSL settings, server names, and includes all routing, policy, and upstream configurations.  
**Template:** Nginx Configuration  
**Dependency Level:** 3  
**Name:** gateway  
**Type:** Configuration  
**Relative Path:** conf.d/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Gateway Server Definition
    - SSL Termination
    - Request Routing Facade
    
**Requirement Ids:**
    
    - Section 5.1 (API Gateway Role)
    - Section 5.2.2 (API Gateway Component)
    
**Purpose:** To define the main virtual server that acts as the API Gateway, handling all incoming client traffic and applying global policies before routing.  
**Logic Description:** Defines a `server` block listening on ports 80 and 443. Port 80 redirects to 443. The 443 server block configures SSL certificates, security headers, CORS policies, and rate limiting zones. It will then `include` all specific route configuration files from the `/etc/nginx/locations` directory. This file also defines the upstream blocks for load balancing by including files from `/etc/nginx/upstreams`.  
**Documentation:**
    
    - **Summary:** Configures the primary server block for the API Gateway, including SSL termination and inclusion of all routing and policy files.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** upstreams/auth_service.conf  
**Description:** Defines the upstream server group for the Authentication & Authorization Service.  
**Template:** Nginx Configuration  
**Dependency Level:** 1  
**Name:** auth_service  
**Type:** Configuration  
**Relative Path:** upstreams/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    - LoadBalancer
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - Section 5.2.2 (API Gateway Component)
    
**Purpose:** To define a named group of backend servers for the authentication service, allowing for load balancing and health checks.  
**Logic Description:** Contains an `upstream auth_service { ... }` block. Inside, it lists the `server` directives with the IP addresses or hostnames and ports of the authentication service instances. It specifies a load balancing method (e.g., `least_conn`) and health check parameters.  
**Documentation:**
    
    - **Summary:** Upstream configuration for the authentication service microservice.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** upstreams/user_management_service.conf  
**Description:** Defines the upstream server group for the User Account & Profile Service.  
**Template:** Nginx Configuration  
**Dependency Level:** 1  
**Name:** user_management_service  
**Type:** Configuration  
**Relative Path:** upstreams/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    - LoadBalancer
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - Section 5.2.2 (API Gateway Component)
    
**Purpose:** To define a named group of backend servers for the user management service, allowing for load balancing and health checks.  
**Logic Description:** Contains an `upstream user_management_service { ... }` block listing the `server` directives for the user management service instances.  
**Documentation:**
    
    - **Summary:** Upstream configuration for the user management microservice.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** upstreams/creative_management_service.conf  
**Description:** Defines the upstream server group for the Creative Management Service (handles projects, assets, etc.).  
**Template:** Nginx Configuration  
**Dependency Level:** 1  
**Name:** creative_management_service  
**Type:** Configuration  
**Relative Path:** upstreams/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    - LoadBalancer
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Discovery
    - Load Balancing
    
**Requirement Ids:**
    
    - Section 5.2.2 (API Gateway Component)
    
**Purpose:** To define a named group of backend servers for the creative management service, allowing for load balancing and health checks.  
**Logic Description:** Contains an `upstream creative_management_service { ... }` block listing the `server` directives for the creative management service instances.  
**Documentation:**
    
    - **Summary:** Upstream configuration for the creative management microservice.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** policies/ratelimit.conf  
**Description:** Defines rate limiting zones and policies.  
**Template:** Nginx Configuration  
**Dependency Level:** 1  
**Name:** ratelimit  
**Type:** Configuration  
**Relative Path:** policies/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - API Rate Limiting
    
**Requirement Ids:**
    
    - REQ-018 (Rate limiting at gateway)
    - SEC-005 (API Protection)
    
**Purpose:** To configure different rate limiting schemes that can be applied to various API routes based on user type or API usage context.  
**Logic Description:** Contains multiple `limit_req_zone` directives. Each zone defines a shared memory area, a key (e.g., `$binary_remote_addr`, `$http_api_key`, or a custom map variable based on JWT claims), and a rate (e.g., `10r/s`). Defines zones for anonymous users, authenticated users, and different API tiers.  
**Documentation:**
    
    - **Summary:** Central configuration for all API rate limiting zones, implementing Nginx's `limit_req` module settings.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** policies/security.conf  
**Description:** Defines common security headers and CORS policy.  
**Template:** Nginx Configuration  
**Dependency Level:** 1  
**Name:** security  
**Type:** Configuration  
**Relative Path:** policies/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - CORS Policy Enforcement
    - Security Header Implementation
    
**Requirement Ids:**
    
    - SEC-005 (API Protection)
    
**Purpose:** To centralize the configuration of essential security headers and Cross-Origin Resource Sharing (CORS) policies to be applied globally or per-route.  
**Logic Description:** Contains `add_header` directives for security headers like `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, and `Content-Security-Policy`. Also includes a `map` or `if` blocks to handle CORS preflight (`OPTIONS`) requests and add `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, and `Access-Control-Allow-Headers` headers for regular requests.  
**Documentation:**
    
    - **Summary:** A consolidated configuration file for applying crucial HTTP security headers and CORS policies.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** locations/auth.conf  
**Description:** Routing configuration for all authentication and user-related public endpoints.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** auth  
**Type:** Configuration  
**Relative Path:** locations/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Auth Service Routing
    
**Requirement Ids:**
    
    - REQ-017 (API Coverage implies Gateway)
    
**Purpose:** To proxy requests for endpoints like /auth/login, /auth/register, /api/v1/users/** to the appropriate backend services.  
**Logic Description:** Contains `location` blocks for paths like `/auth/` and `/api/v1/users/`. Inside these blocks, it uses `proxy_pass http://auth_service;` and `proxy_pass http://user_management_service;` to route requests. It applies specific policies, such as stricter rate limits for login attempts.  
**Documentation:**
    
    - **Summary:** Defines Nginx location blocks to route authentication and user management traffic to the correct upstream services.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** locations/api.conf  
**Description:** Main routing configuration for protected v1 API endpoints. Enforces JWT authentication.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** api  
**Type:** Configuration  
**Relative Path:** locations/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    - APIGateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - JWT Authentication Enforcement
    - API Key Validation
    - Protected API Routing
    
**Requirement Ids:**
    
    - SEC-001 (Auth enforcement at gateway)
    - REQ-017 (API Coverage implies Gateway)
    
**Purpose:** To define the primary `location /api/v1/` block, which acts as a parent for all protected API calls, enforcing authentication before proxying.  
**Logic Description:** Contains a `location /api/v1/ { ... }` block. This block is critical for security. It will contain the `auth_jwt` directive (if using ngx_http_auth_jwt_module) or the `access_by_lua_file` directive pointing to `lua/auth.lua`. It validates the JWT or API Key. If validation succeeds, it proxies the request to the relevant upstream service based on further nested location matches (e.g., for creatives, billing). If validation fails, it returns a 401 Unauthorized error.  
**Documentation:**
    
    - **Summary:** Configures the main protected API location, responsible for invoking JWT or API key authentication for all v1 API requests.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** lua/auth.lua  
**Description:** (If using OpenResty) Lua script for advanced JWT and API Key validation.  
**Template:** Lua Script  
**Dependency Level:** 1  
**Name:** auth  
**Type:** Script  
**Relative Path:** lua/  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - JWT Validation Logic
    - API Key Validation Logic
    - Dynamic Policy Application
    
**Requirement Ids:**
    
    - SEC-001 (Auth enforcement at gateway)
    - SEC-005 (API Protection)
    
**Purpose:** To provide flexible and robust authentication logic that standard Nginx modules may not offer, such as fetching JWKS, caching keys, and validating custom claims.  
**Logic Description:** The script extracts the token from the `Authorization` header or the API key from a header like `X-API-Key`. For JWTs, it fetches the public keys from the auth service's JWKS endpoint (with caching), verifies the token's signature, issuer, and audience. For API keys, it might call an internal service to validate the key and retrieve its permissions. If successful, it can set Nginx variables (e.g., `$user_id`, `$user_tier`) to be used in upstream headers or rate limiting keys. If invalid, it exits with a 401 or 403 status.  
**Documentation:**
    
    - **Summary:** A Lua script for OpenResty that handles the logic for authenticating requests via JWT or API Keys, including JWKS fetching and caching.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** Dockerfile  
**Description:** Dockerfile for building a container image of the Nginx API Gateway.  
**Template:** Dockerfile  
**Dependency Level:** 5  
**Name:** Dockerfile  
**Type:** Build  
**Relative Path:** .  
**Repository Id:** REPO-APIGATEWAY-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Containerization
    
**Requirement Ids:**
    
    
**Purpose:** To create a self-contained, portable, and reproducible Docker image for the Nginx API Gateway.  
**Logic Description:** Starts from a base Nginx or OpenResty image. Copies all the custom configuration files (`nginx.conf`, `conf.d/`, `upstreams/`, `locations/`, `policies/`), Lua scripts (`lua/`), and SSL certificates into the appropriate directories within the image. Exposes ports 80 and 443. The `CMD` instruction starts the Nginx server in the foreground.  
**Documentation:**
    
    - **Summary:** Defines the steps to build a Docker container for the API gateway, packaging Nginx with all necessary custom configurations and scripts.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Build
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - EnableAdvancedLuaAuth
  - EnforceStrictCSP
  
- **Database Configs:**
  
  


---

