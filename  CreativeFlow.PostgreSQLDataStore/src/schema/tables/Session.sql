-- Defines the schema for the 'Session' table, storing active user authentication sessions.

CREATE TABLE IF NOT EXISTS public."Session" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "deviceInfo" VARCHAR(255) NOT NULL,
    "ipAddress" VARCHAR(45) NOT NULL,
    "userAgent" TEXT,
    "lastActivity" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expiresAt" TIMESTAMP WITH TIME ZONE NOT NULL,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_session_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION
);

-- Indexes for the Session table
CREATE INDEX IF NOT EXISTS "idx_session_userid_expiresat" ON public."Session" USING btree ("userId", "expiresAt");
CREATE INDEX IF NOT EXISTS "idx_session_expiresat" ON public."Session" USING btree ("expiresAt");
CREATE INDEX IF NOT EXISTS "idx_session_lastactivity" ON public."Session" USING btree ("lastActivity");


COMMENT ON TABLE public."Session" IS 'User authentication sessions.';
COMMENT ON COLUMN public."Session"."ipAddress" IS 'Supports IPv4 and IPv6.';
COMMENT ON COLUMN public."Session"."userAgent" IS 'Full user agent string for device identification.';
COMMENT ON INDEX public."Session"."idx_session_expiresat" IS 'For cleaning up expired sessions.';