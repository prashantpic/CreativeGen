-- Defines the schema for the 'UsageLog' table.
-- Provides a detailed log of billable or otherwise trackable user actions.

CREATE TABLE IF NOT EXISTS public."UsageLog" (
    "id" BIGSERIAL PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "generationRequestId" UUID,
    "apiClientId" UUID,
    "actionType" VARCHAR(100) NOT NULL,
    "details" JSONB,
    "creditsCost" DECIMAL(10, 2),
    "timestamp" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_usagelog_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_usagelog_genrequest" FOREIGN KEY ("generationRequestId") REFERENCES public."GenerationRequest"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_usagelog_apiclient" FOREIGN KEY ("apiClientId") REFERENCES public."APIClient"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);

-- Indexes for the UsageLog table
CREATE INDEX IF NOT EXISTS "idx_usagelog_userid_timestamp" ON public."UsageLog" USING btree ("userId", "timestamp");
CREATE INDEX IF NOT EXISTS "idx_usagelog_actiontype" ON public."UsageLog" USING btree ("actionType");
CREATE INDEX IF NOT EXISTS "idx_usagelog_generationrequestid" ON public."UsageLog" USING btree ("generationRequestId");
CREATE INDEX IF NOT EXISTS "idx_usagelog_apiclientid" ON public."UsageLog" USING btree ("apiClientId");

COMMENT ON TABLE public."UsageLog" IS 'Detailed log of billable or trackable user actions.';
COMMENT ON COLUMN public."UsageLog"."actionType" IS 'e.g., ''sample_generation_initiated'', ''final_generation_completed'', ''asset_uploaded'', ''asset_exported'', ''api_call_success'', ''login_success'', ''subscription_change''.';
COMMENT ON COLUMN public."UsageLog"."details" IS 'Additional context for the action (e.g., file format, resolution, API endpoint, duration).';
COMMENT ON COLUMN public."UsageLog"."creditsCost" IS 'Credits consumed by this specific action step if any.';

/* PARTITIONING STRATEGY: This table is a candidate for RANGE partitioning on the 'timestamp' column based on data volume. */