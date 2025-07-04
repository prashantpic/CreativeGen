# Specification

# 1. Files

- **Path:** nginx.conf  
**Description:** Main Nginx configuration file. This is the entry point for the gateway. It sets global parameters like worker processes, error log paths, and includes the primary server configuration from the conf.d directory.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** nginx.conf  
**Type:** Configuration  
**Relative Path:**   
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Gateway Bootstrap
    
**Requirement Ids:**
    
    - Section 5.1
    
**Purpose:** To bootstrap the Nginx server process and load all subsequent configurations for the API Gateway.  
**Logic Description:** Defines global settings such as user, worker_processes, and error_log. Includes an http block that sets basic HTTP parameters (e.g., sendfile, tcp_nopush). Crucially, it uses an 'include' directive to load all .conf files from the /etc/nginx/conf.d/ directory, which orchestrates the loading of the entire gateway configuration.  
**Documentation:**
    
    - **Summary:** Top-level Nginx configuration file. It sets up the main server process and includes all virtual host and upstream configurations from the 'conf.d' directory. It is the root of the gateway's configuration tree.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/00-upstreams.conf  
**Description:** Defines all upstream backend service clusters. This file centralizes the definitions of microservice endpoints, allowing for easy updates and management of backend server pools and load balancing strategies.  
**Template:** Nginx Configuration  
**Dependency Level:** 0  
**Name:** 00-upstreams.conf  
**Type:** Configuration  
**Relative Path:** conf.d/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Load Balancing
    - Service Discovery (Static)
    
**Requirement Ids:**
    
    - NFR-005
    
**Purpose:** To declare backend microservice pools for load balancing and routing, abstracting the service locations from the routing logic.  
**Logic Description:** Contains multiple 'upstream' blocks, one for each backend microservice (e.g., auth_service, odoo_service, creative_service). Each block lists the server addresses (IP:port or hostname:port) of the instances for that service. Specifies the load balancing algorithm (e.g., least_conn, round_robin) and server options like weight or max_fails.  
**Documentation:**
    
    - **Summary:** Central configuration for all backend service endpoints. This file defines named groups of servers (upstreams) that the gateway will proxy requests to, along with the load balancing method for each group.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/01-policies.conf  
**Description:** Defines reusable policy blocks, such as rate limiting zones and CORS headers. This allows for consistent application of cross-cutting policies across different API routes.  
**Template:** Nginx Configuration  
**Dependency Level:** 1  
**Name:** 01-policies.conf  
**Type:** Configuration  
**Relative Path:** conf.d/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Rate Limiting Policy Definition
    - CORS Policy Definition
    
**Requirement Ids:**
    
    - SEC-005
    
**Purpose:** To centralize the definition of security and traffic management policies for reuse across the gateway.  
**Logic Description:** Defines 'limit_req_zone' blocks to set up rate limiting based on variables like client IP address or API key. It may also contain 'map' blocks or 'add_header' directives for defining and applying common Cross-Origin Resource Sharing (CORS) headers.  
**Documentation:**
    
    - **Summary:** Contains reusable policy definitions for the API Gateway. This includes setting up rate limiting zones and defining standard CORS headers that can be applied to various locations or server blocks.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/10-gateway.conf  
**Description:** The main virtual server configuration file for the API Gateway. It defines the primary server block, listens on ports 80 and 443, handles SSL termination, and includes all specific route configurations.  
**Template:** Nginx Configuration  
**Dependency Level:** 3  
**Name:** 10-gateway.conf  
**Type:** Configuration  
**Relative Path:** conf.d/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - SSL Termination
    - Request Routing Orchestration
    - Default Error Handling
    
**Requirement Ids:**
    
    - Section 5.2.2
    - NFR-005
    
**Purpose:** To configure the primary virtual host that listens for incoming traffic and acts as the main router for the API Gateway.  
**Logic Description:** Defines a 'server' block listening on port 443 (SSL) and potentially port 80 (redirecting to 443). Specifies SSL certificate paths, protocols, and ciphers. Sets default server-wide parameters like logging formats and timeouts. Uses 'include' directives to pull in all route definition files from the 'routes/' subdirectory, applying them within this server context. Sets up a default catch-all location to return a 404 for undefined paths.  
**Documentation:**
    
    - **Summary:** This is the core server configuration for the gateway. It handles SSL termination, sets default request handling parameters, and includes all the individual route files to build the complete routing table.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/routes/auth.conf  
**Description:** Configuration file containing all routing rules (location blocks) for the Authentication and User Management services.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** auth.conf  
**Type:** Configuration  
**Relative Path:** conf.d/routes/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Authentication Service Routing
    
**Requirement Ids:**
    
    - Section 5.2.2
    
**Purpose:** To route all authentication-related API requests, such as login, register, and token refresh, to the appropriate backend authentication service.  
**Logic Description:** Contains 'location' blocks for paths like '/api/v1/auth/', '/api/v1/users/', and '/api/v1/profiles/'. Each block uses 'proxy_pass' to forward requests to the 'auth_service' upstream defined in '00-upstreams.conf'. It may apply specific, lenient rate limits for login endpoints to prevent brute-forcing.  
**Documentation:**
    
    - **Summary:** Defines the routing rules for all user authentication, authorization, and profile management endpoints. It maps public API paths to the internal authentication microservice.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/routes/api_platform.conf  
**Description:** Routing rules for the external-facing Developer API platform. Handles API key authentication and applies stricter rate limits suitable for third-party developers.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** api_platform.conf  
**Type:** Configuration  
**Relative Path:** conf.d/routes/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Developer API Routing
    - API Key Authentication Logic
    
**Requirement Ids:**
    
    - SEC-001
    - SEC-005
    
**Purpose:** To manage and secure traffic for the public-facing developer API, distinct from the primary web/mobile app traffic.  
**Logic Description:** Defines 'location' blocks for public API endpoints, like '/public-api/v1/'. These blocks will invoke the 'auth_apikey.lua' script to perform authentication. It applies specific rate limits defined in '01-policies.conf' that are tailored for API key usage. Uses 'proxy_pass' to forward valid requests to the 'api_developer_service' upstream.  
**Documentation:**
    
    - **Summary:** Contains all routing, authentication, and policy enforcement configurations for the third-party developer API. It handles API key validation and applies specific rate limits.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/routes/creative_services.conf  
**Description:** Routing rules for all creative and AI generation workflows. These routes are protected and require JWT authentication.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** creative_services.conf  
**Type:** Configuration  
**Relative Path:** conf.d/routes/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Creative Workflow Routing
    - JWT Authentication Logic
    
**Requirement Ids:**
    
    - SEC-001
    - Section 5.2.2
    
**Purpose:** To route authenticated requests for creative generation, project management, and asset management to their respective backend services.  
**Logic Description:** Defines 'location' blocks for core application functions like '/api/v1/generate/', '/api/v1/projects/', and '/api/v1/workbenches/'. Each block invokes the 'auth_jwt.lua' script for JWT validation. Upon successful authentication, it uses 'proxy_pass' to route requests to the appropriate upstream (e.g., 'aigeneration_service', 'creative_management_service').  
**Documentation:**
    
    - **Summary:** Defines routing for all core creative functionalities of the platform. This configuration ensures that only authenticated users can access these services by enforcing JWT validation.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** conf.d/routes/realtime_services.conf  
**Description:** Configuration for handling real-time communication via WebSockets, routing traffic to the Notification and Collaboration services.  
**Template:** Nginx Configuration  
**Dependency Level:** 2  
**Name:** realtime_services.conf  
**Type:** Configuration  
**Relative Path:** conf.d/routes/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - WebSocket Proxying
    
**Requirement Ids:**
    
    - Section 5.2.2
    
**Purpose:** To correctly proxy WebSocket connections for real-time features, ensuring persistent connections are established with the backend services.  
**Logic Description:** Contains 'location' blocks for WebSocket endpoints, such as '/ws/notifications/' and '/ws/collaboration/'. These blocks include specific 'proxy_set_header' directives (e.g., for 'Upgrade' and 'Connection') and 'proxy_http_version 1.1' to enable the WebSocket protocol upgrade. Requests are proxied to the 'notification_service' and 'collaboration_service' upstreams.  
**Documentation:**
    
    - **Summary:** Handles the special configuration required to proxy WebSocket connections to the real-time backend services, enabling features like live notifications and collaborative editing.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** lua/auth_jwt.lua  
**Description:** Lua script for OpenResty (Nginx) to perform JWT validation. This script is invoked by location blocks that require user authentication.  
**Template:** Lua Script  
**Dependency Level:** 1  
**Name:** auth_jwt.lua  
**Type:** Middleware  
**Relative Path:** lua/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** handler  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - JWT Validation
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** To provide a reusable and performant mechanism for validating JWTs at the gateway edge, before requests are passed to upstream services.  
**Logic Description:** The script extracts the JWT from the 'Authorization: Bearer' header. It uses a Lua JWT library to decode and verify the token's signature against a configured secret or by fetching public keys from a JWKS endpoint. It checks standard claims like 'exp' (expiration) and 'iss' (issuer). If validation fails, it aborts the request with a 401 or 403 status code. If successful, it allows the request to proceed and can optionally add user claims (e.g., user_id, roles) as new request headers for upstream services.  
**Documentation:**
    
    - **Summary:** A custom Lua script for validating JSON Web Tokens. It checks the token's signature, expiration, and other claims, and either rejects the request or allows it to pass to the backend.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    
- **Path:** lua/auth_apikey.lua  
**Description:** Lua script for OpenResty (Nginx) to validate third-party developer API keys. Invoked by location blocks dedicated to the external API.  
**Template:** Lua Script  
**Dependency Level:** 1  
**Name:** auth_apikey.lua  
**Type:** Middleware  
**Relative Path:** lua/  
**Repository Id:** REPO-GATEWAY-API-001  
**Pattern Ids:**
    
    - API Gateway
    
**Members:**
    
    
**Methods:**
    
    - **Name:** handler  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - API Key Validation
    
**Requirement Ids:**
    
    - SEC-001
    
**Purpose:** To secure the public-facing API by authenticating requests using API keys before they reach the backend API Platform service.  
**Logic Description:** This script extracts an API key from a request header (e.g., 'X-API-Key'). It then needs to validate this key. This could involve a subrequest to an internal authentication service endpoint or a direct lookup in a shared cache like Redis. Based on the validation response, it will either reject the request with a 401/403 error or allow it to proceed. It can also be used to fetch rate-limiting parameters associated with the key.  
**Documentation:**
    
    - **Summary:** A custom Lua script for validating developer API keys. It extracts the key from the request and checks its validity against a backend system or cache before proxying the request.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Security
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

