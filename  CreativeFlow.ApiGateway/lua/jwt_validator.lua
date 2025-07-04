--
-- CreativeFlow: API Gateway - JWT Validator Script
--
-- Description: This Lua script is executed by Nginx for every request to a protected
-- endpoint. It validates the JWT provided in the 'Authorization' header.
--
-- Dependencies: lua-resty-jwt (https://github.com/SkyLothar/lua-resty-jwt)
--               Install via OPM: `opm get SkyLothar/lua-resty-jwt`
--

-- Load the JWT library
local jwt = require "resty.jwt"
local cjson = require "cjson"

-- --- Configuration ---
-- In a real environment, the secret should be fetched securely, e.g., from an environment
-- variable or a secrets management service. For asymmetric keys (RS256), you would
-- fetch and cache the JWKS (JSON Web Key Set) from your authorization server.
local jwt_secret = os.getenv("JWT_SECRET_KEY") or "your-default-super-secret-key-for-testing"

-- --- Helper function to send an error response ---
local function exit_with_error(status_code, error_message, error_type)
    ngx.status = status_code
    ngx.header['Content-Type'] = 'application/json; charset=utf-8'
    ngx.say(cjson.encode({
        error = error_type,
        detail = error_message
    }))
    return ngx.exit(ngx.HTTP_UNAUTHORIZED) -- Use 401 for consistency
end

-- 1. Extract the token from the 'Authorization' header
local auth_header = ngx.var.http_authorization
if not auth_header then
    return exit_with_error(401, "Authorization header missing", "authentication_error")
end

local _, _, token = string.find(auth_header, "Bearer%s+(.+)")
if not token then
    return exit_with_error(401, "Bearer token malformed or missing", "authentication_error")
end

-- 2. Verify the JWT
-- The `jwt:verify` function checks the signature and standard claims like 'exp' (expiration).
local jwt_obj, err = jwt:verify(jwt_secret, token)

if not jwt_obj then
    ngx.log(ngx.ERR, "JWT validation failed: ", err)
    return exit_with_error(401, "Invalid or expired token: " .. err, "token_validation_error")
end

-- 3. (Optional but recommended) Perform additional claim validation
-- Check the issuer ('iss') and audience ('aud') to ensure the token is from the
-- right authority and intended for this API.
-- local expected_issuer = "https://auth.creativeflow.com"
-- local expected_audience = "creativeflow-api"
-- if jwt_obj.payload.iss ~= expected_issuer then
--     return exit_with_error(403, "Invalid token issuer", "authorization_error")
-- end
-- if jwt_obj.payload.aud ~= expected_audience then
--     return exit_with_error(403, "Invalid token audience", "authorization_error")
-- end

-- 4. Pass user information to the upstream service via request headers
-- This is a critical step for decoupling authentication from business logic.
-- The upstream service can now trust these headers.
local user_id = jwt_obj.payload.sub or jwt_obj.payload.user_id
if user_id then
    ngx.req.set_header("X-User-ID", user_id)
else
    ngx.log(ngx.WARN, "JWT is valid but does not contain a 'sub' or 'user_id' claim.")
end

-- Pass other useful claims if they exist
if jwt_obj.payload.email then
    ngx.req.set_header("X-User-Email", jwt_obj.payload.email)
end

if jwt_obj.payload.roles then
    -- If roles is an array, convert to a comma-separated string
    if type(jwt_obj.payload.roles) == "table" then
        ngx.req.set_header("X-User-Roles", table.concat(jwt_obj.payload.roles, ","))
    else
        ngx.req.set_header("X-User-Roles", jwt_obj.payload.roles)
    end
end

-- If all checks pass, the script finishes and Nginx continues processing the request.