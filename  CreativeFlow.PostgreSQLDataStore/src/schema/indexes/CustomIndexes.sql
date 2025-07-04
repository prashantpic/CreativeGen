-- This script defines custom or performance-critical GIN indexes that are not
-- included in the base table DDLs. These are primarily for enhancing search
-- performance on JSONB columns across various tables.
-- Using `IF NOT EXISTS` ensures idempotency.

-- BrandKit JSONB indexes
CREATE INDEX IF NOT EXISTS idx_brandkit_logos_gin ON public."BrandKit" USING gin (logos);
CREATE INDEX IF NOT EXISTS idx_brandkit_stylepreferences_gin ON public."BrandKit" USING gin (stylePreferences);

-- Project JSONB index
CREATE INDEX IF NOT EXISTS idx_project_collaborationstate_gin ON public."Project" USING gin (collaborationState);

-- Asset JSONB index
CREATE INDEX IF NOT EXISTS idx_asset_metadata_gin ON public."Asset" USING gin (metadata);

-- GenerationRequest JSONB index
CREATE INDEX IF NOT EXISTS idx_generationrequest_inputparameters_gin ON public."GenerationRequest" USING gin (inputParameters);

-- APIClient JSONB index
CREATE INDEX IF NOT EXISTS idx_apiclient_permissions_gin ON public."APIClient" USING gin (permissions);

-- UsageLog JSONB index
CREATE INDEX IF NOT EXISTS idx_usagelog_details_gin ON public."UsageLog" USING gin (details);

-- Notification JSONB index
CREATE INDEX IF NOT EXISTS idx_notification_metadata_gin ON public."Notification" USING gin (metadata);

-- AIModelVersion JSONB index
CREATE INDEX IF NOT EXISTS idx_aimodelversion_parameters_gin ON public."AIModelVersion" USING gin (parameters);

-- AIModelDeployment JSONB index
CREATE INDEX IF NOT EXISTS idx_aimodeldeployment_kubernetesdetails_gin ON public."AIModelDeployment" USING gin (kubernetesDetails);

-- AIModelFeedback JSONB index
CREATE INDEX IF NOT EXISTS idx_aimodelfeedback_details_gin ON public."AIModelFeedback" USING gin (details);