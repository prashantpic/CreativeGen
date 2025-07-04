# Software Design Specification (SDS) for CreativeFlow.Service.CoreBusiness.Odoo

## 1. Introduction

This document provides the detailed software design specification for the `CreativeFlow.Service.CoreBusiness.Odoo` repository. This repository forms the central nervous system of the CreativeFlow AI platform, implementing the core business logic, data models, and operational workflows using the Odoo 18+ framework.

### 1.1. Purpose

The purpose of this Odoo application is to manage all core business entities and processes, including:
-   **User & Account Management:** Extending Odoo's user model to fit platform needs.
-   **Content Management:** Storing metadata for Workbenches, Projects, and Brand Kits.
-   **Subscription & Billing:** Leveraging Odoo's powerful Sales and Accounting apps to manage subscription plans, payments, and a custom credit system.
-   **Customer Support:** Utilizing Odoo's Helpdesk and Knowledge modules for integrated user support.
-   **API & Integration Hub:** Acting as the primary backend that exposes business logic via REST APIs and orchestrates asynchronous tasks via a message broker.

### 1.2. Scope

This SDS covers the design and implementation of all custom Odoo modules required for the CreativeFlow AI platform. This includes data models, business logic (methods), controllers (API endpoints), views (for backend administration), and integration services (RabbitMQ, Payment Gateways).

---

## 2. System Architecture & Design

### 2.1. Architectural Style

The Odoo application is a monolithic service but acts as a core component within a broader **Microservices Architecture**. It adheres to a standard **Layered Architecture** internally, separating models (data), views (presentation for admin), and controllers (business logic/API).

### 2.2. Key Interaction Patterns

1.  **Synchronous API Communication:** Odoo exposes a set of RESTful APIs (via custom controllers) that are consumed by the API Gateway. This is used for operations requiring an immediate response, such as fetching user profile data or project details.
2.  **Asynchronous Event Publishing:** For long-running, resource-intensive tasks like AI creative generation, Odoo acts as an **Event Publisher**. It validates a request, performs initial business logic (e.g., credit deduction), and then publishes a job message to a **RabbitMQ** message broker. This decouples the core application from the AI processing workload, ensuring responsiveness.
3.  **Webhook Consumption:** Odoo acts as a consumer for webhooks from external services, primarily payment gateways like **Stripe** and **PayPal**. Specific controllers listen for events (e.g., successful payment) to trigger internal workflows like activating subscriptions or adding credits.

---

## 3. Module Design & Implementation Details

This section details the implementation for each Odoo module and its constituent files as defined in the repository structure.

### 3.1. `creativeflow_base` Module

This is the foundational module. All other `creativeflow_*` modules will depend on it.

#### 3.1.1. `__manifest__.py`
-   **Purpose:** Declares the base module, its metadata, and dependencies.
-   **Implementation:**
    -   `name`: "CreativeFlow AI - Base Module"
    -   `summary`: "Core models and base functionality for the CreativeFlow AI platform."
    -   `depends`: `['base', 'web', 'auth_signup', 'mail']`
    -   `data`: `['security/ir.model.access.csv', 'views/creativeflow_menus.xml']`
    -   `application`: `True`
    -   `installable`: `True`

#### 3.1.2. `models/res_users.py`
-   **Purpose:** Extends the built-in `res.users` model with platform-specific fields and logic.
-   **Implementation:**
    -   **Class:** `CreativeFlowUser`
    -   **Inheritance:** `_inherit = 'res.users'`
    -   **Fields:**
        -   `subscription_tier`: `fields.Selection`, selection=`[('Free', 'Free'), ('Pro', 'Pro'), ('Team', 'Team'), ('Enterprise', 'Enterprise')]`, default='Free', required=True, string="Subscription Tier".
        -   `credit_balance`: `fields.Float`, string="Credit Balance", default=0.0, digits=(10, 2), readonly=True, help="Cached credit balance. Source of truth is credit transactions."
        -   `x_studio_brand_kit_ids`: `fields.One2many`, comodel_name='creativeflow.brand_kit', inverse_name='user_id', string="Brand Kits".
        -   `x_studio_workbench_ids`: `fields.One2many`, comodel_name='creativeflow.workbench', inverse_name='user_id', string="Workbenches".
    -   **Methods:**
        -   `deduct_credits(self, amount: float, description: str, generation_request_id: int = None) -> bool`:
            -   **Logic:**
                1.  Iterate through `self` (user records).
                2.  Raise `odoo.exceptions.UserError` if `user.credit_balance < amount`.
                3.  Update the user's balance: `user.credit_balance -= amount`.
                4.  Create a `creativeflow.credit_transaction` record with the user_id, a negative amount, description, and optional `generation_request_id`.
                5.  Return `True` on success. The operation must be atomic per user.
        -   `add_credits(self, amount: float, description: str, related_invoice_id: int = None) -> bool`:
            -   **Logic:**
                1.  Iterate through `self` (user records).
                2.  Update the user's balance: `user.credit_balance += amount`.
                3.  Create a `creativeflow.credit_transaction` record with the user_id, a positive amount, description, and optional `related_invoice_id`.
                4.  Return `True`.

#### 3.1.3. `views/creativeflow_menus.xml`
-   **Purpose:** Creates the main application menu in the Odoo UI.
-   **Implementation:**
    -   Define a top-level `ir.ui.menu` record with `id="menu_root"` and `name="CreativeFlow AI"`.
    -   Define child menus under `menu_root` for "Dashboard", "Workbenches", "Brand Kits", "Helpdesk", "Subscriptions", and "Settings". These will have placeholders for `action` attributes, which will be filled in by their respective modules.

#### 3.1.4. `security/ir.model.access.csv`
-   **Purpose:** Provide default access for models in this module.
-   **Implementation:** This file will be expanded upon by other modules. Initially, it might be empty or grant base users access to see their own modified user record fields.

### 3.2. `creativeflow_content_management` Module

#### 3.2.1. `__manifest__.py`
-   `name`: "CreativeFlow AI - Content Management"
-   `depends`: `['creativeflow_base']`
-   `data`: `['security/ir.model.access.csv', 'views/brand_kit_views.xml', 'views/workbench_views.xml', 'views/project_views.xml']`

#### 3.2.2. Models (`models/`)
-   `creativeflow_brand_kit.py`:
    -   **Model:** `creativeflow.brand_kit`
    -   **Fields:**
        -   `name`: `fields.Char`, required=True
        -   `user_id`: `fields.Many2one`, comodel_name='res.users', required=True, ondelete='cascade'
        -   `colors`: `fields.Text`, help="JSON string for color palette, e.g., '[{\"name\": \"Primary\", \"hex\": \"#FF0000\"}]'"
        -   `fonts`: `fields.Text`, help="JSON string for font definitions."
        -   `logos`: `fields.Text`, help="JSON string of logo asset MinIO paths."
        -   `is_default`: `fields.Boolean`, default=False, copy=False
    -   **Constraints:**
        -   `@api.constrains('is_default', 'user_id')`: A SQL constraint to ensure only one `is_default=True` record exists per `user_id`.
-   `creativeflow_workbench.py`:
    -   **Model:** `creativeflow.workbench`
    -   **Fields:**
        -   `name`: `fields.Char`, required=True
        -   `user_id`: `fields.Many2one`, comodel_name='res.users', required=True, ondelete='cascade'
        -   `project_ids`: `fields.One2many`, comodel_name='creativeflow.project', inverse_name='workbench_id'
        -   `default_brand_kit_id`: `fields.Many2one`, comodel_name='creativeflow.brand_kit'
-   `creativeflow_project.py`:
    -   **Model:** `creativeflow.project`
    -   **Fields:**
        -   `name`: `fields.Char`, required=True
        -   `workbench_id`: `fields.Many2one`, comodel_name='creativeflow.workbench', required=True, ondelete='cascade'
        -   `user_id`: `fields.Many2one`, comodel_name='res.users', related='workbench_id.user_id', store=True, readonly=True
        -   `brand_kit_id`: `fields.Many2one`, comodel_name='creativeflow.brand_kit', help="Override the workbench's default brand kit."
        -   `asset_ids`: `fields.One2many`, comodel_name='creativeflow.asset', inverse_name='project_id' (This model will likely live in another module, but the relation is defined here).

#### 3.2.3. Views (`views/`)
-   Each model (`brand_kit`, `workbench`, `project`) will have a corresponding `_views.xml` file.
-   Each view file will define an `ir.actions.act_window` and `form`, `tree`, and `kanban` views for the respective model, linked to the menus created in `creativeflow_base`.

### 3.3. `creativeflow_billing_subscription` Module

#### 3.3.1. `__manifest__.py`
-   `name`: "CreativeFlow AI - Billing & Subscriptions"
-   `depends`: `['creativeflow_base', 'sale_subscription', 'account', 'payment']`
-   `data`: `['security/ir.model.access.csv', 'data/product_data.xml', 'views/subscription_views.xml']`

#### 3.3.2. Data (`data/`)
-   `product_data.xml`:
    -   **Purpose:** Define the subscription plans as Odoo `product.template` records.
    -   **Implementation:** Create `product.template` records for "Pro Plan", "Team Plan", and "Enterprise Plan". Set `is_subscription = True`. Define `subscription_template_id` to link to a `sale.subscription.template` which defines the recurrence (e.g., monthly). Set the `list_price`.

#### 3.3.3. Models (`models/`)
-   `creativeflow_credit_transaction.py`:
    -   **Model:** `creativeflow.credit_transaction`
    -   **Fields:**
        -   `user_id`: `fields.Many2one`, comodel_name='res.users', required=True
        -   `amount`: `fields.Float`, required=True, digits=(10, 2)
        -   `description`: `fields.Char`, required=True
        -   `generation_request_id`: `fields.Many2one`, comodel_name='creativeflow.generation_request' (Model to be defined in AI module)
        -   `related_invoice_id`: `fields.Many2one`, comodel_name='account.move'
-   `sale_subscription.py` (Model Extension):
    -   **Inheritance:** `_inherit = 'sale.subscription'`
    -   **Logic:** Override `_recurring_create_invoice` and `_reconcile_and_send_invoices` to add custom logic. After a subscription invoice is successfully paid, find the related `res.users` record and call the `add_credits` method if the plan includes credit packs.

#### 3.3.4. Controllers (`controllers/`)
-   `payment_controllers.py`:
    -   **Inheritance:** `_inherit = 'payment.portal'` (or a new controller)
    -   **Methods:**
        -   `stripe_webhook(self, **post)`:
            -   **Route:** `'/payment/stripe/webhook'`, `type='json'`, `auth='public'`.
            -   **Logic:**
                1.  Retrieve Stripe webhook secret from `ir.config_parameter`.
                2.  Get the `Stripe-Signature` header and the request payload.
                3.  Use the `stripe` library to construct the event, which verifies the signature. Raise an exception if verification fails.
                4.  Handle `checkout.session.completed` and `invoice.paid` events.
                5.  From the event data, find the corresponding Odoo `sale.order` or `sale.subscription`.
                6.  Confirm the sale order/subscription. If it involves credit packs, call `user.add_credits()`.
                7.  Return a 200 OK response.
        -   `paypal_webhook(self, **post)`: Similar logic for PayPal's IPN or webhook system.

### 3.4. `creativeflow_api` Module

This module provides the primary interface for the web frontend.

#### 3.4.1. `__manifest__.py`
-   `name`: "CreativeFlow AI - REST API"
-   `depends`: `['creativeflow_base', 'creativeflow_content_management', 'creativeflow_billing_subscription', 'creativeflow_integration_rabbitmq']`

#### 3.4.2. Controllers (`controllers/`)
-   `generation_controller.py`:
    -   **Class:** `GenerationController`, inherits `http.Controller`
    -   **Methods:**
        -   `initiate_generation(self, **kwargs)`:
            -   **Route:** `'/api/v1/generation/create'`, `type='json'`, `auth='user'`, `methods=['POST']`, `csrf=False`.
            -   **Logic:**
                1.  Get the current user: `user = request.env.user`.
                2.  Extract `prompt`, `project_id`, `format`, etc., from `kwargs`. Validate inputs.
                3.  Calculate credit cost based on the request type (e.g., sample vs. final).
                4.  **Critical Section:** Call `user.deduct_credits(cost, 'AI Generation Request')`. This should be transactional. If it fails, an exception is raised and the process stops.
                5.  Create a `creativeflow.generation_request` record in the database with status 'Pending'.
                6.  Get the RabbitMQ publisher service: `publisher = request.env['rabbitmq.publisher']`.
                7.  Construct the JSON `job_payload` including `generation_request_id`, `user_id`, `prompt`, etc.
                8.  Call `publisher.publish_generation_job(job_payload)`.
                9.  Return a JSON response: `{'status': 'success', 'generation_id': new_request.id}`.
        -   `get_generation_status(self, generation_id)`:
            -   **Route:** `'/api/v1/generation/<uuid:generation_id>/status'`, `type='http'`, `auth='user'`, `methods=['GET']`.
            -   **Logic:**
                1.  Find the `creativeflow.generation_request` record. Ensure the current user has access rights.
                2.  Return JSON with the status and any relevant data (e.g., sample URLs if ready).

### 3.5. `creativeflow_integration_rabbitmq` Module

#### 3.5.1. `__manifest__.py`
-   `name`: "CreativeFlow AI - RabbitMQ Integration"
-   `depends`: `['creativeflow_base']`

#### 3.5.2. Services (`services/`)
-   `rabbitmq_publisher.py`:
    -   **Class:** `RabbitMQPublisher`, inherits `models.AbstractModel`.
    -   **Model Name:** `_name = 'rabbitmq.publisher'`.
    -   **Methods:**
        -   `_get_connection_params()`: Reads `RABBITMQ_HOST`, `RABBITMQ_USER`, etc., from `request.env['ir.config_parameter'].sudo().get_param(...)`.
        -   `_connect()`: Establishes a connection to RabbitMQ using `pika.BlockingConnection` and creates a channel.
        -   `publish_generation_job(self, job_payload: dict)`:
            -   **Logic:**
                1.  Ensure connection is active, or call `_connect()`.
                2.  Declare a durable exchange, e.g., `exchange='ai_exchange'`, `exchange_type='topic'`.
                3.  Publish the message: `channel.basic_publish(...)` with `routing_key='generation.create'`, `body=json.dumps(job_payload)`, and `properties=pika.BasicProperties(delivery_mode=2)` for message persistence.
                4.  Include error handling for connection failures.

### 3.6. `creativeflow_helpdesk` Module

#### 3.6.1. `__manifest__.py`
-   `name`: "CreativeFlow AI - Helpdesk Customizations"
-   `depends`: `['creativeflow_base', 'helpdesk', 'website_helpdesk_form']`

#### 3.6.2. Models (`models/`)
-   `helpdesk_ticket.py`:
    -   **Inheritance:** `_inherit = 'helpdesk.ticket'`
    -   **Fields:**
        -   `project_id`: `fields.Many2one`, comodel_name='creativeflow.project', string="Related Project".
        -   `generation_request_id`: `fields.Many2one`, comodel_name='creativeflow.generation_request', string="Related Generation Request".

---

## 4. Error Handling and Logging

-   **User Errors:** All business logic validation (e.g., insufficient credits, invalid input) will raise `odoo.exceptions.UserError` or `ValidationError`. API controllers will catch these and return a structured JSON error with HTTP status 400 or 422.
-   **System Errors:** Unexpected exceptions will be caught at the controller level and return a generic HTTP 500 error. All exceptions must be logged with a full traceback.
-   **Logging:** Odoo's built-in `_logger` will be used. All API requests, job publications, credit transactions, and webhook processing steps must be logged at an `INFO` level. Errors and exceptions will be logged at an `ERROR` level. Logs must be structured where possible to facilitate parsing by the central logging system.

## 5. Security

-   **Authentication:** API endpoints will use `auth='user'`, relying on Odoo's session/token validation. Public webhooks (`auth='public'`) must perform their own signature verification.
-   **Authorization:** Odoo's record rules and `ir.model.access.csv` will be the primary mechanism for authorization, ensuring users can only access their own data (projects, workbenches, etc.).
-   **Secrets Management:** All external service credentials (RabbitMQ, Stripe, PayPal) must be stored securely using Odoo's `ir.config_parameter` and should not be hardcoded. The production environment should have these parameters set with restricted access.