-- Lua script for atomic session operations in CreativeFlow.
-- Based on SDS section 4.3.1.
-- This file contains Lua code snippets intended to be executed on the Redis server via EVAL or EVALSHA.
-- It is not a standalone executable script.

--[[
    Script: updateAndExtendSession
    Description: Atomically updates one or more fields in a session hash and resets its TTL.
                 This is ideal for "touching" a session on each user activity.
    Usage:
      redis-cli --eval session_operations.lua session:user123 , lastActivity 1678886400 lastPage /dashboard newTTL 3600
    
    KEYS[1]: The session key (e.g., 'session:user123')
    
    ARGV: A list of field-value pairs to set, followed by the new TTL.
          The last argument MUST be the TTL. The number of arguments before it must be even.
          Example: ARGV[1]=field1, ARGV[2]=value1, ARGV[3]=field2, ARGV[4]=value2, ARGV[5]=ttl
    
    Returns: 1 on success, or a Redis error if arguments are incorrect.
]]

-- Extract TTL from the end of ARGV
local ttl = tonumber(ARGV[#ARGV])

-- Check if there are field-value pairs to process
if #ARGV > 1 then
  -- Prepare arguments for HMSET, excluding the last element (TTL)
  local hmset_args = {KEYS[1]}
  for i = 1, #ARGV - 1 do
    table.insert(hmset_args, ARGV[i])
  end
  redis.call('HMSET', unpack(hmset_args))
end

-- Set the expiration for the key
redis.call('EXPIRE', KEYS[1], ttl)

return 1


--[[
    Script: getAndExtendSession
    Description: Atomically retrieves all fields of a session hash and resets its TTL.
                 Useful when validating a session token and wanting to keep it alive.
    Usage:
      redis-cli --eval session_operations.lua session:user123 , 3600
      
    KEYS[1]: The session key
    ARGV[1]: The new TTL for the session key in seconds.
    
    Returns: The session data as a flat array of key/value pairs, or an empty list if not found.
    
    -- LUA LOGIC (as a separate script):
    local session_data = redis.call('HGETALL', KEYS[1])
    if #session_data > 0 then
        redis.call('EXPIRE', KEYS[1], ARGV[1])
    end
    return session_data
]]