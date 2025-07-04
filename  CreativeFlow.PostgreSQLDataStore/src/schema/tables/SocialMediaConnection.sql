-- Defines the schema for the 'SocialMediaConnection' table, storing user's connected social media accounts.

CREATE TABLE IF NOT EXISTS public."SocialMediaConnection" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "platform" VARCHAR(20) NOT NULL CHECK ("platform" IN ('Instagram','Facebook','LinkedIn','Twitter','Pinterest','TikTok')),
    "externalUserId" VARCHAR(100) NOT NULL,
    "accessToken" TEXT NOT NULL, -- Encrypted at the application layer before storing.
    "refreshToken" TEXT, -- Encrypted at the application layer before storing.
    "expiresAt" TIMESTAMP WITH TIME ZONE,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_socialconnection_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_socialconnection_user_platform" UNIQUE ("userId", "platform")
);

-- Indexes for the SocialMediaConnection table
CREATE INDEX IF NOT EXISTS "idx_socialconnection_userid_platform" ON public."SocialMediaConnection" USING btree ("userId", "platform");

COMMENT ON TABLE public."SocialMediaConnection" IS 'User''s connected social media accounts.';
COMMENT ON COLUMN public."SocialMediaConnection"."accessToken" IS 'OAuth token for accessing the platform API, encrypted at application level.';
COMMENT ON COLUMN public."SocialMediaConnection"."refreshToken" IS 'OAuth refresh token, encrypted at application level.';