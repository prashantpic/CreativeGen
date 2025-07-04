# Software Design Specification: CreativeFlow.OdooERPPlatform

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specifications for the `CreativeFlow.OdooERPPlatform` repository. This repository encompasses the Odoo 18+ customizations and configurations required to support core business logic for the CreativeFlow AI platform. This includes functionalities related to user data synchronization for administrative views, subscription management, billing and invoicing, credit system logic, product/plan catalog, and the customer support helpdesk and knowledge base.

### 1.2 Scope
The scope of this SDS is limited to the custom Odoo modules developed and configurations applied within the `CreativeFlow.OdooERPPlatform` repository. It details the models, views, controllers, services, and data specific to these customizations. Standard Odoo modules (e.g., `base`, `account`, `sale_subscription`, `helpdesk`, `knowledge`, `payment`) are leveraged as dependencies, and this document focuses on how they are extended or configured for CreativeFlow's needs. Interactions with external microservices are primarily through adapter layers or asynchronous messaging, with Odoo acting as the backend for specific business operations.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **Odoo:** Open-source suite of business applications.
*   **ERP:** Enterprise Resource Planning.
*   **SDS:** Software Design Specification.
*   **ORM:** Object-Relational Mapper.
*   **ACL:** Access Control List.
*   **MVC:** Model-View-Controller.
*   **XML-RPC:** XML Remote Procedure Call.
*   **JSON-RPC:** JSON Remote Procedure Call.
*   **CI/CD:** Continuous Integration / Continuous Deployment.
*   **PWA:** Progressive Web Application.
*   **MinIO:** High-performance, S3 compatible object storage.
*   **CF:** CreativeFlow.
*   **KPI:** Key Performance Indicator.
*   **RTL:** React Testing Library.
*   **TS:** TypeScript.
*   **ETL:** Extract, Transform, Load.
*   **UAT:** User Acceptance Testing.
*   **SAST:** Static Application Security Testing.
*   **DAST:** Dynamic Application Security Testing.
*   **PII:** Personally Identifiable Information.
*   **GDPR:** General Data Protection Regulation.
*   **CCPA:** California Consumer Privacy Act.
*   **RPO:** Recovery Point Objective.
*   **RTO:** Recovery Time Objective.
*   **DR:** Disaster Recovery.
*   **IaC:** Infrastructure as Code.
*   **SLA:** Service Level Agreement.
*   **SLO:** Service Level Objective.
*   **SOP:** Standard Operating Procedure.

## 2. System Overview
The `CreativeFlow.OdooERPPlatform` acts as the central nervous system for many core business operations of the CreativeFlow AI platform. It leverages Odoo 18+'s robust framework to manage:
*   **Subscription & Billing:** Handling different subscription tiers (Free, Pro, Team, Enterprise), recurring billing, payment processing via Stripe and PayPal, credit management, and invoicing.
*   **Customer Support:** Providing a helpdesk system for ticket management and a knowledge base for self-service support.
*   **Content Management (Admin):** Managing the platform's template catalog, if configured to do so.
*   **User Data (Admin Context):** Storing or syncing essential user data for administrative and billing purposes within Odoo, complementing the primary user management system which might be external.

Odoo interacts with other platform services often through asynchronous mechanisms (e.g., webhooks from payment gateways, messages via RabbitMQ for job orchestration) or via adapter services that call its XML-RPC/JSON-RPC API. This design minimizes Odoo's direct involvement in real-time critical paths of the user-facing application where possible, ensuring scalability and resilience of the overall platform.

The repository contains custom Odoo modules prefixed with `creativeflow_` to extend and tailor standard Odoo functionality.

## 3. Module Design

This section details the design of each custom Odoo module within this repository.

### 3.1 `creativeflow_core` Module
This module provides core extensions and utilities shared across other CreativeFlow Odoo modules.

#### 3.1.1 Purpose
To provide foundational customizations, primarily extending Odoo's `res.partner` model to include fields relevant to CreativeFlow's administrative views within Odoo.

#### 3.1.2 Models

##### 3.1.2.1 `res_partner_extension.py` (`res.partner`)
*   **Inheritance:** `_inherit = 'res.partner'`
*   **Fields:**
    | Name                            | Odoo Type     | Attributes/Description                                                                      | Requirement IDs                                |
    | :------------------------------ | :------------ | :------------------------------------------------------------------------------------------ | :--------------------------------------------- |
    | `cf_synced_credit_balance`      | `fields.Float`| `string="CF Credit Balance (Synced)"`, `readonly=True`, `help="User's credit balance synced from the platform."` | `comp.backend.odoo.userMgmtModule`           |
    | `cf_synced_subscription_tier` | `fields.Char` | `string="CF Subscription Tier (Synced)"`, `readonly=True`, `help="User's subscription tier synced from the platform."` | `comp.backend.odoo.userMgmtModule`           |
*   **Methods:**
    *   `action_sync_with_platform(self)`:
        *   **Parameters:** `self`
        *   **Return Type:** `None` (or boolean for success/failure)
        *   **Logic Description:** Placeholder method. Intended to be called by an external system (e.g., an adapter service) or an Odoo cron job to update `cf_synced_credit_balance` and `cf_synced_subscription_tier` from the main CreativeFlow platform's user database or billing service. This module itself does not initiate the sync but provides the fields for storing synced data. For actual sync, an API endpoint (e.g., XML-RPC) would be exposed by this module or a dedicated sync module.
        *   **Error Handling:** Log errors if sync fails.
        *   **Integration Points:** Potentially called by an external service or cron job.
    *   **Notes:** The primary source of truth for credit balance and subscription tier resides outside Odoo (managed by `Subscription & Billing Service` and `User Account & Profile Service`). These fields in `res.partner` are for display and reference within Odoo's admin interface.

#### 3.1.3 Views

##### 3.1.3.1 `res_partner_views_extension.xml`
*   **Purpose:** Extend the `res.partner` form and tree views to display CreativeFlow-specific synced fields.
*   **Inherited Views:**
    *   `base.view_partner_form`
    *   `base.view_partner_tree` (optional, if needed in list view)
*   **Key Elements Added/Modified:**
    *   In Partner Form View:
        *   Add `cf_synced_subscription_tier` field, typically within a "CreativeFlow" group or tab.
        *   Add `cf_synced_credit_balance` field, typically within the same group or tab.
        *   (Optional) Add a button to manually trigger `action_sync_with_platform` (for admin/debug purposes).
    *   In Partner Tree View (Optional):
        *   Add columns for `cf_synced_subscription_tier` and `cf_synced_credit_balance`.

#### 3.1.4 Security

##### 3.1.4.1 `ir.model.access.csv`
*   **Purpose:** Define access rights for the extended fields on `res.partner`.
*   **Key Access Rights:**
    *   Ensure appropriate user groups (e.g., Sales / Administrator, Billing Manager) have read access to `cf_synced_credit_balance` and `cf_synced_subscription_tier` on `res.partner`. Write access should be restricted as these fields are intended to be synced from an external source.

#### 3.1.5 Manifest (`__manifest__.py`)
*   **`name`**: "CreativeFlow Core Extensions"
*   **`version`**: "1.0.0"
*   **`summary`**: "Core extensions for CreativeFlow integration with Odoo."
*   **`category`**: "CreativeFlow/Core"
*   **`depends`**: `['base', 'mail']`
*   **`data`**: `['security/ir.model.access.csv', 'views/res_partner_views_extension.xml']`
*   **`installable`**: `True`
*   **`application`**: `False`
*   **`auto_install`**: `False`

### 3.2 `creativeflow_subscription_billing` Module
This module handles subscription management, billing logic, credit system, and payment gateway integration.

#### 3.2.1 Purpose
To manage CreativeFlow subscription plans, process payments, handle credit balances, and integrate with payment providers (Stripe, PayPal) within the Odoo environment, fulfilling `Section 3.4 (Subscription and Billing functions often in Odoo)` and `INT-003 (Payment processing integrated with Odoo)`.

#### 3.2.2 Models

##### 3.2.2.1 `res_partner_billing_extension.py` (`res.partner`)
*   **Inheritance:** `_inherit = 'res.partner'`
*   **Fields:**
    | Name                         | Odoo Type        | Attributes/Description                                                                              | Requirement IDs                     |
    | :--------------------------- | :--------------- | :-------------------------------------------------------------------------------------------------- | :---------------------------------- |
    | `cf_credit_balance`          | `fields.Float`   | `string="CF Credit Balance (Odoo Managed)"`, `digits=(16, 4)`, `default=0.0`, `help="User's credit balance managed within Odoo for platform features."` | `comp.backend.odoo.billingSubModule` |
    | `cf_subscription_ids`      | `fields.One2many`| `comodel_name='sale.subscription'`, `inverse_name='partner_id'`, `string="CF Subscriptions"`, `readonly=True` | `comp.backend.odoo.billingSubModule` |
    | `cf_credit_log_ids`          | `fields.One2many`| `comodel_name='creativeflow.credit.log'`, `inverse_name='partner_id'`, `string="CF Credit Logs"`, `readonly=True` | `comp.backend.odoo.billingSubModule` |
*   **Methods:**
    *   `add_credits(self, amount, description=None, force_commit=False)`:
        *   **Parameters:** `amount` (float, positive), `description` (str, optional), `force_commit` (bool, if True, commits the transaction immediately).
        *   **Return Type:** `self.env['creativeflow.credit.log']` (the created log record)
        *   **Logic Description:**
            1.  Validate `amount` > 0.
            2.  Update `self.cf_credit_balance` by adding `amount`.
            3.  Call `_create_credit_transaction_log(amount, description, 'addition')`.
            4.  If `force_commit`, call `self.env.cr.commit()`.
        *   **Error Handling:** Raise `UserError` if amount is not positive.
    *   `deduct_credits(self, amount, description=None, related_document_model=None, related_document_id=None, force_commit=False)`:
        *   **Parameters:** `amount` (float, positive), `description` (str, optional), `related_document_model` (str, optional), `related_document_id` (int, optional), `force_commit` (bool).
        *   **Return Type:** `self.env['creativeflow.credit.log']` (the created log record) or `False` if insufficient credits.
        *   **Logic Description:**
            1.  Validate `amount` > 0.
            2.  Check if `self.cf_credit_balance >= amount`. If not, raise `UserError` "Insufficient credits." or return `False` depending on desired behavior.
            3.  Update `self.cf_credit_balance` by subtracting `amount`.
            4.  Call `_create_credit_transaction_log(-amount, description, 'deduction', related_document_model, related_document_id)`.
            5.  If `force_commit`, call `self.env.cr.commit()`.
        *   **Error Handling:** Raise `UserError` for negative amount or insufficient credits.
    *   `_create_credit_transaction_log(self, amount, description, transaction_type, related_document_model=None, related_document_id=None)`:
        *   **Parameters:** `amount` (float), `description` (str), `transaction_type` (str: 'addition', 'deduction', 'initial', 'refund'), `related_document_model`, `related_document_id`.
        *   **Return Type:** `self.env['creativeflow.credit.log']`
        *   **Logic Description:** Create a new record in `creativeflow.credit.log` with `partner_id=self.id`, `amount`, `description`, `transaction_type`, `date_transaction=fields.Datetime.now()`, and related document if provided.

##### 3.2.2.2 `sale_subscription_extension.py` (`sale.subscription`)
*   **Inheritance:** `_inherit = 'sale.subscription'`
*   **Fields:**
    | Name                                | Odoo Type     | Attributes/Description                                                                        | Requirement IDs                     |
    | :---------------------------------- | :------------ | :-------------------------------------------------------------------------------------------- | :---------------------------------- |
    | `cf_platform_plan_id`               | `fields.Char` | `string="CF Platform Plan ID"`, `help="Identifier of the corresponding plan on the CreativeFlow platform."` | `Section 3.4`                       |
    | `cf_credit_allotment_per_cycle`     | `fields.Float`| `string="CF Credits Allotment/Cycle"`, `help="Credits to add to user's Odoo balance on successful renewal."` | `Section 3.4`                       |
    | `cf_last_sync_status_to_platform` | `fields.Datetime`| `string="Last Synced to Platform"`, `readonly=True`                                           | `Section 3.4`                       |
*   **Methods:**
    *   `_recurring_invoice(self, automatic=False)`:
        *   **Return Type:** `super()._recurring_invoice(automatic=automatic)`
        *   **Logic Description:**
            1.  Call `super()._recurring_invoice(automatic=automatic)` to generate the standard renewal invoice.
            2.  If invoice creation is successful and `self.cf_credit_allotment_per_cycle > 0`:
                *   Attempt to find/confirm payment for the newly created invoice.
                *   If payment is confirmed (or if policy allows credit addition before payment for certain plans):
                    *   Call `self.partner_id.add_credits(self.cf_credit_allotment_per_cycle, description=f"Credit allotment for subscription {self.name}")`.
            3.  Trigger `action_sync_status_to_platform()` or enqueue a job for it.
        *   **Error Handling:** Log errors during credit addition.
    *   `action_sync_status_to_platform(self)`:
        *   **Logic Description:** Placeholder. This method would be responsible for pushing the subscription status (e.g., active, cancelled, in_grace_period) and `currentPeriodEnd` to the main CreativeFlow platform via an API call to an adapter service or directly if Odoo is authoritative. Updates `cf_last_sync_status_to_platform`.
        *   **Note:** This method should be called on relevant subscription state changes (`write` method override) or via cron.
    *   `_handle_<y_bin_359>Payment_failure(self, invoice)`:
        *   **Logic Description:** Called when a recurring payment fails. Implement dunning logic: send dunning emails (using Odoo mail templates), schedule retries. If retries exhausted, change subscription state (e.g., to 'suspended' or cancel it). This might interact with `billing_service.py`.
        *   **Requirement IDs:** `INT-003` (failed payment retry logic)

##### 3.2.2.3 `account_payment_acquirer_extension.py` (`payment.acquirer`)
*   **Inheritance:** `_inherit = 'payment.acquirer'`
*   **Fields:**
    | Name                   | Odoo Type     | Attributes/Description                                                       | Requirement IDs |
    | :--------------------- | :------------ | :--------------------------------------------------------------------------- | :-------------- |
    | `cf_custom_config`     | `fields.Text` | `string="CF Custom Configuration"`, `help="JSON or text field for specific acquirer configurations needed by CreativeFlow."` | `INT-003`       |
    | `cf_webhook_secret`    | `fields.Char` | `string="CF Webhook Secret"`, `help="Secret key for verifying webhook signatures, stored securely."` | `INT-003`       |
*   **Methods:** (Mostly relies on base Odoo payment acquirer logic, extensions are for configuration or specialized webhook validation if needed).
    *   `_stripe_verify_webhook_signature(self, signature_header, payload_body)`:
        *   **Logic:** Implement Stripe webhook signature verification using `cf_webhook_secret`.
    *   `_paypal_verify_webhook_signature(self, headers, payload_body)`:
        *   **Logic:** Implement PayPal webhook signature verification logic.

##### 3.2.2.4 `creativeflow_credit_log.py` (`creativeflow.credit.log`) - New Model
*   **Model:** `_name = 'creativeflow.credit.log'`
*   **Description:** `_description = 'CreativeFlow Credit Transaction Log'`
*   **Order:** `_order = 'date_transaction desc, id desc'`
*   **Fields:**
    | Name                       | Odoo Type      | Attributes/Description                                                         |
    | :------------------------- | :------------- | :----------------------------------------------------------------------------- |
    | `partner_id`               | `fields.Many2one`| `comodel_name='res.partner'`, `string="Partner"`, `required=True`, `ondelete='cascade'` |
    | `amount`                   | `fields.Float` | `string="Amount"`, `digits=(16, 4)`, `required=True`                             |
    | `description`              | `fields.Text`  | `string="Description"`                                                         |
    | `transaction_type`         | `fields.Selection`| `selection=[('addition', 'Addition'), ('deduction', 'Deduction'), ('initial', 'Initial Balance'), ('refund', 'Refund')]`, `string="Type"`, `required=True` |
    | `date_transaction`         | `fields.Datetime`| `string="Transaction Date"`, `required=True`, `default=fields.Datetime.now`  |
    | `related_document_model`   | `fields.Char`  | `string="Related Document Model"`                                              |
    | `related_document_id`    | `fields.Integer`| `string="Related Document ID"`                                                 |
    | `related_document_display` | `fields.Char`  | `string="Related Document"`, `compute='_compute_related_document_display'`   |
*   **Methods:**
    *   `_compute_related_document_display(self)`:
        *   **Logic:** For each record, if `related_document_model` and `related_document_id` are set, try to fetch the `display_name` of the related record and set it to `related_document_display`.

#### 3.2.3 Controllers

##### 3.2.3.1 `payment_webhook_controller.py` (`PaymentWebhookController`)
*   **Inheritance:** `odoo.http.Controller`
*   **Routes & Methods:**
    *   `stripe_webhook(self, **kwargs)`:
        *   **Route:** `/payment/stripe/webhook`, `auth='public'`, `methods=['POST']`, `csrf=False`, `type='http'`
        *   **Logic Description:**
            1.  Retrieve raw request payload and `Stripe-Signature` header.
            2.  Fetch the Stripe acquirer and its `cf_webhook_secret`.
            3.  Verify webhook signature using `stripe.Webhook.construct_event`. If verification fails, log error and return HTTP 400.
            4.  Get the event object from `construct_event`.
            5.  Call `request.env['billing.service'].sudo().process_stripe_payment_event(event_object, acquirer_id)` (Service method to be defined).
            6.  Return HTTP 200 OK.
        *   **Error Handling:** Log signature verification failures, event processing errors. Return appropriate HTTP status codes.
        *   **Requirement IDs:** `INT-003`
    *   `paypal_webhook(self, **kwargs)`:
        *   **Route:** `/payment/paypal/webhook`, `auth='public'`, `methods=['POST']`, `csrf=False`, `type='http'`
        *   **Logic Description:**
            1.  Retrieve raw request payload and PayPal-specific headers for verification.
            2.  Fetch the PayPal acquirer and its `cf_webhook_secret` or relevant credentials.
            3.  Verify webhook integrity/authenticity (e.g., by sending event back to PayPal for verification, or using SDK methods if available). If verification fails, log error and return HTTP 400.
            4.  Parse the event data.
            5.  Call `request.env['billing.service'].sudo().process_paypal_payment_event(event_data, acquirer_id)` (Service method to be defined).
            6.  Return HTTP 200 OK.
        *   **Error Handling:** Log verification failures, event processing errors.
        *   **Requirement IDs:** `INT-003`

#### 3.2.4 Services

##### 3.2.4.1 `billing_service.py` (`BillingService`)
*   **Inheritance:** `odoo.addons.component.core.Component` (if using OCA components) or standard Python class instantiated as a service. For simplicity, assuming standard service pattern.
    *   Could also be model methods on `payment.transaction` or `sale.subscription` if logic is tightly coupled.
*   **Class Name:** `BillingService` (conceptual, actual implementation might be methods on models or a separate class managed by Odoo's service registry if using newer patterns).
*   **Methods:**
    *   `process_stripe_payment_event(self, event_object, acquirer_id)`:
        *   **Parameters:** `event_object` (Stripe event), `acquirer_id` (ID of Stripe payment acquirer).
        *   **Logic Description:**
            *   Identify event type (e.g., `invoice.payment_succeeded`, `invoice.payment_failed`, `customer.subscription.updated`, `charge.refunded`).
            *   Based on event type:
                *   `invoice.payment_succeeded`: Find related Odoo `sale.subscription` or `account.move` (invoice). Mark invoice as paid. If it's a subscription renewal, call `partner.add_credits()` if `cf_credit_allotment_per_cycle` is defined on the subscription. Trigger invoice generation/sending via Odoo's standard mechanisms.
                *   `invoice.payment_failed`: Find related invoice/subscription. Log failure. Initiate dunning process (e.g., call `subscription._handle_payment_failure()`).
                *   `customer.subscription.updated/deleted`: Update corresponding `sale.subscription` status in Odoo (e.g., active, cancelled). Trigger `action_sync_status_to_platform()` on the subscription.
                *   `charge.refunded`: Find related payment/invoice. Create credit note in Odoo. Adjust partner credits if applicable.
        *   **Error Handling:** Log any errors during processing. Ensure idempotency (e.g., check if event ID already processed).
    *   `process_paypal_payment_event(self, event_data, acquirer_id)`:
        *   **Parameters:** `event_data` (parsed PayPal event), `acquirer_id`.
        *   **Logic Description:** Similar to `process_stripe_payment_event`, but tailored for PayPal event types and data structures.
    *   `apply_taxes_to_invoice_line(self, invoice_line)`:
        *   **Parameters:** `invoice_line` (Odoo `account.move.line` record).
        *   **Logic Description:** Ensure correct taxes are applied based on product, partner fiscal position, and Odoo tax configuration. Odoo's standard tax computation should handle most of this automatically if products and fiscal positions are correctly set up. This service method might be for overrides or complex scenarios.
        *   **Requirement IDs:** `INT-003` (Tax calculation)
    *   `initiate_dunning_for_subscription(self, subscription_id)`:
        *   **Parameters:** `subscription_id` (Odoo `sale.subscription` ID).
        *   **Logic Description:** Manage the dunning process for a subscription with a failed payment. This could involve:
            1.  Checking the number of past retries.
            2.  Sending dunning emails using Odoo mail templates.
            3.  Potentially scheduling a payment retry via the payment acquirer if supported.
            4.  Updating the subscription status (e.g., 'pending_payment', 'suspended') after a certain number of failures.
        *   **Requirement IDs:** `INT-003` (failed payment retry logic, dunning emails)

#### 3.2.5 Data Files

##### 3.2.5.1 `data/payment_acquirer_data.xml`
*   **Purpose:** Define Stripe and PayPal payment acquirers.
*   **Key Records:**
    *   `payment.acquirer` record for Stripe:
        *   `name`: "Stripe CreativeFlow"
        *   `provider`: "stripe"
        *   `state`: "test" (initially, can be changed to "enabled" in production)
        *   `stripe_publishable_key`: Placeholder (e.g., `pk_test_YOUR_STRIPE_KEY`)
        *   `stripe_secret_key`: Placeholder (e.g., `sk_test_YOUR_STRIPE_SECRET`)
        *   `cf_webhook_secret`: Placeholder (e.g., `whsec_YOUR_STRIPE_WEBHOOK_SECRET`) - To be configured securely in Odoo UI.
        *   Other fields: `journal_id`, `company_id`, `payment_flow`, etc.
    *   `payment.acquirer` record for PayPal:
        *   `name`: "PayPal CreativeFlow"
        *   `provider`: "paypal"
        *   `state`: "test"
        *   `paypal_email_account`: Placeholder
        *   `paypal_seller_account`: Placeholder
        *   `cf_webhook_secret`: Placeholder (if PayPal uses webhook secrets in a similar way)
        *   Other fields for PayPal configuration.

##### 3.2.5.2 `data/subscription_product_data.xml`
*   **Purpose:** Define CreativeFlow subscription plans as Odoo products.
*   **Key Records:**
    *   `product.template` records for each tier (Free, Pro, Team, Enterprise):
        *   `name`: e.g., "CreativeFlow - Pro Tier"
        *   `detailed_type`: "service"
        *   `list_price`: e.g., 19.00 for Pro (monthly)
        *   `subscription_template_id`: Link to an `sale.subscription.template` defining recurrence (e.g., monthly).
        *   `cf_platform_plan_id` (custom field): e.g., "PRO_MONTHLY_V1"
        *   `cf_credit_allotment_per_cycle` (custom field): e.g., 1000.0 for a plan that includes credits.
    *   `sale.subscription.template` records:
        *   Define recurrence (e.g., "Monthly", "Annually").

#### 3.2.6 Views (`subscription_views.xml`)
*   **Purpose:** Admin UI for managing subscriptions and billing.
*   **Key Views:**
    *   Extend `res.partner` form view:
        *   Add page/group for "CreativeFlow Billing".
        *   Display `cf_credit_balance`.
        *   Display list of `cf_subscription_ids`.
        *   Display list of `cf_credit_log_ids`.
        *   Button to "Add Credits" (calls a wizard or action).
    *   Extend `sale.subscription` form and tree views:
        *   Display `cf_platform_plan_id`.
        *   Display `cf_credit_allotment_per_cycle`.
        *   Display `cf_last_sync_status_to_platform`.
        *   Button `action_sync_status_to_platform`.
    *   Views for `creativeflow.credit.log` (tree, form).
    *   Menu items for accessing credit logs and subscription management.

#### 3.2.7 Security (`ir.model.access.csv`)
*   **Purpose:** Define access rights for billing-related models and fields.
*   **Key Access Rights:**
    *   `res.partner`: Permissions for `cf_credit_balance` (e.g., Billing Manager group can read/write, Sales can read).
    *   `sale.subscription`: Permissions for `cf_platform_plan_id`, `cf_credit_allotment_per_cycle`.
    *   `creativeflow.credit.log`: Read access for billing managers/admins. No direct write/create/delete for typical users.
    *   `payment.acquirer`: Permissions for `cf_custom_config`, `cf_webhook_secret` (admin only).

#### 3.2.8 Manifest (`__manifest__.py`)
*   **`name`**: "CreativeFlow Subscription & Billing"
*   **`version`**: "1.0.0"
*   **`summary`**: "Manages subscriptions, billing, credits, and payment integration for CreativeFlow."
*   **`category`**: "CreativeFlow/Billing"
*   **`depends`**: `['sale_subscription', 'account', 'payment', 'creativeflow_core']`
*   **`data`**: List all XML view files, data files, and security CSV.
*   **`installable`**: `True`
*   **`application`**: `True` (as it forms a core part of the business application)

### 3.3 `creativeflow_helpdesk` Module
This module customizes Odoo's helpdesk functionality for CreativeFlow.

#### 3.3.1 Purpose
To leverage and extend Odoo's `helpdesk` and `knowledge` modules to provide customer support and self-service capabilities, fulfilling `Section 3.7 (Support and Help System via Odoo modules)`.

#### 3.3.2 Models

##### 3.3.2.1 `helpdesk_ticket_extension.py` (`helpdesk.ticket`)
*   **Inheritance:** `_inherit = 'helpdesk.ticket'`
*   **Fields:**
    | Name                                        | Odoo Type           | Attributes/Description                                                                                                | Requirement IDs                           |
    | :------------------------------------------ | :------------------ | :-------------------------------------------------------------------------------------------------------------------- | :---------------------------------------- |
    | `cf_related_feature_area`                   | `fields.Selection`  | `selection=[('general', 'General Inquiry'), ('ai_generation', 'AI Generation'), ('billing', 'Billing & Subscription'), ('account', 'Account Management'), ('mobile_app', 'Mobile App'), ('api', 'API Usage'), ('bug_report', 'Bug Report'), ('feature_request', 'Feature Request')]`, `string="CF Feature Area"` | `comp.backend.odoo.helpdeskModule`      |
    | `cf_user_subscription_tier_at_creation`     | `fields.Char`       | `string="User Subscription Tier (at ticket creation)"`, `compute='_compute_cf_user_subscription_tier'`, `store=True`, `readonly=True` | `comp.backend.odoo.helpdeskModule`      |
    | `partner_id` (standard Odoo field)          | `fields.Many2one`   | Ensure this is used and linked to `res.partner`.                                                                      |                                           |
*   **Methods:**
    *   `_compute_cf_user_subscription_tier(self)`:
        *   **Logic:** For each ticket, if `partner_id` is set, try to fetch `partner_id.cf_synced_subscription_tier` (from `creativeflow_core`) and set it. This helps support agents understand user context. Should be triggered `onchange` of `partner_id` or on create.

#### 3.3.3 Data Files

##### 3.3.3.1 `data/helpdesk_team_data.xml`
*   **Purpose:** Configure default helpdesk teams and stages.
*   **Key Records:**
    *   `helpdesk.team` record:
        *   `name`: "CreativeFlow Customer Support"
        *   `use_sla`: True
        *   `use_website_helpdesk_form`: True (if portal submission is used)
        *   Other settings: assignment method, visibility, etc.
    *   `helpdesk.stage` records:
        *   e.g., "New", "In Progress", "Pending Customer", "Resolved", "Cancelled". Sequence these appropriately for the "CreativeFlow Customer Support" team.
    *   (Optional) `helpdesk.ticket.type` records if specific ticket types are needed.

#### 3.3.4 Views (`helpdesk_views_extension.xml`)
*   **Purpose:** Customize helpdesk ticket views.
*   **Key Views:**
    *   Extend `helpdesk.ticket` form view:
        *   Add `cf_related_feature_area` field.
        *   Display `cf_user_subscription_tier_at_creation` (readonly).
        *   Potentially link to Knowledge Base articles related to `cf_related_feature_area`.
    *   Extend `helpdesk.ticket` tree and search views:
        *   Add `cf_related_feature_area` for filtering and grouping.

#### 3.3.5 Security (`ir.model.access.csv`)
*   **Purpose:** Define access rights for helpdesk.
*   **Key Access Rights:**
    *   Ensure support groups (`helpdesk.group_helpdesk_user`, `helpdesk.group_helpdesk_manager`) have appropriate access to standard and extended `helpdesk.ticket` fields.

#### 3.3.6 Manifest (`__manifest__.py`)
*   **`name`**: "CreativeFlow Helpdesk"
*   **`version`**: "1.0.0"
*   **`summary`**: "Customizes Odoo Helpdesk for CreativeFlow customer support."
*   **`category`**: "CreativeFlow/Support"
*   **`depends`**: `['helpdesk', 'website_helpdesk', 'knowledge', 'creativeflow_core']` (Note: `website_knowledge` might be needed if KB is on website portal)
*   **`data`**: `['security/ir.model.access.csv', 'views/helpdesk_views_extension.xml', 'data/helpdesk_team_data.xml']`
*   **`installable`**: `True`
*   **`application`**: `True`

### 3.4 `creativeflow_template_catalog` Module
This module manages the creative template catalog within Odoo, if templates are centrally managed here.

#### 3.4.1 Purpose
To provide an administrative interface within Odoo for managing the library of creative templates offered on the CreativeFlow platform, as per `comp.backend.odoo.contentMgmtModule`.

#### 3.4.2 Models

##### 3.4.2.1 `creative_template.py` (`creativeflow.template`)
*   **Model:** `_name = 'creativeflow.template'`
*   **Description:** `_description = 'CreativeFlow AI Template'`
*   **Fields:**
    | Name                   | Odoo Type         | Attributes/Description                                                                                 |
    | :--------------------- | :---------------- | :----------------------------------------------------------------------------------------------------- |
    | `name`                 | `fields.Char`     | `string="Template Name"`, `required=True`, `translate=True`                                            |
    | `description`          | `fields.Text`     | `string="Description"`, `translate=True`                                                               |
    | `category_id`          | `fields.Many2one` | `comodel_name='creativeflow.template.category'`, `string="Category"`, `required=True`, `ondelete='restrict'` |
    | `tags_ids`             | `fields.Many2many`| `comodel_name='creativeflow.template.tag'`, `string="Tags"`                                              |
    | `preview_image_url`    | `fields.Char`     | `string="Preview Image URL"`, `help="URL to the preview image, likely in MinIO."`                        |
    | `template_json_data`   | `fields.Text`     | `string="Template JSON Data"`, `help="JSON structure defining the template elements and layout for the frontend editor."`, `required=True` |
    | `is_active`            | `fields.Boolean`  | `string="Active"`, `default=True`, `help="Whether this template is available to users."`               |
    | `platform_suitability` | `fields.Char`     | `string="Platform Suitability"`, `help="e.g., Instagram Post, Facebook Ad, comma-separated"`          |
    | `usage_count`          | `fields.Integer`  | `string="Usage Count"`, `default=0`, `readonly=True`                                                   |
    | `is_pro_template`      | `fields.Boolean`  | `string="Pro Template"`, `default=False`, `help="Is this template restricted to Pro+ users?"`          |
*   **Methods:**
    *   `action_view_on_platform(self)`: (Optional) If there's a way to preview/link to how this template looks on the main platform.

##### 3.4.2.2 `template_category.py` (`creativeflow.template.category`)
*   **Model:** `_name = 'creativeflow.template.category'`
*   **Description:** `_description = 'CreativeFlow Template Category'`
*   **Fields:**
    | Name        | Odoo Type         | Attributes/Description                                                              |
    | :---------- | :---------------- | :---------------------------------------------------------------------------------- |
    | `name`      | `fields.Char`     | `string="Category Name"`, `required=True`, `translate=True`                           |
    | `parent_id` | `fields.Many2one` | `comodel_name='creativeflow.template.category'`, `string="Parent Category"`, `ondelete='cascade'` |
    | `sequence`  | `fields.Integer`  | `string="Sequence"`                                                                 |

##### 3.4.2.3 `template_tag.py` (`creativeflow.template.tag`) - New Model
*   **Model:** `_name = 'creativeflow.template.tag'`
*   **Description:** `_description = 'CreativeFlow Template Tag'`
*   **Fields:**
    | Name   | Odoo Type     | Attributes/Description                              |
    | :----- | :------------ | :-------------------------------------------------- |
    | `name` | `fields.Char` | `string="Tag Name"`, `required=True`, `translate=True` |

#### 3.4.3 Data Files

##### 3.4.3.1 `data/template_category_data.xml`
*   **Purpose:** Initialize default template categories.
*   **Key Records:**
    *   `creativeflow.template.category` records:
        *   e.g., "Social Media", "Marketing", "Events", "Industry > Real Estate", "Industry > Fashion".

#### 3.4.4 Views (`template_views.xml`)
*   **Purpose:** Admin UI for managing templates, categories, and tags.
*   **Key Views:**
    *   Form, tree, search views for `creativeflow.template`.
    *   Form, tree, search views for `creativeflow.template.category`.
    *   Form, tree, search views for `creativeflow.template.tag`.
    *   Menu items for Template Catalog management.

#### 3.4.5 Security (`ir.model.access.csv`)
*   **Purpose:** Define access rights for template catalog models.
*   **Key Access Rights:**
    *   Permissions for `creativeflow.template`, `creativeflow.template.category`, `creativeflow.template.tag` for groups like "Content Manager" (CRUD) and potentially "Sales" (Read).

#### 3.4.6 Manifest (`__manifest__.py`)
*   **`name`**: "CreativeFlow Template Catalog"
*   **`version`**: "1.0.0"
*   **`summary`**: "Manages the creative template catalog for CreativeFlow AI."
*   **`category`**: "CreativeFlow/Content Management"
*   **`depends`**: `['base', 'creativeflow_core']`
*   **`data`**: `['security/ir.model.access.csv', 'views/template_category_views.xml', 'views/template_tag_views.xml', 'views/template_views.xml', 'data/template_category_data.xml']`
*   **`installable`**: `True`
*   **`application`**: `True`

## 4. Interfaces

### 4.1 External Interfaces (Consumed by CreativeFlow Platform)
Odoo provides standard XML-RPC and JSON-RPC interfaces. The CreativeFlow platform (specifically adapter services) will interact with these for:
*   **User Data Sync:** If Odoo stores authoritative copies or needs updates for `res.partner` fields (e.g., `cf_synced_credit_balance`, `cf_synced_subscription_tier`). This would typically be a custom XML-RPC endpoint exposed by `creativeflow_core` or a dedicated sync module.
    *   Example Endpoint: `execute_kw(db, uid, password, 'res.partner', 'update_cf_synced_data', [[partner_ids], {'credits': X, 'tier': 'Y'}])`
*   **Subscription Management:** Adapter services may call Odoo to create/update subscriptions, manage payments (if not directly handled by Stripe/PayPal adapters first), or query subscription status.
    *   Example: `execute_kw(db, uid, password, 'sale.subscription', 'write', [[sub_id], {'stage_id': new_stage_id}])`
*   **Credit Management:** Adapters may call Odoo to add/deduct Odoo-managed credits.
    *   Example: `execute_kw(db, uid, password, 'res.partner', 'add_credits', [[partner_id], credit_amount, description])`
*   **Template Catalog Fetching:** If templates are managed in Odoo, an endpoint (likely custom) to fetch template metadata for the main platform.
    *   Example: `execute_kw(db, uid, password, 'creativeflow.template', 'search_read_cf_platform', [domain, fields])` - custom method for optimized fetching.

### 4.2 Internal Interfaces (Webhook Callbacks)
*   **Stripe Webhook Endpoint:** `POST /payment/stripe/webhook` (defined in `payment_webhook_controller.py`)
*   **PayPal Webhook Endpoint:** `POST /payment/paypal/webhook` (defined in `payment_webhook_controller.py`)

These endpoints are public but secured by signature verification.

## 5. Data Management
*   **Database:** PostgreSQL 16.3 (or latest stable), managed by Odoo's ORM.
*   **Schemas:** Defined by Odoo standard modules and extended/created by the custom `creativeflow_*` modules as detailed in Section 3.
*   **Data Integrity:** Enforced by Odoo ORM constraints (`required=True`, `ondelete` rules), SQL constraints where necessary, and Python model validation.
*   **Data Archival/Retention:** Odoo itself does not typically hard-delete records; it often archives them (`active=False`). Specific retention policies for business data (invoices, subscriptions) are usually governed by legal and accounting requirements, configurable within Odoo or handled by standard archival processes. User-initiated data deletion requests (GDPR) would need custom handling to ensure data is properly anonymized or removed from Odoo as well, respecting linked records constraints.

## 6. Configuration
*   **`odoo.conf`:** Standard Odoo configuration file for database connection, addons path, server settings.
*   **Odoo UI (System Parameters / Technical Settings):**
    *   Payment Acquirer API keys (Stripe, PayPal).
    *   Webhook secrets for payment acquirers.
    *   Tax configurations.
*   **Feature Toggles (via `ir.config_parameter` or custom model):**
    *   `creativeflow.enable_custom_credit_logic_in_odoo`: Boolean, to enable/disable custom credit logic if an alternative master system is used.
    *   `creativeflow.enable_extended_helpdesk_fields`: Boolean, to enable additional fields on helpdesk tickets.
    *   `creativeflow.manage_templates_in_odoo`: Boolean, to determine if Odoo is the master for template catalog.
*   **Data Files (`.xml`):** Initial setup for payment acquirers, subscription products, helpdesk teams, template categories (as detailed in Section 3).

## 7. Error Handling & Logging
*   **Error Handling:**
    *   Standard Odoo exceptions (`odoo.exceptions.UserError`, `odoo.exceptions.ValidationError`, `odoo.exceptions.AccessError`) will be used to provide user-friendly feedback for operational errors.
    *   Python `try-except` blocks for handling potential errors in custom logic, especially in service methods and webhook controllers.
    *   Webhook controllers must return appropriate HTTP status codes (200 for success, 4xx for client errors like invalid signature, 5xx for server errors). Webhook processing should be idempotent.
*   **Logging:**
    *   Utilize Odoo's standard logging mechanism (`_logger = logging.getLogger(__name__)`).
    *   Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) should be used appropriately.
    *   Log key events:
        *   Webhook reception and processing status (success/failure, event type).
        *   Credit additions/deductions.
        *   Subscription status changes.
        *   Errors encountered in custom services or model methods.
        *   Sync actions with the main platform.
    *   Log messages should be informative and include relevant context (e.g., record IDs, event IDs).

## 8. Deployment Considerations
*   **Module Installation:** Standard Odoo module installation process. Dependencies listed in `__manifest__.py` files must be satisfied.
*   **Configuration:** After installation, API keys for payment acquirers and webhook secrets must be securely configured via the Odoo UI or environment variables mapped to Odoo settings.
*   **Initial Data:** Data files (`.xml`) will seed initial configurations.
*   **Permissions:** Ensure `ir.model.access.csv` files correctly set up permissions for new models and fields.
*   **Testing:** Thorough testing of all custom functionalities and integrations post-deployment is crucial.

## 9. Future Considerations
*   **Deeper User Synchronization:** If more user profile data from the main platform needs to be visible or editable within Odoo for specific administrative workflows, `creativeflow_core` could be expanded.
*   **Advanced Reporting:** Custom Odoo reports for CreativeFlow specific KPIs (e.g., credit consumption trends, subscription churn analysis within Odoo context).
*   **Direct API for Adapters:** While XML-RPC/JSON-RPC is standard, dedicated RESTful endpoints could be built within Odoo (using Odoo's HTTP controllers) if more complex or higher-performance integrations are needed by adapter microservices, though this is generally discouraged in favor of keeping Odoo as a pure backend.
*   **Odoo Enterprise Features:** If Odoo Enterprise is used, leverage its advanced features for accounting, marketing automation, etc., that might benefit CreativeFlow.