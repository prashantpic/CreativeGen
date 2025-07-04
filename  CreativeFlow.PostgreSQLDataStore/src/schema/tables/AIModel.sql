-- Defines the schema for the 'AIModel' table, storing metadata about AI models available on the platform.
-- This table acts as a registry for AI models, their providers, and intended tasks.

CREATE TABLE IF NOT EXISTS public."AIModel" (
    "id" UUID PRIMARY KEY NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "provider" VARCHAR(50) NOT NULL,
    "taskType" VARCHAR(50) NOT NULL CHECK ("taskType" IN ('ImageGeneration', 'TextGeneration', 'ImageTransformation', 'StyleTransfer', 'ContentSafety')),
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "uq_aimodel_name" UNIQUE ("name")
);

-- Indexes for the AIModel table
CREATE INDEX IF NOT EXISTS "idx_aimodel_provider_tasktype" ON public."AIModel" USING btree ("provider", "taskType");
CREATE INDEX IF NOT EXISTS "idx_aimodel_isactive" ON public."AIModel" USING btree ("isActive");

COMMENT ON TABLE public."AIModel" IS 'Metadata for AI models available on the platform.';
COMMENT ON COLUMN public."AIModel"."name" IS 'Unique name of the AI model.';
COMMENT ON COLUMN public."AIModel"."provider" IS 'e.g., ''Internal'', ''OpenAI'', ''StabilityAI'', ''OtherProvider''.';
COMMENT ON COLUMN public."AIModel"."taskType" IS 'The primary task the model is designed for.';
COMMENT ON COLUMN public."AIModel"."isActive" IS 'Indicates if the model is currently available for use.';