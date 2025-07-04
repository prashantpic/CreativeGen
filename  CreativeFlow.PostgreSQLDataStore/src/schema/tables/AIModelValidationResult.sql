-- Defines the schema for the 'AIModelValidationResult' table.
-- Stores results from validating AI model versions.

CREATE TABLE IF NOT EXISTS public."AIModelValidationResult" (
    "id" UUID PRIMARY KEY NOT NULL,
    "modelVersionId" UUID NOT NULL,
    "validationTimestamp" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "securityScanStatus" VARCHAR(50) NOT NULL CHECK ("securityScanStatus" IN ('Passed','Failed','Pending','Skipped')),
    "functionalStatus" VARCHAR(50) NOT NULL CHECK ("functionalStatus" IN ('Passed','Failed','Pending','Skipped')),
    "performanceBenchmark" JSONB,
    "results" JSONB,
    "validatedByUserId" UUID,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_aimodelvalidationresult_version" FOREIGN KEY ("modelVersionId") REFERENCES public."AIModelVersion"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelvalidationresult_user" FOREIGN KEY ("validatedByUserId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);

-- Indexes for the AIModelValidationResult table
CREATE INDEX IF NOT EXISTS "idx_aimodelvalidationresult_versionid" ON public."AIModelValidationResult" USING btree ("modelVersionId");
CREATE INDEX IF NOT EXISTS "idx_aimodelvalidationresult_timestamp" ON public."AIModelValidationResult" USING btree ("validationTimestamp");


COMMENT ON TABLE public."AIModelValidationResult" IS 'Results from validating an AI model version.';
COMMENT ON COLUMN public."AIModelValidationResult"."performanceBenchmark" IS 'JSON object with benchmark data (latency, throughput, quality metrics).';
COMMENT ON COLUMN public."AIModelValidationResult"."results" IS 'Full results log from validation tools.';
COMMENT ON COLUMN public."AIModelValidationResult"."validatedByUserId" IS 'User or system account that triggered validation.';