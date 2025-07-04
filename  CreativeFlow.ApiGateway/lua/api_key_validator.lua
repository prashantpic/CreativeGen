--
-- CreativeFlow: API Gateway - API Key Validator Script
--
-- Description: This Lua script validates an API key provided in the 'X-API-Key' header.
-- It's designed for developer-facing APIs.
--
-- Dependencies: lua-resty-redis (for production implementation)
--               cjson
--

local cjson = require "cjson"

-- --- Helper function to send an error response ---
local function exit_with_error(status_code, error_message)
    ngx.status = status_code
    ngx.header['Content-Type'] = 'application/json; charset=utf-8'
    ngx.say(cjson.encode({
        detail = error_message
    }))
    return ngx.exit(status_code)
end

-- 1. Get the API Key from the header
local api_key = ngx.var.http_x_api_key
if not api_key then
    return exit_with_error(401, "Missing required X-API-Key header.")
end

-- --- Validation Logic ---
--
-- !! IMPORTANT !!
-- The following is a PLACEHOLDER implementation using a simple Lua table.
-- In a PRODUCTION environment, you MUST replace this with a call to a fast,
-- secure data store like Redis or a dedicated authentication microservice.
--
-- Production Strategy using Redis:
-- 1. Use `resty.redis` to connect to a Redis instance.
-- 2. Store API keys in Redis, e.g., HSET apikeys:<api_key> user_id "uuid-..." tier "tier1" ...
-- 3. On each request, perform: `redis:hgetall("apikeys:" .. api_key)`
-- 4. If the key exists, proceed. If not, reject.
-- 5. Cache the result in `ngx.ctx` to avoid repeated lookups on the same request.
--
local function validate_key_placeholder(key)
    local valid_keys = {
        ["dev-key-tier1-abc123"] = { user_id = "user-abc-123", tier = "tier1", rate_limit = 100 },
        ["dev-key-tier2-def456"] = { user_id = "user-def-456", tier = "tier2", rate_limit = 1000 },
        ["dev-key-ent-xyz789"] = { user_id = "user-xyz-789", tier = "enterprise", rate_limit = 9999 }
    }
    return valid_keys[key]
end

local key_info = validate_key_placeholder(api_key)

-- 2. Check if the key is valid
if not key_info then
    -- Use a generic message to avoid leaking information about valid key formats.
    return exit_with_error(403, "Invalid API Key provided.")
end

-- 3. Pass authenticated identity and metadata to the upstream service
ngx.req.set_header("X-Authenticated-User-ID", key_info.user_id)
ngx.req.set_header("X-API-Key-Tier", key_info.tier)

-- This variable can be used by other nginx directives, such as the `map`
-- for dynamic rate limiting zones.
ngx.var.api_key_tier = key_info.tier

-- If all checks pass, the script finishes and Nginx continues processing.