-- Defines the schema for the 'AIModelVersion' table, tracking specific versions of AI models.

CREATE TABLE IF NOT EXISTS public."AIModelVersion" (
    "id" UUID PRIMARY KEY NOT NULL,
    "modelId" UUID NOT NULL,
    "versionNumber" VARCHAR(50) NOT NULL,
    "sourcePath" VARCHAR(1024),
    "format" VARCHAR(50),
    "parameters" JSONB,
    "status" VARCHAR(50) NOT NULL DEFAULT 'Staged' CHECK ("status" IN ('Staged','Production','Deprecated','Archived','Failed')),
    "validationResultId" UUID, -- Nullable FK to AIModelValidationResult, added after its table is created to break cycle.
    "createdByUserId" UUID,
    "releaseNotes" TEXT,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_aimodelversion_model" FOREIGN KEY ("modelId") REFERENCES public."AIModel"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelversion_user" FOREIGN KEY ("createdByUserId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "uq_aimodelversion_model_version" UNIQUE ("modelId", "versionNumber")
    -- FK to validationResultId is added after AIModelValidationResult table is created.
);

-- Indexes for the AIModelVersion table
CREATE INDEX IF NOT EXISTS "idx_aimodelversion_modelid" ON public."AIModelVersion" USING btree ("modelId");
CREATE INDEX IF NOT EXISTS "idx_aimodelversion_status" ON public."AIModelVersion" USING btree ("status");

COMMENT ON TABLE public."AIModelVersion" IS 'Specific versions of AI models.';
COMMENT ON COLUMN public."AIModelVersion"."versionNumber" IS 'e.g., ''1.0'', ''2023-10-26'', ''DALL-E 3''.';
COMMENT ON COLUMN public."AIModelVersion"."sourcePath" IS 'MinIO path for internal model artifacts. Null for external models.';
COMMENT ON COLUMN public."AIModelVersion"."format" IS 'e.g., ''ONNX'', ''TensorFlow SavedModel'', ''API''.';
COMMENT ON COLUMN public."AIModelVersion"."createdByUserId" IS 'User (admin/enterprise) who uploaded/created this version.';