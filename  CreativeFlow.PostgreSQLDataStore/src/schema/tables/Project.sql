-- Defines the schema for the 'Project' table, representing individual creative projects.

CREATE TABLE IF NOT EXISTS public."Project" (
    "id" UUID PRIMARY KEY NOT NULL,
    "workbenchId" UUID NOT NULL,
    "userId" UUID NOT NULL, -- Denormalized from Workbench for query performance.
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

-- Indexes for the Project table
CREATE INDEX IF NOT EXISTS "idx_project_workbenchid" ON public."Project" USING btree ("workbenchId");
CREATE INDEX IF NOT EXISTS "idx_project_userid" ON public."Project" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_project_updatedat" ON public."Project" USING btree ("updatedAt");


COMMENT ON TABLE public."Project" IS 'Creative project containing assets and generation requests.';
COMMENT ON COLUMN public."Project"."userId" IS 'Denormalized from Workbench for query performance. Application logic should ensure consistency with Workbench.userId.';
COMMENT ON COLUMN public."Project"."brandKitId" IS 'Optional brand kit override for this project.';
COMMENT ON COLUMN public."Project"."targetPlatform" IS 'Primary target platform for this project, e.g., ''InstagramStory'', ''TikTok''.';
COMMENT ON COLUMN public."Project"."collaborationState" IS 'JSON representation of the creative canvas state, potentially using CRDT representation for collaborative projects.';
COMMENT ON COLUMN public."Project"."deletedAt" IS 'Timestamp for soft delete.';