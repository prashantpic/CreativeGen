-- Defines the schema for the 'Workbench' table, a container for organizing creative projects.

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

-- Indexes for the Workbench table
CREATE INDEX IF NOT EXISTS "idx_workbench_userid" ON public."Workbench" USING btree ("userId");

COMMENT ON TABLE public."Workbench" IS 'Container for organizing creative projects.';
COMMENT ON COLUMN public."Workbench"."defaultBrandKitId" IS 'Optional default brand kit for new projects in this workbench.';