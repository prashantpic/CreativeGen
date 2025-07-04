-- Flyway Migration V001: Initial Schema
-- This script creates the complete initial database structure for the CreativeFlow AI platform.
-- The order of table creation is determined by foreign key dependencies.

-- Level 0: Tables with no foreign key dependencies
--------------------------------------------------------------------------------
-- Defines the schema for the 'User' table
CREATE TABLE IF NOT EXISTS public."User" (
    "id" UUID PRIMARY KEY NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "passwordHash" VARCHAR(255),
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
    "mfaSecret" VARCHAR(255),
    "subscriptionTier" VARCHAR(20) NOT NULL DEFAULT 'Free' CHECK ("subscriptionTier" IN ('Free','Pro','Team','Enterprise')),
    "creditBalance" DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    "lastLoginAt" TIMESTAMP WITH TIME ZONE,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP WITH TIME ZONE,
    CONSTRAINT "uq_user_email" UNIQUE ("email"),
    CONSTRAINT "uq_user_username" UNIQUE ("username"),
    CONSTRAINT "uq_user_social" UNIQUE ("socialProvider", "socialProviderId")
);
CREATE INDEX IF NOT EXISTS "idx_user_subscriptiontier" ON public."User" USING btree ("subscriptionTier");
CREATE INDEX IF NOT EXISTS "idx_user_languagepreference" ON public."User" USING btree ("languagePreference");
CREATE INDEX IF NOT EXISTS "idx_user_deletedat" ON public."User" USING btree ("deletedAt") WHERE "deletedAt" IS NOT NULL;

-- Defines the schema for the 'AIModel' table
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
CREATE INDEX IF NOT EXISTS "idx_aimodel_provider_tasktype" ON public."AIModel" USING btree ("provider", "taskType");
CREATE INDEX IF NOT EXISTS "idx_aimodel_isactive" ON public."AIModel" USING btree ("isActive");


-- Level 1: Tables depending on User and AIModel
--------------------------------------------------------------------------------
-- Defines the schema for the 'Team' table
CREATE TABLE IF NOT EXISTS public."Team" (
    "id" UUID PRIMARY KEY NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "ownerId" UUID NOT NULL,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_team_owner" FOREIGN KEY ("ownerId") REFERENCES public."User"("id") ON DELETE RESTRICT ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_team_ownerid" ON public."Team" USING btree ("ownerId");

-- Defines the 'APIClient' table
CREATE TABLE IF NOT EXISTS public."APIClient" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "apiKey" VARCHAR(100) NOT NULL,
    "secretHash" VARCHAR(255) NOT NULL,
    "permissions" JSONB,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_apiclient_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_apiclient_apikey" UNIQUE ("apiKey")
);
CREATE INDEX IF NOT EXISTS "idx_apiclient_userid" ON public."APIClient" USING btree ("userId");

-- Defines the 'Subscription' table
CREATE TABLE IF NOT EXISTS public."Subscription" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "odooSaleOrderId" VARCHAR(255) NOT NULL,
    "planId" VARCHAR(50) NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK ("status" IN ('Active','Trial','Suspended','Cancelled','Expired')),
    "currentPeriodStart" TIMESTAMP WITH TIME ZONE NOT NULL,
    "currentPeriodEnd" TIMESTAMP WITH TIME ZONE NOT NULL,
    "paymentProvider" VARCHAR(50) NOT NULL CHECK ("paymentProvider" IN ('Stripe', 'PayPal', 'OdooManual')),
    "paymentProviderSubscriptionId" VARCHAR(255),
    "paymentMethodId" VARCHAR(255),
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_subscription_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_subscription_odoo_so" UNIQUE ("odooSaleOrderId")
);
CREATE INDEX IF NOT EXISTS "idx_subscription_userid_status" ON public."Subscription" USING btree ("userId", "status");
CREATE INDEX IF NOT EXISTS "idx_subscription_currentperiodend" ON public."Subscription" USING btree ("currentPeriodEnd");

-- Defines the 'Session' table
CREATE TABLE IF NOT EXISTS public."Session" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "deviceInfo" VARCHAR(255) NOT NULL,
    "ipAddress" VARCHAR(45) NOT NULL,
    "userAgent" TEXT,
    "lastActivity" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expiresAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_session_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_session_userid_expiresat" ON public."Session" USING btree ("userId", "expiresAt");
CREATE INDEX IF NOT EXISTS "idx_session_expiresat" ON public."Session" USING btree ("expiresAt");
CREATE INDEX IF NOT EXISTS "idx_session_lastactivity" ON public."Session" USING btree ("lastActivity");

-- Defines the 'Notification' table
CREATE TABLE IF NOT EXISTS public."Notification" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "message" TEXT NOT NULL,
    "metadata" JSONB,
    "isRead" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_notification_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_notification_userid_isread_createdat" ON public."Notification" USING btree ("userId", "isRead", "createdAt");
CREATE INDEX IF NOT EXISTS "idx_notification_userid_isread_unread" ON public."Notification" ("userId", "isRead") WHERE "isRead" = false;

-- Defines the 'SocialMediaConnection' table
CREATE TABLE IF NOT EXISTS public."SocialMediaConnection" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "platform" VARCHAR(20) NOT NULL CHECK ("platform" IN ('Instagram','Facebook','LinkedIn','Twitter','Pinterest','TikTok')),
    "externalUserId" VARCHAR(100) NOT NULL,
    "accessToken" TEXT NOT NULL,
    "refreshToken" TEXT,
    "expiresAt" TIMESTAMP WITH TIME ZONE,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_socialconnection_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_socialconnection_user_platform" UNIQUE ("userId", "platform")
);
CREATE INDEX IF NOT EXISTS "idx_socialconnection_userid_platform" ON public."SocialMediaConnection" USING btree ("userId", "platform");

-- Defines the 'Template' table
CREATE TABLE IF NOT EXISTS public."Template" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "category" VARCHAR(50) NOT NULL,
    "previewUrl" VARCHAR(1024) NOT NULL,
    "sourceData" JSONB NOT NULL,
    "tags" JSONB,
    "isPublic" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_template_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_template_category_ispublic" ON public."Template" USING btree ("category", "isPublic");
CREATE INDEX IF NOT EXISTS "idx_template_userid" ON public."Template" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_template_tags_gin" ON public."Template" USING gin ("tags");


-- Level 2: Tables depending on Level 1
--------------------------------------------------------------------------------
-- Defines the 'TeamMember' table
CREATE TABLE IF NOT EXISTS public."TeamMember" (
    "id" UUID PRIMARY KEY NOT NULL,
    "teamId" UUID NOT NULL,
    "userId" UUID NOT NULL,
    "role" VARCHAR(20) NOT NULL CHECK ("role" IN ('Owner','Admin','Editor','Viewer')),
    "joinedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_teammember_team" FOREIGN KEY ("teamId") REFERENCES public."Team"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_teammember_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_teammember_team_user" UNIQUE ("teamId", "userId")
);
CREATE INDEX IF NOT EXISTS "idx_teammember_teamid" ON public."TeamMember" USING btree ("teamId");
CREATE INDEX IF NOT EXISTS "idx_teammember_userid_role" ON public."TeamMember" USING btree ("userId", "role");

-- Defines the 'BrandKit' table
CREATE TABLE IF NOT EXISTS public."BrandKit" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "teamId" UUID,
    "name" VARCHAR(100) NOT NULL,
    "colors" JSONB NOT NULL,
    "fonts" JSONB NOT NULL,
    "logos" JSONB,
    "stylePreferences" JSONB,
    "isDefault" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_brandkit_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_brandkit_team" FOREIGN KEY ("teamId") REFERENCES public."Team"("id") ON DELETE CASCADE ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_brandkit_userid" ON public."BrandKit" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_brandkit_teamid" ON public."BrandKit" USING btree ("teamId");
CREATE INDEX IF NOT EXISTS "idx_brandkit_colors_gin" ON public."BrandKit" USING gin ("colors");
CREATE INDEX IF NOT EXISTS "idx_brandkit_fonts_gin" ON public."BrandKit" USING gin ("fonts");

-- Level 3: Tables depending on Level 2
--------------------------------------------------------------------------------
-- Defines the 'Workbench' table
CREATE TABLE IF NOT EXISTS public."Workbench" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "defaultBrandKitId" UUID,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_workbench_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_workbench_brandkit" FOREIGN KEY ("defaultBrandKitId") REFERENCES public."BrandKit"("id") ON DELETE SET NULL ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_workbench_userid" ON public."Workbench" USING btree ("userId");

-- Level 4: Tables depending on Level 3
--------------------------------------------------------------------------------
-- Defines the 'Project' table
CREATE TABLE IF NOT EXISTS public."Project" (
    "id" UUID PRIMARY KEY NOT NULL,
    "workbenchId" UUID NOT NULL,
    "userId" UUID NOT NULL,
    "templateId" UUID,
    "brandKitId" UUID,
    "name" VARCHAR(100) NOT NULL,
    "targetPlatform" VARCHAR(50),
    "collaborationState" JSONB,
    "lastCollaboratedAt" TIMESTAMP WITH TIME ZONE,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP WITH TIME ZONE,
    CONSTRAINT "fk_project_workbench" FOREIGN KEY ("workbenchId") REFERENCES public."Workbench"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_project_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_project_template" FOREIGN KEY ("templateId") REFERENCES public."Template"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_project_brandkit" FOREIGN KEY ("brandKitId") REFERENCES public."BrandKit"("id") ON DELETE SET NULL ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_project_workbenchid" ON public."Project" USING btree ("workbenchId");
CREATE INDEX IF NOT EXISTS "idx_project_userid" ON public."Project" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_project_updatedat" ON public."Project" USING btree ("updatedAt");

-- Level 5: MLOps and Generation Core
--------------------------------------------------------------------------------
-- Defines 'AIModelVersion' table
CREATE TABLE IF NOT EXISTS public."AIModelVersion" (
    "id" UUID PRIMARY KEY NOT NULL,
    "modelId" UUID NOT NULL,
    "versionNumber" VARCHAR(50) NOT NULL,
    "sourcePath" VARCHAR(1024),
    "format" VARCHAR(50),
    "parameters" JSONB,
    "status" VARCHAR(50) NOT NULL DEFAULT 'Staged' CHECK ("status" IN ('Staged','Production','Deprecated','Archived','Failed')),
    "validationResultId" UUID, -- FK added after AIModelValidationResult is created
    "createdByUserId" UUID,
    "releaseNotes" TEXT,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_aimodelversion_model" FOREIGN KEY ("modelId") REFERENCES public."AIModel"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelversion_user" FOREIGN KEY ("createdByUserId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "uq_aimodelversion_model_version" UNIQUE ("modelId", "versionNumber")
);
CREATE INDEX IF NOT EXISTS "idx_aimodelversion_modelid" ON public."AIModelVersion" USING btree ("modelId");
CREATE INDEX IF NOT EXISTS "idx_aimodelversion_status" ON public."AIModelVersion" USING btree ("status");

-- Defines 'AIModelValidationResult' table
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
CREATE INDEX IF NOT EXISTS "idx_aimodelvalidationresult_versionid" ON public."AIModelValidationResult" USING btree ("modelVersionId");
CREATE INDEX IF NOT EXISTS "idx_aimodelvalidationresult_timestamp" ON public."AIModelValidationResult" USING btree ("validationTimestamp");

-- Add FK from AIModelVersion to AIModelValidationResult
ALTER TABLE public."AIModelVersion" ADD CONSTRAINT "fk_aimodelversion_validationresult" FOREIGN KEY ("validationResultId") REFERENCES public."AIModelValidationResult"("id") ON DELETE SET NULL ON UPDATE NO ACTION;

-- Defines 'AIModelDeployment' table
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
CREATE INDEX IF NOT EXISTS "idx_aimodeldeployment_versionid_env" ON public."AIModelDeployment" USING btree ("modelVersionId", "environment");
CREATE INDEX IF NOT EXISTS "idx_aimodeldeployment_status" ON public."AIModelDeployment" USING btree ("status");

-- Defines 'GenerationRequest' table
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
    "selectedSampleId" UUID,
    "finalAssetId" UUID, -- FK added after Asset table is created
    "creditsCostSample" DECIMAL(10, 2),
    "creditsCostFinal" DECIMAL(10, 2),
    "aiModelUsed" VARCHAR(100),
    "processingTimeMs" INTEGER,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_generationrequest_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE RESTRICT ON UPDATE NO ACTION,
    CONSTRAINT "fk_generationrequest_project" FOREIGN KEY ("projectId") REFERENCES public."Project"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_generationrequest_userid" ON public."GenerationRequest" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_generationrequest_projectid" ON public."GenerationRequest" USING btree ("projectId");
CREATE INDEX IF NOT EXISTS "idx_generationrequest_status_createdat" ON public."GenerationRequest" USING btree ("status", "createdAt");

-- Defines 'Asset' table
CREATE TABLE IF NOT EXISTS public."Asset" (
    "id" UUID PRIMARY KEY NOT NULL,
    "projectId" UUID,
    "userId" UUID NOT NULL,
    "generationRequestId" UUID,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(20) NOT NULL CHECK ("type" IN ('Uploaded','AIGenerated','Derived')),
    "filePath" VARCHAR(1024) NOT NULL,
    "mimeType" VARCHAR(50) NOT NULL,
    "format" VARCHAR(10) NOT NULL,
    "resolution" VARCHAR(20),
    "isFinal" BOOLEAN NOT NULL DEFAULT false,
    "metadata" JSONB,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP WITH TIME ZONE,
    CONSTRAINT "fk_asset_project" FOREIGN KEY ("projectId") REFERENCES public."Project"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_asset_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_asset_generationrequest" FOREIGN KEY ("generationRequestId") REFERENCES public."GenerationRequest"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_asset_projectid_createdat" ON public."Asset" USING btree ("projectId", "createdAt");
CREATE INDEX IF NOT EXISTS "idx_asset_userid" ON public."Asset" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_asset_generationrequestid" ON public."Asset" USING btree ("generationRequestId");
CREATE INDEX IF NOT EXISTS "idx_asset_type" ON public."Asset" USING btree ("type");

-- Add FK from GenerationRequest to Asset
ALTER TABLE public."GenerationRequest" ADD CONSTRAINT "fk_generationrequest_finalasset" FOREIGN KEY ("finalAssetId") REFERENCES public."Asset"("id") ON DELETE SET NULL ON UPDATE NO ACTION;

-- Defines 'AssetVersion' table
CREATE TABLE IF NOT EXISTS public."AssetVersion" (
    "id" UUID PRIMARY KEY NOT NULL,
    "assetId" UUID,
    "projectId" UUID,
    "versionNumber" INTEGER NOT NULL,
    "filePath" VARCHAR(1024),
    "stateData" JSONB,
    "description" TEXT,
    "createdByUserId" UUID,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_assetversion_asset" FOREIGN KEY ("assetId") REFERENCES public."Asset"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_assetversion_project" FOREIGN KEY ("projectId") REFERENCES public."Project"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_assetversion_user" FOREIGN KEY ("createdByUserId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_assetversion_assetid" ON public."AssetVersion" USING btree ("assetId");
CREATE INDEX IF NOT EXISTS "idx_assetversion_projectid" ON public."AssetVersion" USING btree ("projectId");
CREATE INDEX IF NOT EXISTS "idx_assetversion_assetid_version" ON public."AssetVersion" USING btree ("assetId", "versionNumber");
CREATE INDEX IF NOT EXISTS "idx_assetversion_projectid_version" ON public."AssetVersion" USING btree ("projectId", "versionNumber");

-- Defines 'AIModelFeedback' table
CREATE TABLE IF NOT EXISTS public."AIModelFeedback" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "generationRequestId" UUID,
    "modelVersionId" UUID,
    "rating" INTEGER CHECK ("rating" >= 1 AND "rating" <= 5),
    "comment" TEXT,
    "feedbackTimestamp" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "details" JSONB,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_aimodelfeedback_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelfeedback_genrequest" FOREIGN KEY ("generationRequestId") REFERENCES public."GenerationRequest"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_aimodelfeedback_modelversion" FOREIGN KEY ("modelVersionId") REFERENCES public."AIModelVersion"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_aimodelfeedback_userid" ON public."AIModelFeedback" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_aimodelfeedback_generationrequestid" ON public."AIModelFeedback" USING btree ("generationRequestId");
CREATE INDEX IF NOT EXISTS "idx_aimodelfeedback_modelversionid" ON public."AIModelFeedback" USING btree ("modelVersionId");

-- Level 6: Logging and Transaction Tables
--------------------------------------------------------------------------------
-- Defines 'CreditTransaction' table
CREATE TABLE IF NOT EXISTS public."CreditTransaction" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "odooInvoiceId" VARCHAR(255),
    "generationRequestId" UUID,
    "apiClientId" UUID,
    "amount" DECIMAL(10, 2) NOT NULL,
    "actionType" VARCHAR(50) NOT NULL,
    "description" TEXT,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "syncedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "fk_credittransaction_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_credittransaction_genrequest" FOREIGN KEY ("generationRequestId") REFERENCES public."GenerationRequest"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_credittransaction_apiclient" FOREIGN KEY ("apiClientId") REFERENCES public."APIClient"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);
CREATE INDEX IF NOT EXISTS "idx_credittransaction_userid_createdat" ON public."CreditTransaction" USING btree ("userId", "createdAt");
CREATE INDEX IF NOT EXISTS "idx_credittransaction_actiontype" ON public."CreditTransaction" USING btree ("actionType");

-- Defines 'UsageLog' table
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
CREATE INDEX IF NOT EXISTS "idx_usagelog_userid_timestamp" ON public."UsageLog" USING btree ("userId", "timestamp");
CREATE INDEX IF NOT EXISTS "idx_usagelog_actiontype" ON public."UsageLog" USING btree ("actionType");
CREATE INDEX IF NOT EXISTS "idx_usagelog_generationrequestid" ON public."UsageLog" USING btree ("generationRequestId");
CREATE INDEX IF NOT EXISTS "idx_usagelog_apiclientid" ON public."UsageLog" USING btree ("apiClientId");