-- Defines the schema for the 'Template' table.
-- Stores predefined system templates and user-saved private templates.

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

-- Indexes for the Template table
CREATE INDEX IF NOT EXISTS "idx_template_category_ispublic" ON public."Template" USING btree ("category", "isPublic");
CREATE INDEX IF NOT EXISTS "idx_template_userid" ON public."Template" USING btree ("userId");

-- GIN index for efficient searching within JSONB tags
CREATE INDEX IF NOT EXISTS "idx_template_tags_gin" ON public."Template" USING gin ("tags");


COMMENT ON TABLE public."Template" IS 'Predefined or user-saved creative templates.';
COMMENT ON COLUMN public."Template"."userId" IS 'Null for system templates. User ID for private templates.';
COMMENT ON COLUMN public."Template"."category" IS 'Category for organizing templates.';
COMMENT ON COLUMN public."Template"."previewUrl" IS 'MinIO path or external URL for preview image.';
COMMENT ON COLUMN public."Template"."sourceData" IS 'JSON structure defining the template content and layout for the editor.';
COMMENT ON COLUMN public."Template"."tags" IS 'JSON array of strings for search keywords.';
COMMENT ON COLUMN public."Template"."isPublic" IS 'True for system templates, false for private user templates.';