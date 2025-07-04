-- Defines the schema for the 'APIClient' table, storing API access credentials for developers.

CREATE TABLE IF NOT EXISTS public."APIClient" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "apiKey" VARCHAR(100) NOT NULL,
    "secretHash" VARCHAR(255) NOT NULL, -- Hashed API secret. The raw secret is only shown once on creation.
    "permissions" JSONB,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_apiclient_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_apiclient_apikey" UNIQUE ("apiKey")
);

-- Indexes for the APIClient table
CREATE INDEX IF NOT EXISTS "idx_apiclient_userid" ON public."APIClient" USING btree ("userId");

COMMENT ON TABLE public."APIClient" IS 'API access credentials for developers.';
COMMENT ON COLUMN public."APIClient"."name" IS 'User-defined name for the API key.';
COMMENT ON COLUMN public."APIClient"."apiKey" IS 'Public API key identifier.';
COMMENT ON COLUMN public."APIClient"."secretHash" IS 'Hashed API secret.';
COMMENT ON COLUMN public."APIClient"."permissions" IS 'JSON object defining granular permissions for this key.';