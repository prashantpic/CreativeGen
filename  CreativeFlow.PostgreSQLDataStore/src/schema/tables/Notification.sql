-- Defines the schema for the 'Notification' table, storing system-generated notifications for users.

CREATE TABLE IF NOT EXISTS public."Notification" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "message" TEXT NOT NULL,
    "metadata" JSONB,
    "isRead" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_notification_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION
);

-- Indexes for the Notification table
CREATE INDEX IF NOT EXISTS "idx_notification_userid_isread_createdat" ON public."Notification" USING btree ("userId", "isRead", "createdAt");

-- Partial index for quick lookup of unread notifications, a common query pattern.
CREATE INDEX IF NOT EXISTS "idx_notification_userid_isread_unread" ON public."Notification" ("userId", "isRead") WHERE "isRead" = false;


COMMENT ON TABLE public."Notification" IS 'System notifications for users.';
COMMENT ON COLUMN public."Notification"."type" IS 'e.g., ''generation_complete'', ''collaboration_invite'', ''billing_alert'', ''system_update''.';
COMMENT ON COLUMN public."Notification"."metadata" IS 'JSON object with context (e.g., links to project/asset/team, generation status).';
COMMENT ON COLUMN public."Notification"."updatedAt" IS 'Can track when marked as read.';

/* PARTITIONING STRATEGY: This table is a candidate for RANGE partitioning on the 'createdAt' column based on data volume. */