-- File: /etc/nginx/lua/auth_jwt.lua
-- Purpose: Validates a JWT Bearer token from the Authorization header.
-- If the token is valid, it extracts user claims and adds them as
-- request headers for the upstream service.
-- Based on SDS Section 3.2.1.

local jwt = require "resty.jwt"
local cjson = require "cjson.safe"

-- Helper function to terminate request with a standardized JSON error response.
local function exit_with_error(status, error_code, message)
    ngx.status = status
    ngx.header["Content-Type"] = "application/json; charset=utf-8"
    ngx.say(cjson.encode({ status = status, error = error_code, message = message }))
    return ngx.exit(status)
end

-- 1. Extract token from Authorization: Bearer <token> header.
local auth_header = ngx.var.http_Authorization
if not auth_header then
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "UNAUTHORIZED", "Authorization header missing.")
end

local _, _, token = string.find(auth_header, "^[Bb]earer%s+(.+)$")
if not token then
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "UNAUTHORIZED", "Bearer token missing or malformed.")
end

-- 2. Get the JWT secret from an environment variable for security.
local jwt_secret = os.getenv("JWT_SECRET")
if not jwt_secret or jwt_secret == "" then
    ngx.log(ngx.ERR, "FATAL: JWT_SECRET environment variable not set.")
    return exit_with_error(ngx.HTTP_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", "Server configuration error.")
end

-- 3. Verify the token. `resty.jwt` automatically validates the signature,
--    expiration (exp), and not-before (nbf) claims.
--    Use a pcall to safely handle potential errors from the library.
local ok, jwt_obj = pcall(jwt.verify, jwt, jwt_secret, token)

if not ok or not jwt_obj.verified then
    local reason = "Invalid token"
    if jwt_obj and jwt_obj.reason then
       reason = jwt_obj.reason
    elseif not ok then
       reason = jwt_obj -- error message from pcall
    end
    ngx.log(ngx.INFO, "JWT verification failed: ", reason)
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "INVALID_TOKEN", reason)
end

-- 4. Verify custom claims: issuer (iss) and audience (aud).
local payload = jwt_obj.payload
local expected_issuer = "CreativeFlow.Auth"
local expected_audience = "CreativeFlow.Api"

if payload.iss ~= expected_issuer then
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "INVALID_TOKEN", "Invalid token issuer.")
end

if payload.aud ~= expected_audience then
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "INVALID_TOKEN", "Invalid token audience.")
end

-- 5. If valid, forward user claims as request headers to the upstream service.
--    This allows backend services to trust the user's identity.
if payload.sub then
    ngx.req.set_header("X-User-ID", payload.sub)
else
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "INVALID_TOKEN", "Token is missing user identifier (sub).")
end

if payload.roles and type(payload.roles) == "table" then
    ngx.req.set_header("X-User-Roles", table.concat(payload.roles, ","))
end

-- If all checks pass, the request is allowed to proceed.