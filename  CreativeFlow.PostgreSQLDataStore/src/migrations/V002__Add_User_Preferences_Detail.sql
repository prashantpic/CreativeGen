-- Flyway Migration V002: Add User Preferences Detail
-- This script adds a new JSONB column 'ui_settings' to the 'User' table
-- to store more detailed user interface preferences.

ALTER TABLE public."User"
ADD COLUMN IF NOT EXISTS "ui_settings" JSONB;

COMMENT ON COLUMN public."User"."ui_settings" IS 'Stores detailed user-specific UI settings and preferences, such as theme, layout choices, or dismissed tips.';