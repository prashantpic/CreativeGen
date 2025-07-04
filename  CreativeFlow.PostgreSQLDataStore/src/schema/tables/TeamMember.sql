-- Defines the schema for the 'TeamMember' table, associating users with teams and their roles.

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

-- Indexes for the TeamMember table
CREATE INDEX IF NOT EXISTS "idx_teammember_teamid" ON public."TeamMember" USING btree ("teamId");
CREATE INDEX IF NOT EXISTS "idx_teammember_userid_role" ON public."TeamMember" USING btree ("userId", "role");

COMMENT ON TABLE public."TeamMember" IS 'Association between users and teams.';
COMMENT ON COLUMN public."TeamMember"."role" IS 'Role of the user within the team.';