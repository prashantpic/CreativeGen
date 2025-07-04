-- Defines the schema for the 'GenerationRequest' table.
-- Stores details of AI creative generation requests and their outcomes.

CREATE TABLE IF NOT EXISTS public."GenerationRequest" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "projectId" UUID NOT NULL,
    "inputPrompt" TEXT NOT NULL,
    "styleGuidance" TEXT,
    "inputParameters" JSONB,
    "status" VARCHAR(50) NOT NULL DEFAULT 'Pending' CHECK ("status" IN ('Pending','ProcessingSamples','AwaitingSelection','ProcessingFinal','Completed','Failed','Cancelled','ContentRejected')),
    "errorMessage" TEXT,
    "sampleAssets" JSONB,
    "selectedSampleId" UUID, -- This would logically reference an Asset, but is not a hard FK to avoid circular dependencies at creation.
    "finalAssetId" UUID, -- Nullable FK to Asset table.
    "creditsCostSample" DECIMAL(10, 2),
    "creditsCostFinal" DECIMAL(10, 2),
    "aiModelUsed" VARCHAR(100),
    "processingTimeMs" INTEGER,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_generationrequest_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE RESTRICT ON UPDATE NO ACTION,
    CONSTRAINT "fk_generationrequest_project" FOREIGN KEY ("projectId") REFERENCES public."Project"("id") ON DELETE SET NULL ON UPDATE NO ACTION
    -- FK to finalAssetId is added after Asset table is created to break circular dependency.
);

-- Indexes for the GenerationRequest table
CREATE INDEX IF NOT EXISTS "idx_generationrequest_userid" ON public."GenerationRequest" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_generationrequest_projectid" ON public."GenerationRequest" USING btree ("projectId");
CREATE INDEX IF NOT EXISTS "idx_generationrequest_status" ON public."GenerationRequest" USING btree ("status");
CREATE INDEX IF NOT EXISTS "idx_generationrequest_createdat" ON public."GenerationRequest" USING btree ("createdAt");
CREATE INDEX IF NOT EXISTS "idx_generationrequest_status_createdat" ON public."GenerationRequest" USING btree ("status", "createdAt");


COMMENT ON TABLE public."GenerationRequest" IS 'AI creative generation request details and results.';
COMMENT ON COLUMN public."GenerationRequest"."userId" IS 'Restrict user deletion if requests exist for audit/billing.';
COMMENT ON COLUMN public."GenerationRequest"."inputParameters" IS 'JSON object including format, resolution hints, input assets references, etc.';
COMMENT ON COLUMN public."GenerationRequest"."sampleAssets" IS 'JSON array of sample asset metadata (e.g., [{ ''id'': ''asset_uuid_ref'', ''url'': ''minio_path'' }]). Reference to Asset entity.';
COMMENT ON COLUMN public."GenerationRequest"."finalAssetId" IS 'Link to the final generated Asset entity.';