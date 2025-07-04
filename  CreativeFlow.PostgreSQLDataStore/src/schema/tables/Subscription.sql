-- Defines the schema for the 'Subscription' table, storing user subscription details,
-- typically synced from a billing system like Odoo.

CREATE TABLE IF NOT EXISTS public."Subscription" (
    "id" UUID PRIMARY KEY NOT NULL,
    "userId" UUID NOT NULL,
    "odooSaleOrderId" VARCHAR(255) NOT NULL,
    "planId" VARCHAR(50) NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK ("status" IN ('Active','Trial','Suspended','Cancelled','Expired')),
    "currentPeriodStart" TIMESTAMP WITH TIME ZONE NOT NULL,
    "currentPeriodEnd" TIMESTAMP WITH TIME ZONE NOT NULL,
    "paymentProvider" VARCHAR(50) NOT NULL CHECK ("paymentProvider" IN ('Stripe', 'PayPal', 'OdooManual')),
    "paymentProviderSubscriptionId" VARCHAR(255),
    "paymentMethodId" VARCHAR(255),
    "createdAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fk_subscription_user" FOREIGN KEY ("userId") REFERENCES public."User"("id") ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT "uq_subscription_odoo_so" UNIQUE ("odooSaleOrderId")
);

-- Indexes for the Subscription table
CREATE INDEX IF NOT EXISTS "idx_subscription_userid_status" ON public."Subscription" USING btree ("userId", "status");
CREATE INDEX IF NOT EXISTS "idx_subscription_currentperiodend" ON public."Subscription" USING btree ("currentPeriodEnd");

COMMENT ON TABLE public."Subscription" IS 'User subscription details, synced with Odoo.';
COMMENT ON COLUMN public."Subscription"."odooSaleOrderId" IS 'Reference to the Odoo Sale Order/Subscription record.';
COMMENT ON COLUMN public."Subscription"."planId" IS 'Identifier for the subscription plan (e.g., ''pro_monthly'', ''team_annual'').';
COMMENT ON COLUMN public."Subscription"."paymentProviderSubscriptionId" IS 'Reference to the subscription ID in the payment provider (e.g., Stripe, PayPal).';