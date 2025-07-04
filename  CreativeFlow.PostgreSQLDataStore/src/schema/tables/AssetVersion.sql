-- Defines the schema for the 'AssetVersion' table.
-- Tracks version history for creative assets or project states.

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

-- Indexes for the AssetVersion table
CREATE INDEX IF NOT EXISTS "idx_assetversion_assetid" ON public."AssetVersion" USING btree ("assetId");
CREATE INDEX IF NOT EXISTS "idx_assetversion_projectid" ON public."AssetVersion" USING btree ("projectId");
CREATE INDEX IF NOT EXISTS "idx_assetversion_assetid_version" ON public."AssetVersion" USING btree ("assetId", "versionNumber");
CREATE INDEX IF NOT EXISTS "idx_assetversion_projectid_version" ON public."AssetVersion" USING btree ("projectId", "versionNumber");

COMMENT ON TABLE public."AssetVersion" IS 'Version history for creative assets or project states.';
COMMENT ON COLUMN public."AssetVersion"."assetId" IS 'Link to the parent Asset this version belongs to.';
COMMENT ON COLUMN public."AssetVersion"."projectId" IS 'Link to the Project this version belongs to (could be a project state version).';
COMMENT ON COLUMN public."AssetVersion"."filePath" IS 'Path in MinIO object storage if this version saves a specific file state.';
COMMENT ON COLUMN public."AssetVersion"."stateData" IS 'JSON data representing the project or asset state at this version point.';
COMMENT ON COLUMN public."AssetVersion"."createdByUserId" IS 'User who created this version.';