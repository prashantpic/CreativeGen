-- DDL for creating the 'users' table
-- This script is for reference and manual setup;
-- the authoritative schema is managed by Alembic migrations.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    passwordHash VARCHAR(255),
    socialProvider VARCHAR(50) CHECK (socialProvider IN ('google', 'facebook', 'apple')),
    socialProviderId VARCHAR(255),
    isEmailVerified BOOLEAN NOT NULL DEFAULT FALSE,
    emailVerificationToken VARCHAR(255),
    passwordResetToken VARCHAR(255),
    passwordResetExpires TIMESTAMP WITHOUT TIME ZONE,
    fullName VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    profilePictureUrl VARCHAR(1024),
    languagePreference VARCHAR(10) NOT NULL DEFAULT 'en-US',
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    mfaEnabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfaSecret VARCHAR(255), -- Application layer encryption required
    subscriptionTier VARCHAR(20) NOT NULL DEFAULT 'Free' CHECK (subscriptionTier IN ('Free','Pro','Team','Enterprise')),
    creditBalance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    lastLoginAt TIMESTAMP WITHOUT TIME ZONE,
    createdAt TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deletedAt TIMESTAMP WITHOUT TIME ZONE,
    
    CONSTRAINT uq_user_social UNIQUE (socialProvider, socialProviderId)
);

-- Indexes
CREATE INDEX idx_user_email_unique ON users (email);
CREATE INDEX idx_user_username_unique ON users (username) WHERE username IS NOT NULL;
CREATE INDEX idx_user_social_unique ON users (socialProvider, socialProviderId) WHERE socialProvider IS NOT NULL AND socialProviderId IS NOT NULL;
CREATE INDEX idx_user_subscriptiontier ON users (subscriptionTier);
CREATE INDEX idx_user_deletedat ON users (deletedAt) WHERE deletedAt IS NOT NULL;
CREATE INDEX idx_user_languagepreference ON users (languagePreference);

-- A trigger to automatically update the 'updatedAt' timestamp on row updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updatedAt = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();