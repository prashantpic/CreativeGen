-- Defines the schema for the 'User' table, storing registered user account details.
-- This includes authentication information, preferences, and subscription status.

CREATE TABLE IF NOT EXISTS public."User" (
    "id" UUID PRIMARY KEY NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "passwordHash" VARCHAR(255), -- Hashed at application level. Required for email/password auth.
    "socialProvider" VARCHAR(50) CHECK ("socialProvider" IN ('google', 'facebook', 'apple')),
    "socialProviderId" VARCHAR(255),
    "isEmailVerified" BOOLEAN NOT NULL DEFAULT false,
    "emailVerificationToken" VARCHAR(255),
    "passwordResetToken" VARCHAR(255),
    "passwordResetExpires" TIMESTAMP WITH TIME ZONE,
    "fullName" VARCHAR(100),
    "username" VARCHAR(50),
    "profilePictureUrl" VARCHAR(1024),
    "languagePreference" VARCHAR(10) NOT NULL DEFAULT 'en-US',
    "timezone" VARCHAR(50) NOT NULL DEFAULT 'UTC',
    "mfaEnabled" BOOLEAN NOT NULL DEFAULT false,
    "mfaSecret" VARCHAR(255), -- Encrypted at application level. For authenticator apps (e.g., TOTP).
    "subscriptionTier" VARCHAR(20) NOT NULL DEFAULT 'Free' CHECK ("subscriptionTier" IN ('Free','Pro','Team','Enterprise')),
    "creditBalance" DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    "lastLoginAt" TIMESTAMP WITH TIME ZONE,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP WITH TIME ZONE, -- Timestamp for soft delete.

    CONSTRAINT "uq_user_email" UNIQUE ("email"),
    CONSTRAINT "uq_user_username" UNIQUE ("username"),
    CONSTRAINT "uq_user_social" UNIQUE ("socialProvider", "socialProviderId")
);

-- Add conditional logic for the social unique constraint if the database version supports it properly,
-- otherwise handle uniqueness at the application level.
-- The standard UNIQUE constraint will enforce uniqueness on non-null combinations.
-- For a stricter constraint:
-- CREATE UNIQUE INDEX uq_user_social_conditional ON public."User" ("socialProvider", "socialProviderId")
-- WHERE "socialProvider" IS NOT NULL AND "socialProviderId" IS NOT NULL;


-- Indexes for the User table
CREATE INDEX IF NOT EXISTS "idx_user_subscriptiontier" ON public."User" USING btree ("subscriptionTier");
CREATE INDEX IF NOT EXISTS "idx_user_languagepreference" ON public."User" USING btree ("languagePreference");
CREATE INDEX IF NOT EXISTS "idx_user_deletedat" ON public."User" USING btree ("deletedAt") WHERE "deletedAt" IS NOT NULL;


COMMENT ON TABLE public."User" IS 'Represents a registered user account. Caching strategy: Cache fullName, subscriptionTier, languagePreference, timezone, creditBalance.';
COMMENT ON COLUMN public."User"."passwordHash" IS 'Hashed password. Required if using email/password authentication.';
COMMENT ON COLUMN public."User"."socialProvider" IS 'Used if signed up via social login.';
COMMENT ON COLUMN public."User"."mfaSecret" IS 'For authenticator apps (e.g., TOTP). Flagged for app-level encryption.';
COMMENT ON COLUMN public."User"."creditBalance" IS 'Synced from Odoo, stored here for quick access.';
COMMENT ON COLUMN public."User"."deletedAt" IS 'Timestamp for soft delete.';