-- Defines the schema for the 'BrandKit' table, storing brand assets (colors, fonts, logos)
-- and preferences for users or teams.

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

-- Indexes for the BrandKit table
CREATE INDEX IF NOT EXISTS "idx_brandkit_userid" ON public."BrandKit" USING btree ("userId");
CREATE INDEX IF NOT EXISTS "idx_brandkit_teamid" ON public."BrandKit" USING btree ("teamId");

-- GIN indexes for efficient searching within JSONB columns
CREATE INDEX IF NOT EXISTS "idx_brandkit_colors_gin" ON public."BrandKit" USING gin ("colors");
CREATE INDEX IF NOT EXISTS "idx_brandkit_fonts_gin" ON public."BrandKit" USING gin ("fonts");


COMMENT ON TABLE public."BrandKit" IS 'Collection of brand assets and preferences. Can belong to a user or a team.';
COMMENT ON COLUMN public."BrandKit"."userId" IS 'User who owns this brand kit. For team brand kits, this might be the creator or the owning team''s owner.';
COMMENT ON COLUMN public."BrandKit"."teamId" IS 'Optional: Team this brand kit belongs to.';
COMMENT ON COLUMN public."BrandKit"."colors" IS 'JSON array of color definitions, e.g., [{ "name": "Primary", "hex": "#FF0000", "variable": "--color-primary" }].';
COMMENT ON COLUMN public."BrandKit"."fonts" IS 'JSON array of font definitions, e.g., [{ "name": "Heading", "family": "Arial", "url": "..." }].';
COMMENT ON COLUMN public."BrandKit"."logos" IS 'JSON array of logo asset references (MinIO paths), e.g., [{ "name": "Main Logo", "path": "minio_path", "format": "png" }].';
COMMENT ON COLUMN public."BrandKit"."stylePreferences" IS 'JSON object for default style preferences like tone, industry hints etc.';