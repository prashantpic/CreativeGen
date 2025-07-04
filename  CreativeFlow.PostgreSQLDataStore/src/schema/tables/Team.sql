-- Defines the schema for the 'Team' table, representing collaboration groups for team accounts.

CREATE TABLE IF NOT EXISTS public."Team" (
    "id" UUID PRIMARY KEY NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "ownerId" UUID NOT NULL,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_team_owner" FOREIGN KEY ("ownerId") REFERENCES public."User"("id") ON DELETE RESTRICT ON UPDATE NO ACTION
);

-- Indexes for the Team table
CREATE INDEX IF NOT EXISTS "idx_team_ownerid" ON public."Team" USING btree ("ownerId");

COMMENT ON TABLE public."Team" IS 'Collaboration group for team accounts.';
COMMENT ON COLUMN public."Team"."ownerId" IS 'The primary owner of the team. Restrict deletion if team still exists.';