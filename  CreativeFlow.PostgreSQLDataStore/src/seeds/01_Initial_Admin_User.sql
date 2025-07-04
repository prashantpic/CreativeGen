-- Seeds an initial administrative user account for platform setup and management.
-- This script is designed to be idempotent.

INSERT INTO public."User" (
    "id",
    "email",
    "passwordHash",
    "isEmailVerified",
    "fullName",
    "username",
    "subscriptionTier",
    "creditBalance",
    "createdAt",
    "updatedAt"
) VALUES (
    gen_random_uuid(),
    'admin@creativeflow.ai',
    '$2b$12$D4T2p.y/Sg9y.AdGCIHwU.sSjFvF0kQvFkRz3RzXjXjXjXjXjXjXj', -- Replace with a valid bcrypt hash for a secure initial password.
    true,
    'Admin User',
    'admin',
    'Enterprise',
    9999.99,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
ON CONFLICT (email) DO NOTHING;