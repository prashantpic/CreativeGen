-- Lua script for a flexible sliding window rate limiter using a sorted set.
-- Based on SDS section 4.3.2.
-- This script is designed to be executed via EVAL or EVALSHA on a Redis server.

--[[
    Script: isAllowedSlidingWindow
    Description: Checks if a request is allowed under a given rate limit using the sliding window algorithm.
                 It is atomic and highly efficient.
    Usage:
      redis-cli --eval rate_limiter_flexible.lua ratelimit:user123:api , now_ms window_ms limit
      Example: redis-cli --eval rate_limiter_flexible.lua ratelimit:user123:api , 1678886400000 60000 100

    KEYS[1]: The unique key for the rate limit (e.g., 'ratelimit:user123:api_endpoint')
    
    ARGV[1]: The current timestamp in milliseconds.
    ARGV[2]: The size of the time window in milliseconds (e.g., 60000 for a 60-second window).
    ARGV[3]: The maximum number of requests allowed in the window.
    
    Returns: A table with two values:
             1. is_allowed (number): 1 if the request is allowed, 0 if it is denied.
             2. current_count (number): The number of requests in the window *after* the current request was processed.
]]

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

-- The score at which to start clearing old entries from the sorted set
local clear_before = now - window

-- Atomically perform all operations. This is the power of Lua scripting in Redis.

-- 1. Remove timestamps (members) that are older than the current window.
--    ZREMRANGEBYSCORE is efficient for this.
redis.call('ZREMRANGEBYSCORE', key, 0, clear_before)

-- 2. Get the current number of requests in the window.
local current_count = redis.call('ZCARD', key)

local is_allowed = 0
-- 3. Check if the current count is below the limit.
if current_count < limit then
    -- If allowed, add the current request timestamp to the sorted set.
    -- The member and score are the same (the timestamp).
    redis.call('ZADD', key, now, now)
    
    -- Set the allowed flag to 1.
    is_allowed = 1
end

-- 4. Set an expiration on the key itself. This is a cleanup mechanism in case
--    the key becomes inactive. The TTL should be at least the window size.
redis.call('PEXPIRE', key, window)

-- 5. Return the result.
local final_count = redis.call('ZCARD', key)
return {is_allowed, final_count}