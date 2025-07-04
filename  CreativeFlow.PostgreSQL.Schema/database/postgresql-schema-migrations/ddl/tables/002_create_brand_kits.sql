-- DDL for creating the 'brand_kits' table
-- This script is for reference and manual setup;
-- the authoritative schema is managed by Alembic migrations.

CREATE TABLE brand_kits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    userId UUID NOT NULL,
    teamId UUID,
    name VARCHAR(100) NOT NULL,
    colors JSONB NOT NULL DEFAULT '[]'::jsonb,
    fonts JSONB NOT NULL DEFAULT '[]'::jsonb,
    logos JSONB,
    stylePreferences JSONB,
    isDefault BOOLEAN NOT NULL DEFAULT FALSE,
    createdAt TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_brand_kits_userId_users FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_brand_kits_teamId_teams FOREIGN KEY (teamId) REFERENCES teams(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_brandkit_userid ON brand_kits (userId);
CREATE INDEX idx_brandkit_teamid ON brand_kits (teamId);
CREATE INDEX idx_brandkit_colors_gin ON brand_kits USING GIN (colors);
CREATE INDEX idx_brandkit_fonts_gin ON brand_kits USING GIN (fonts);

-- Trigger for updatedAt timestamp
CREATE TRIGGER update_brand_kits_updated_at
BEFORE UPDATE ON brand_kits
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();