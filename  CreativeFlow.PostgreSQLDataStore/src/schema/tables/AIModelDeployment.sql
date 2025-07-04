-- Defines the schema for the 'AIModelDeployment' table.
-- Records deployments of AI model versions to various environments.

CREATE TABLE IF NOT EXISTS public."AIModelDeployment" (
    "id" UUID PRIMARY KEY NOT NULL,
    "modelVersionId" UUID NOT NULL,
    "environment" VARCHAR(50) NOT NULL CHECK ("environment" IN ('staging','production','testing')),
    "status" VARCHAR(50) NOT NULL DEFAULT 'Initiated' CHECK ("status" IN ('Initiated','Deploying','Active','Inactive','Failed','RolledBack')),
    "deploymentStrategy" VARCHAR(50),
    "endpoint" VARCHAR(255),
    "kubernetesDetails" JSONB,
    "deployedByUserId" UUID,
    "deploymentTimestamp" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_aimodeldeployment_version" FOREIGN KEY ("modelVersionId") REFERENCES public."AIModelVersion"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodeldeployment_user" FOREIGN KEY ("deployedByUserId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);

-- Indexes for the AIModelDeployment table
CREATE INDEX IF NOT EXISTS "idx_aimodeldeployment_versionid_env" ON public."AIModelDeployment" USING btree ("modelVersionId", "environment");
CREATE INDEX IF NOT EXISTS "idx_aimodeldeployment_status" ON public."AIModelDeployment" USING btree ("status");

COMMENT ON TABLE public."AIModelDeployment" IS 'Record of AI model version deployments.';
COMMENT ON COLUMN public."AIModelDeployment"."deploymentStrategy" IS 'e.g., ''blue_green'', ''canary'', ''rolling_update''.';
COMMENT ON COLUMN public."AIModelDeployment"."endpoint" IS 'Internal endpoint for accessing the deployed model.';
COMMENT ON COLUMN public."AIModelDeployment"."kubernetesDetails" IS 'JSON object with K8s deployment name, namespace, pod counts, etc.';
COMMENT ON COLUMN public."AIModelDeployment"."deployedByUserId" IS 'User or system account that triggered deployment.';