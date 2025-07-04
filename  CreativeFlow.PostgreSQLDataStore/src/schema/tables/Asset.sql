-- Defines the schema for the 'Asset' table.
-- Represents a specific creative asset file (uploaded or AI-generated).

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

-- Indexes for the Asset table
CREATE INDEX IF NOT EXISTS "idx_asset_projectid_createdat" ON public."Asset" USING btree ("projectId", "createdAt");
CREATE INDEX IF NOT EXISTS "idx_asset_userid" ON public."Asset" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_asset_generationrequestid" ON public."Asset" USING btree ("generationRequestId");
CREATE INDEX IF NOT EXISTS "idx_asset_type" ON public."Asset" USING btree ("type");


COMMENT ON TABLE public."Asset" IS 'Represents a specific creative asset file (uploaded or AI-generated).';
COMMENT ON COLUMN public."Asset"."projectId" IS 'Asset can exist independently of a project (e.g., uploaded to user library).';
COMMENT ON COLUMN public."Asset"."generationRequestId" IS 'Link to the generation request if this asset was AI-generated.';
COMMENT ON COLUMN public."Asset"."type" IS '''Derived'' for assets created by editing existing ones.';
COMMENT ON COLUMN public."Asset"."filePath" IS 'Path in MinIO object storage.';
COMMENT ON COLUMN public."Asset"."isFinal" IS 'True if this is the user-selected final asset from a generation or a completed edited version.';
COMMENT ON COLUMN public."Asset"."metadata" IS 'Optional metadata (e.g., dominant colors, tags, source generation parameters if AI-generated).';
COMMENT ON COLUMN public."Asset"."deletedAt" IS 'Timestamp for soft delete.';