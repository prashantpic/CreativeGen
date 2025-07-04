-- File: /etc/nginx/lua/auth_apikey.lua
-- Purpose: Validates a third-party API key from the X-API-Key header.
-- It first checks a local Redis cache. If not found, it makes an
-- internal subrequest to the api_developer_service for validation.
-- Based on SDS Section 3.2.2.

local redis = require "resty.redis"
local cjson = require "cjson.safe"

-- Configuration from environment variables
local REDIS_HOST = os.getenv("REDIS_HOST") or "127.0.0.1"
local REDIS_PORT = tonumber(os.getenv("REDIS_PORT") or 6379)
local CACHE_TTL = 300 -- Cache validation results for 5 minutes

-- Helper function for standardized error responses
local function exit_with_error(status, error_code, message)
    ngx.status = status
    ngx.header["Content-Type"] = "application/json; charset=utf-8"
    ngx.say(cjson.encode({ status = status, error = error_code, message = message }))
    return ngx.exit(status)
end

-- 1. Extract API key from header
local api_key = ngx.var.http_X_API_Key
if not api_key then
    return exit_with_error(ngx.HTTP_UNAUTHORIZED, "UNAUTHORIZED", "X-API-Key header missing.")
end

-- 2. Cache Lookup (Optional but highly recommended)
local cache_key = "apikey_cache:" .. api_key
local redis_conn

local ok, err = pcall(function()
    redis_conn = redis:new()
    redis_conn:set_timeout(100) -- 100ms timeout for redis operations
    local ok, err = redis_conn:connect(REDIS_HOST, REDIS_PORT)
    if not ok then
        ngx.log(ngx.ERR, "Failed to connect to Redis for API key caching: ", err)
        return -- Proceed without cache
    end

    local cached_data, err = redis_conn:get(cache_key)
    if cached_data and cached_data ~= ngx.null then
        local decoded_data = cjson.decode(cached_data)
        if decoded_data and decoded_data.user_id then
            ngx.req.set_header("X-User-ID", decoded_data.user_id)
            ngx.req.set_header("X-API-Key", api_key) -- Forward the key itself for logging/context
            redis_conn:set_keepalive(10000, 100)
            return true -- Signal that the request is handled
        end
    end
end)

if ok then -- pcall was successful and returned true
    return -- Request was authenticated via cache
end

-- 3. Validation Subrequest (if not in cache)
local subreq_uri = "/internal_validate_apikey"
local subreq_args = {
    method = ngx.HTTP_POST,
    body = cjson.encode({ apiKey = api_key })
}
local res = ngx.location.capture(subreq_uri, subreq_args)

-- 4. Process Subrequest Response
if res.status == ngx.HTTP_OK then
    local body = cjson.decode(res.body)
    if not body or not body.user_id then
        return exit_with_error(ngx.HTTP_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", "Invalid validation response from auth service.")
    end

    -- Set headers for upstream
    ngx.req.set_header("X-User-ID", body.user_id)
    ngx.req.set_header("X-API-Key", api_key)

    -- Store successful validation in cache
    if redis_conn and redis_conn.set then
       pcall(function()
           redis_conn:set(cache_key, res.body)
           redis_conn:expire(cache_key, CACHE_TTL)
           redis_conn:set_keepalive(10000, 100)
       end)
    end

    return -- Allow request to proceed

elseif res.status == ngx.HTTP_UNAUTHORIZED or res.status == ngx.HTTP_FORBIDDEN then
    return exit_with_error(res.status, "INVALID_API_KEY", "API Key is invalid or inactive.")
else
    ngx.log(ngx.ERR, "API Key validation subrequest failed with status: ", res.status, " Body: ", res.body)
    return exit_with_error(ngx.HTTP_INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", "Could not validate API Key.")
end