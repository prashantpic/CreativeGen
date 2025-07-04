-- Defines the schema for the 'CreditTransaction' table.
-- Records credit purchases and usage, often synced from Odoo.

CREATE TABLE IF NOT EXISTS public."CreditTransaction" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "odooInvoiceId" VARCHAR(255),
    "generationRequestId" UUID,
    "apiClientId" UUID,
    "amount" DECIMAL(10, 2) NOT NULL,
    "actionType" VARCHAR(50) NOT NULL,
    "description" TEXT,
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "syncedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_credittransaction_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "fk_credittransaction_genrequest" FOREIGN KEY ("generationRequestId") REFERENCES public."GenerationRequest"("id") ON DELETE SET NULL ON UPDATE NO ACTION,
    CONSTRAINT "fk_credittransaction_apiclient" FOREIGN KEY ("apiClientId") REFERENCES public."APIClient"("id") ON DELETE SET NULL ON UPDATE NO ACTION
);

-- Indexes for the CreditTransaction table
CREATE INDEX IF NOT EXISTS "idx_credittransaction_userid_createdat" ON public."CreditTransaction" USING btree ("userId", "createdAt");
CREATE INDEX IF NOT EXISTS "idx_credittransaction_actiontype" ON public."CreditTransaction" USING btree ("actionType");


COMMENT ON TABLE public."CreditTransaction" IS 'Credit usage and purchase records, synced from Odoo.';
COMMENT ON COLUMN public."CreditTransaction"."odooInvoiceId" IS 'Reference to the Odoo Invoice record if applicable.';
COMMENT ON COLUMN public."CreditTransaction"."amount" IS 'Credit amount (+ for purchase/refund, - for usage).';
COMMENT ON COLUMN public."CreditTransaction"."actionType" IS 'e.g., ''purchase'', ''sample_generation'', ''final_generation'', ''export_hd'', ''api_generation'', ''refund''.';
COMMENT ON COLUMN public."CreditTransaction"."syncedAt" IS 'Timestamp when this record was synced from Odoo.';

/* PARTITIONING STRATEGY: This table is a candidate for RANGE partitioning on the 'createdAt' column based on data volume. Example: PARTITION BY RANGE (createdAt) */