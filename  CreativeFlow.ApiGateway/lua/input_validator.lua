--
-- CreativeFlow: API Gateway - Input Validator Script
--
-- Description: This Lua script performs validation on the request body against a
-- predefined JSON schema. This allows for complex validation at the edge,
-- protecting upstream services from malformed requests.
--
-- Dependencies: lua-jsonschema (https://github.com/api7/lua-jsonschema)
--               Install via OPM: `opm get api7/lua-jsonschema`
--

local validator = require "resty.schema.validator"
local cjson = require "cjson.safe" -- Use safe cjson to handle potential errors

-- --- Schema Definitions ---
--
-- In a real application, schemas should be loaded from external files for better
-- management, e.g., based on the request URI.
--
-- Example of loading from a file:
-- local schema_file = io.open("/etc/nginx/lua/schemas/" .. ngx.var.uri .. ".json", "r")
-- if schema_file then
--     local schema_content = schema_file:read("*a")
--     schema_file:close()
--     schema = cjson.decode(schema_content)
-- end
--
-- For this example, we define schemas directly in the script.
local schemas = {
    -- Schema for an example endpoint: /api/v1/generation-requests
    ["/api/v1/generation-requests"] = {
        type = "object",
        properties = {
            user_id = { type = "string", format = "uuid" },
            project_id = { type = "string", format = "uuid" },
            input_prompt = { type = "string", minLength = 10, maxLength = 2000 },
            output_format = { type = "string", enum = {"InstagramPost_1x1", "Custom"} },
            custom_dimensions = {
                type = "object",
                properties = {
                    width = { type = "integer", minimum = 64, maximum = 4096 },
                    height = { type = "integer", minimum = 64, maximum = 4096 },
                },
                required = {"width", "height"}
            }
        },
        required = {"user_id", "project_id", "input_prompt", "output_format"}
    }
}

-- Select the schema based on the request URI
local request_uri = ngx.var.uri
local selected_schema = schemas[request_uri]

-- If no schema is defined for this URI, or if the method is not POST/PUT, we can skip validation.
if not selected_schema or (ngx.var.request_method ~= "POST" and ngx.var.request_method ~= "PUT") then
    return
end

-- 1. Read the request body
ngx.req.read_body()
local body_data = ngx.req.get_body_data()

if not body_data or body_data == "" then
    ngx.status = 400
    ngx.say('{"error": "bad_request", "detail": "Request body cannot be empty."}')
    return ngx.exit(400)
end

-- 2. Decode the JSON body
local ok, body_json = pcall(cjson.decode, body_data)
if not ok then
    ngx.status = 400
    ngx.say('{"error": "bad_request", "detail": "Failed to decode JSON body: ' .. tostring(body_json) .. '"}')
    return ngx.exit(400)
end

-- 3. Validate the JSON against the schema
local v, err = validator.new(selected_schema)
if not v then
    ngx.log(ngx.ERR, "failed to create validator: ", err)
    -- This is a server-side error (bad schema)
    ngx.exit(500)
end

local ok, err = v:validate(body_json)

-- 4. If validation fails, return a detailed 400 error
if not ok then
    ngx.status = 400
    ngx.header['Content-Type'] = 'application/json; charset=utf-8'
    ngx.say(cjson.encode({
        error = "validation_error",
        detail = "The provided data is invalid.",
        -- The error from lua-jsonschema can be quite detailed
        validation_errors = err
    }))
    return ngx.exit(400)
end

-- If validation succeeds, the script finishes and processing continues.