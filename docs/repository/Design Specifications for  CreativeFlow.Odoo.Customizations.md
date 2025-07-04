# Software Design Specification: CreativeFlow.Odoo.Customizations

## 1. Introduction

This document outlines the software design specification for the `CreativeFlow.Odoo.Customizations` repository. This repository contains custom Odoo 18+ modules developed to extend the core Odoo functionality to meet the specific business logic requirements of the CreativeFlow AI platform. These customizations span user management, credit systems, billing and subscriptions, brand/workbench management, and support interface enhancements.

**Target Odoo Version:** Odoo 18+ (or latest stable at development start)
**Primary Language:** Python 3.11+
**View/Data Language:** XML
**Frontend Extension Language:** JavaScript (ES6+)

## 2. General Design Principles

*   **Modularity**: Each distinct functional area (e.g., credits, user extensions) will be encapsulated in its own Odoo module to ensure separation of concerns and maintainability.
*   **Inheritance**: Standard Odoo models will be extended using Odoo's inheritance mechanisms (`_inherit`) to add new fields and modify behavior without altering core code directly.
*   **Security**: Access control will be managed via `ir.model.access.csv` files and group assignments, adhering to the principle of least privilege.
*   **User Experience**: Custom views will integrate seamlessly with the standard Odoo interface, providing a consistent user experience. Branding elements will be applied where necessary, especially for user-facing portal components.
*   **Data Integrity**: Relational integrity will be maintained through proper use of Odoo's ORM, foreign keys, and `ondelete` rules.
*   **Configuration**: Where applicable, system behavior (e.g., credit costs) will be configurable via Odoo backend interfaces.
*   **External System Interaction**: Interactions with the main CreativeFlow platform (e.g., syncing user IDs, credit balance updates) will primarily be through API calls or message queues managed by other services. Odoo's role is to store relevant synced data and apply business logic based on it. JSON fields are used to store structured data from external systems where direct relational mapping is not required or too complex within Odoo.

## 3. Module Specifications

This section details the design for each custom Odoo module within this repository.

### 3.1. Module: `creativeflow_user_extensions`

**Purpose**: To extend the standard Odoo `res.users` model with fields specific to the CreativeFlow platform, facilitating integration and data synchronization.

**Namespace**: `odoo.addons.creativeflow_user_extensions`

#### 3.1.1. Manifest (`__manifest__.py`)

*   **`name`**: "CreativeFlow User Extensions"
*   **`version`**: "18.0.1.0.0"
*   **`summary`**: "Extends Odoo users with CreativeFlow specific fields like credit balance and subscription tier."
*   **`category`**: "CreativeFlow/User Management"
*   **`author`**: "CreativeFlow AI Team"
*   **`website`**: "https://creativeflow.ai"
*   **`depends`**: `['base', 'mail']`
*   **`data`**:
    *   `security/ir.model.access.csv`
    *   `views/res_users_views.xml`
*   **`installable`**: `True`
*   **`application`**: `False`
*   **`auto_install`**: `False`

#### 3.1.2. Models

##### 3.1.2.1. `models/res_users.py` (Extending `res.users`)

*   **`_inherit`**: `res.users`
*   **Fields**:
    *   `credit_balance`:
        *   Type: `fields.Float`
        *   String: "Credit Balance"
        *   `digits`: `(16, 4)` (Consider precision based on credit unit, e.g., 0.25 credits)
        *   `readonly`: `True`
        *   `default`: `0.0`
        *   `tracking`: `True`
        *   `help`: "User's current credit balance, primarily managed by the CreativeFlow Credit System module but displayed here for information. This field is typically updated by automated processes or credit transactions."
    *   `cf_subscription_tier`:
        *   Type: `fields.Selection`
        *   String: "CreativeFlow Subscription Tier"
        *   `selection`: `[('free', 'Free'), ('pro', 'Pro'), ('team', 'Team'), ('enterprise', 'Enterprise')]`
        *   `default`: `'free'`
        *   `tracking`: `True`
        *   `help`: "The user's current subscription tier on the CreativeFlow platform."
    *   `cf_external_user_id`:
        *   Type: `fields.Char`
        *   String: "CreativeFlow Platform User ID"
        *   `index`: `True`
        *   `help`: "Unique User ID from the main CreativeFlow platform, used for synchronization and API calls. This helps link the Odoo user to their primary platform account if Odoo is not the master identity provider."
    *   `cf_language_preference`:
        *   Type: `fields.Char` (Consider `fields.Selection` if languages are predefined and limited)
        *   String: "CreativeFlow Language Preference"
        *   `size`: `10`
        *   `default`: `'en-US'`
        *   `help`: "User's preferred language for the CreativeFlow platform UI (e.g., 'en-US', 'es-ES')."
    *   `cf_timezone`:
        *   Type: `fields.Char` (Consider `fields.Selection` populated by `pytz.all_timezones`)
        *   String: "CreativeFlow Timezone"
        *   `size`: `50`
        *   `default`: `'UTC'`
        *   `help`: "User's preferred timezone for localized date/time display."
*   **Methods**: None specific to this direct extension, logic related to credits will be in `creativeflow_credits`.

#### 3.1.3. Views

##### 3.1.3.1. `views/res_users_views.xml`

*   Inherit `res.users` form view (`base.view_users_form`):
    *   Add a new notebook page titled "CreativeFlow Details".
    *   Inside this page, add a group with fields: `credit_balance`, `cf_subscription_tier`, `cf_external_user_id`, `cf_language_preference`, `cf_timezone`.
*   Inherit `res.users` tree view (`base.view_users_tree`):
    *   Add columns for `cf_subscription_tier` and `credit_balance` (optional, for quick admin overview).

#### 3.1.4. Security

##### 3.1.4.1. `security/ir.model.access.csv`

| id                                     | name                                  | model_id/id      | group_id/id      | perm_read | perm_write | perm_create | perm_unlink |
| :------------------------------------- | :------------------------------------ | :--------------- | :--------------- | :-------- | :--------- | :---------- | :---------- |
| access_res_users_cf_fields_user        | res.users.cf.fields.user.access       | model_res_users  | base.group_user  | 1         | 1          | 0           | 0           |
| access_res_users_cf_fields_admin       | res.users.cf.fields.admin.access      | model_res_users  | base.group_system| 1         | 1          | 0           | 0           |
| access_res_users_cf_credit_balance_ro  | res.users.cf.credit_balance.ro.access | model_res_users  | base.group_user  | 1         | 0          | 0           | 0           |
> Note: `credit_balance` is `readonly=True` in model, so `perm_write` 0 for users is consistent. Admins might need write for manual adjustments, though this should be rare and ideally through credit transactions. This CSV focuses on field-level access if record-level is already granted by base. Odoo might not support fine-grained field access directly in `ir.model.access.csv` for inherited models this way; it's usually controlled by view attributes or model field attributes (`readonly`, `groups`). The primary control here is that base Odoo user records are accessible by admins; these fields will follow suit.

### 3.2. Module: `creativeflow_credits`

**Purpose**: To implement the credit system logic, including tracking credit transactions, defining costs for platform actions, and providing methods for debiting/crediting user balances.

**Namespace**: `odoo.addons.creativeflow_credits`

#### 3.2.1. Manifest (`__manifest__.py`)

*   **`name`**: "CreativeFlow Credit System"
*   **`version`**: "18.0.1.0.0"
*   **`summary`**: "Manages user credits, action costs, and credit transactions for the CreativeFlow platform."
*   **`category`**: "CreativeFlow/Billing"
*   **`author`**: "CreativeFlow AI Team"
*   **`website`**: "https://creativeflow.ai"
*   **`depends`**: `['base', 'mail', 'creativeflow_user_extensions']`
*   **`data`**:
    *   `security/ir.model.access.csv`
    *   `views/credit_transaction_views.xml`
    *   `views/credit_action_cost_views.xml`
    *   `views/res_users_credit_views.xml` (to add credit transaction related list to user form)
    *   `views/credit_menus.xml`
    *   `data/credit_action_cost_data.xml`
*   **`installable`**: `True`
*   **`application`**: `True` (as it provides core business functionality)
*   **`auto_install`**: `False`

#### 3.2.2. Models

##### 3.2.2.1. `models/credit_transaction.py`

*   **`_name`**: `creativeflow.credit.transaction`
*   **`_description`**: "CreativeFlow Credit Transaction"
*   **`_inherit`**: `['mail.thread', 'mail.activity.mixin']` (for communication and tracking)
*   **`_order`**: `transaction_date desc, id desc`
*   **Fields**:
    *   `user_id`:
        *   Type: `fields.Many2one`
        *   `comodel_name`: `'res.users'`
        *   String: "User"
        *   `required`: `True`
        *   `ondelete`: `'cascade'`
        *   `index`: `True`
    *   `amount`:
        *   Type: `fields.Float`
        *   String: "Amount"
        *   `required`: `True`
        *   `digits`: `(16, 4)` (consistent with `credit_balance`)
        *   `help`: "Positive for credit (addition to balance), negative for debit (deduction from balance)."
    *   `balance_after_transaction`:
        *   Type: `fields.Float`
        *   String: "Balance After"
        *   `digits`: `(16, 4)`
        *   `readonly`: `True`
        *   `help`: "User's credit balance after this transaction was applied."
    *   `type`:
        *   Type: `fields.Selection`
        *   String: "Type"
        *   `selection`: `[('purchase', 'Purchase'), ('refund', 'Refund'), ('adjustment_add', 'Adjustment (Add)'), ('adjustment_deduct', 'Adjustment (Deduct)'), ('sample_generation', 'Sample Generation'), ('final_generation', 'Final Generation'), ('export_hd', 'HD Export'), ('api_usage', 'API Usage'), ('other_debit', 'Other Debit'), ('other_credit', 'Other Credit')]`
        *   `required`: `True`
        *   `help`: "Categorizes the credit transaction."
    *   `description`:
        *   Type: `fields.Text`
        *   String: "Description"
        *   `help`: "Details about the transaction, e.g., 'Purchase of 100 credits', 'Cost for generating image X'."
    *   `reference_document`:
        *   Type: `fields.Reference`
        *   `selection`: `[('creativeflow.generation.request.external', 'Generation Request (External)'), ('creativeflow.api.call.external', 'API Call (External)'), ('sale.order', 'Sale Order/Invoice')]`
        *   String: "Reference Document"
        *   `help`: "Link to the originating document if applicable (e.g., an Odoo Sale Order for credit purchase, or an external generation request ID)."
            > Note: `creativeflow.generation.request.external` and `creativeflow.api.call.external` are placeholder model names for external references. These won't be actual Odoo models but serve as a string key for the reference. The actual ID will be stored in a separate Char field.
    *   `external_reference_id`:
        *   Type: `fields.Char`
        *   String: "External Reference ID"
        *   `help`: "Stores the ID of the external document (e.g., Generation Request ID, API Call ID)."
    *   `transaction_date`:
        *   Type: `fields.Datetime`
        *   String: "Date"
        *   `default`: `fields.Datetime.now`
        *   `required`: `True`
        *   `readonly`: `True`

##### 3.2.2.2. `models/credit_action_cost.py`

*   **`_name`**: `creativeflow.credit.action.cost`
*   **`_description`**: "CreativeFlow Credit Action Cost"
*   **Fields**:
    *   `name`:
        *   Type: `fields.Char`
        *   String: "Action Name / Identifier"
        *   `required`: `True`
        *   `index`: `True`
        *   `help`: "Unique identifier for the billable action, e.g., 'sample_generation', 'final_generation_standard_res', 'export_hd', 'api_call_model_x'."
    *   `cost`:
        *   Type: `fields.Float`
        *   String: "Credit Cost"
        *   `required`: `True`
        *   `digits`: `(16, 4)`
        *   `help`: "Number of credits this action costs. Can be 0 for free actions under certain plans."
    *   `description`:
        *   Type: `fields.Text`
        *   String: "Description"
    *   `is_active`:
        *   Type: `fields.Boolean`
        *   String: "Active"
        *   `default`: `True`
        *   `help`: "Only active costs are considered for billing."
*   **SQL Constraints**:
    *   `unique_action_name`: `UNIQUE(name)`, "An action with this identifier already exists!"

##### 3.2.2.3. `models/res_users_credit_mixin.py` (Extending `res.users`)

*   **`_inherit`**: `res.users`
*   **Methods**:
    *   `_get_action_cost(self, action_identifier)`:
        *   **Parameters**: `action_identifier` (str)
        *   **Returns**: `float` (cost) or raises `UserError` if action not found or inactive.
        *   **Logic**:
            1.  Search `creativeflow.credit.action.cost` for an active record where `name == action_identifier`.
            2.  If not found or not active, raise `UserError("Action cost not defined or inactive for: %s" % action_identifier)`.
            3.  Return the `cost`.
    *   `action_debit_credits(self, amount_to_debit, action_type, description, external_reference_model=None, external_reference_id=None, force_debit=False)`:
        *   **Parameters**:
            *   `amount_to_debit` (float): The specific amount of credits to debit.
            *   `action_type` (str): The type of action from `credit.transaction` selection.
            *   `description` (str): Description for the transaction.
            *   `external_reference_model` (str, optional): Model name for `reference_document`.
            *   `external_reference_id` (str/int, optional): ID for `external_reference_id`.
            *   `force_debit` (bool, optional, default=False): If True, allows debiting even if balance goes negative (e.g., for system corrections by admin).
        *   **Returns**: `creativeflow.credit.transaction` record.
        *   **Logic**:
            1.  Iterate through `self` (users). For each user:
            2.  Check `user.credit_balance >= amount_to_debit` if `not force_debit`. If insufficient, raise `UserError("Insufficient credits for %s. Required: %.2f, Available: %.2f" % (user.name, amount_to_debit, user.credit_balance))`.
            3.  Update `user.credit_balance -= amount_to_debit`.
            4.  Create a `creativeflow.credit.transaction` record:
                *   `user_id`: `user.id`
                *   `amount`: `-amount_to_debit` (store as negative)
                *   `type`: `action_type`
                *   `description`: `description`
                *   `balance_after_transaction`: `user.credit_balance`
                *   `reference_document`: `"%s,%s" % (external_reference_model, external_reference_id)` if both provided.
                *   `external_reference_id`: `str(external_reference_id)` if provided.
            5.  Return the created transaction record.
            > Use `@api.multi` or loop `self` for Odoo 12+ style, ensure `self.ensure_one()` if operating on a single record context. For Odoo 13+, method operates on `self` recordset.
    *   `action_credit_credits(self, amount_to_credit, action_type, description, external_reference_model=None, external_reference_id=None)`:
        *   **Parameters**:
            *   `amount_to_credit` (float): Positive amount of credits to add.
            *   `action_type` (str): The type of action from `credit.transaction` selection.
            *   `description` (str): Description for the transaction.
            *   `external_reference_model` (str, optional): Model name for `reference_document`.
            *   `external_reference_id` (str/int, optional): ID for `external_reference_id`.
        *   **Returns**: `creativeflow.credit.transaction` record.
        *   **Logic**:
            1.  Iterate through `self` (users). For each user:
            2.  Update `user.credit_balance += amount_to_credit`.
            3.  Create a `creativeflow.credit.transaction` record:
                *   `user_id`: `user.id`
                *   `amount`: `amount_to_credit` (store as positive)
                *   `type`: `action_type`
                *   `description`: `description`
                *   `balance_after_transaction`: `user.credit_balance`
                *   `reference_document`: `"%s,%s" % (external_reference_model, external_reference_id)` if both provided.
                *   `external_reference_id`: `str(external_reference_id)` if provided.
            4.  Return the created transaction record.
    *   `api_debit_credits_by_action_identifier(self, action_identifier, description_prefix="", external_reference_model=None, external_reference_id=None, force_debit=False)`:
        *   **Parameters**:
            *   `action_identifier` (str): The unique identifier from `creativeflow.credit.action.cost`.
            *   `description_prefix` (str, optional): Prefix for the transaction description.
            *   `external_reference_model` (str, optional): Model name for `reference_document`.
            *   `external_reference_id` (str/int, optional): ID for `external_reference_id`.
            *   `force_debit` (bool, optional, default=False).
        *   **Returns**: `creativeflow.credit.transaction` record.
        *   **Logic**:
            1.  `self.ensure_one()`
            2.  `cost = self._get_action_cost(action_identifier)`
            3.  `action_config = self.env['creativeflow.credit.action.cost'].search([('name', '=', action_identifier), ('is_active', '=', True)], limit=1)`
            4.  `description = "%s%s (Cost: %.2f credits)" % (description_prefix, action_config.description or action_identifier, cost)`
            5.  Map `action_identifier` to an appropriate `action_type` for `credit.transaction` (e.g., `sample_generation` -> `'sample_generation'`). This might require a predefined mapping or deriving it from `action_identifier`.
            6.  Call `self.action_debit_credits(cost, mapped_action_type, description, external_reference_model, external_reference_id, force_debit=force_debit)`.
*   **Controller (Optional, if Odoo needs to expose credit deduction to external authenticated services)**:
    *   An Odoo controller endpoint might be needed if the main platform needs to call Odoo to debit credits. This should be secured.
    *   Example: `/creativeflow/credits/debit` (POST request)
        *   **Parameters**: `user_external_id`, `action_identifier`, `reference_details` (JSON).
        *   **Authentication**: Requires secure service-to-service authentication (e.g., API key, OAuth client credentials).
        *   **Logic**: Finds `res.users` by `cf_external_user_id`, then calls `api_debit_credits_by_action_identifier`.

#### 3.2.3. Views

##### 3.2.3.1. `views/credit_transaction_views.xml`

*   **Tree View (`creativeflow_credit_transaction_tree`)**:
    *   Fields: `transaction_date`, `user_id`, `type`, `amount`, `balance_after_transaction`, `description`, `reference_document`, `external_reference_id`.
    *   Default sort: `transaction_date desc`.
*   **Form View (`creativeflow_credit_transaction_form`)**:
    *   Fields: `user_id` (readonly if created), `amount` (readonly), `type` (readonly), `balance_after_transaction` (readonly), `description`, `reference_document`, `external_reference_id`, `transaction_date` (readonly).
    *   Make fields mostly readonly as transactions are typically system-generated. Manual adjustments might be possible via specific actions/wizards for admins.
*   **Search View (`creativeflow_credit_transaction_search`)**:
    *   Search by `user_id`, `type`, `description`, `reference_document`.
    *   Group by `user_id`, `type`.

##### 3.2.3.2. `views/credit_action_cost_views.xml`

*   **Tree View (`creativeflow_credit_action_cost_tree`)**:
    *   Fields: `name`, `cost`, `description`, `is_active`.
*   **Form View (`creativeflow_credit_action_cost_form`)**:
    *   Fields: `name`, `cost`, `description`, `is_active`.

##### 3.2.3.3. `views/res_users_credit_views.xml`

*   Inherit `res.users` form view (`base.view_users_form` or the one from `creativeflow_user_extensions`):
    *   Under the "CreativeFlow Details" tab, add a new group or section.
    *   Add a one2many field displaying `credit_transaction_ids` related to the user:
        xml
        <field name="credit_transaction_ids" nolabel="1" readonly="1">
            <tree string="Credit Transactions" default_order="transaction_date desc">
                <field name="transaction_date"/>
                <field name="type"/>
                <field name="amount"/>
                <field name="balance_after_transaction"/>
                <field name="description"/>
            </tree>
        </field>
        
        (Requires adding `credit_transaction_ids = fields.One2many('creativeflow.credit.transaction', 'user_id', string="Credit Transactions")` to `res.users` model in `creativeflow_credits/models/res_users_credit_mixin.py`).

##### 3.2.3.4. `views/credit_menus.xml`

*   Main Menu: "CreativeFlow Credits"
    *   Submenu: "Credit Transactions" (action: `creativeflow_credit_transaction_action`)
    *   Submenu: "Action Costs Configuration" (action: `creativeflow_credit_action_cost_action`)

#### 3.2.4. Data

##### 3.2.4.1. `data/credit_action_cost_data.xml`

*   Populate initial `creativeflow.credit.action.cost` records:
    *   ID: `action_cost_sample_gen`, Name: "sample_generation", Cost: 0.25, Description: "Cost for generating 4 low-resolution samples."
    *   ID: `action_cost_final_gen_std`, Name: "final_generation_standard_res", Cost: 1.0, Description: "Cost for generating one final standard resolution creative."
    *   ID: `action_cost_export_hd`, Name: "export_hd", Cost: 2.0, Description: "Cost for exporting a creative in High Definition."
    *   ID: `action_cost_api_gen_std`, Name: "api_generation_standard", Cost: 0.05, Description: "Cost per API generation call (standard)." (As per REQ-018)
    *   ... other actions as defined by REQ-016.

#### 3.2.5. Security

##### 3.2.5.1. `security/ir.model.access.csv`

| id                                            | name                                               | model_id/id                             | group_id/id               | perm_read | perm_write | perm_create | perm_unlink |
| :-------------------------------------------- | :------------------------------------------------- | :-------------------------------------- | :------------------------ | :-------- | :--------- | :---------- | :---------- |
| access_credit_transaction_admin               | creativeflow.credit.transaction.admin.access       | model_creativeflow_credit_transaction   | base.group_system         | 1         | 1          | 1           | 1           |
| access_credit_transaction_user                | creativeflow.credit.transaction.user.access        | model_creativeflow_credit_transaction   | base.group_user           | 1         | 0          | 0           | 0           |
| access_credit_action_cost_admin               | creativeflow.credit.action.cost.admin.access       | model_creativeflow_credit_action_cost   | base.group_system         | 1         | 1          | 1           | 1           |
| access_credit_action_cost_user                | creativeflow.credit.action.cost.user.access        | model_creativeflow_credit_action_cost   | base.group_user           | 1         | 0          | 0           | 0           |
> Note: User group access to transactions might be restricted further by record rules to only see their own, if exposed on a portal. Admins need full control for adjustments.

### 3.3. Module: `creativeflow_billing_subscription_extensions`

**Purpose**: To customize Odoo's standard subscription management (`sale_subscription` module) to align with CreativeFlow's specific requirements, such as linking to CreativeFlow users, managing initial credit grants, and syncing payment provider subscription IDs.

**Namespace**: `odoo.addons.creativeflow_billing_subscription_extensions`

#### 3.3.1. Manifest (`__manifest__.py`)

*   **`name`**: "CreativeFlow Billing & Subscription Extensions"
*   **`version`**: "18.0.1.0.0"
*   **`summary`**: "Extends Odoo subscription management for CreativeFlow specific logic."
*   **`category`**: "CreativeFlow/Billing"
*   **`author`**: "CreativeFlow AI Team"
*   **`website`**: "https://creativeflow.ai"
*   **`depends`**: `['sale_subscription', 'creativeflow_user_extensions', 'creativeflow_credits']`
*   **`data`**:
    *   `security/ir.model.access.csv`
    *   `views/sale_subscription_views.xml`
    *   `views/product_template_views.xml` (to link products to CF tiers)
*   **`installable`**: `True`
*   **`application`**: `False`
*   **`auto_install`**: `False`

#### 3.3.2. Models

##### 3.3.2.1. `models/sale_subscription.py` (Extending `sale.subscription`)

*   **`_inherit`**: `sale.subscription`
*   **Fields**:
    *   `cf_linked_user_id`:
        *   Type: `fields.Many2one`
        *   `comodel_name`: `'res.users'`
        *   String: "CreativeFlow User"
        *   `help`: "The CreativeFlow platform user associated with this Odoo subscription. Typically linked via partner's email or cf_external_user_id."
        *   `compute`: `'_compute_cf_linked_user_id'`
        *   `store`: `True`
        *   `readonly`: `True`
    *   `cf_subscription_tier_product`:
        *   Type: `fields.Selection`
        *   Related: `template_id.product_id.cf_subscription_tier_provided` (New field on product.template)
        *   String: "CF Tier (from Product)"
        *   `readonly`: `True`
        *   `store`: `True`
    *   `cf_initial_credits_on_period_start`:
        *   Type: `fields.Float`
        *   String: "Initial Credits per Period"
        *   Related: `template_id.product_id.cf_credits_granted_on_period_start` (New field on product.template)
        *   `help`: "Number of credits to grant the user at the start of each subscription period (e.g., monthly Pro credits). Fetched from the subscription product."
        *   `readonly`: `True`
    *   `cf_payment_provider_subscription_id`:
        *   Type: `fields.Char`
        *   String: "Payment Provider Subscription ID"
        *   `copy`: `False`
        *   `help`: "Subscription ID from external payment provider (e.g., Stripe, PayPal) for reconciliation."
*   **Methods**:
    *   `@api.depends('partner_id', 'partner_id.user_ids', 'partner_id.email')`
        `_compute_cf_linked_user_id(self)`:
        *   **Logic**:
            1.  For each subscription `sub`:
            2.  Attempt to find a `res.users` record. Priority:
                *   If `sub.partner_id.user_ids` is set (and only one, common case), use it.
                *   Else, search `res.users` where `partner_id == sub.partner_id.id`.
                *   Else, search `res.users` by `email == sub.partner_id.email` (if unique).
                *   Else, search `res.users` by `cf_external_user_id` if a mapping exists from another source.
            3.  Set `sub.cf_linked_user_id`.
    *   `_do_payment_and_grant_credits(self, payment_token, invoice)` (override or extend existing payment methods):
        *   **Logic**:
            1.  Call `super()._do_payment(...)` or equivalent for payment processing.
            2.  If payment is successful and invoice is for a new subscription period (or initial one):
                *   If `self.cf_linked_user_id` and `self.cf_initial_credits_on_period_start > 0`:
                    *   Call `self.cf_linked_user_id.action_credit_credits(self.cf_initial_credits_on_period_start, 'purchase', f"Credits for subscription {self.code} period start", external_reference_model='sale.order', external_reference_id=invoice.id)`.
    *   `_handle_subscription_ μετα(self, state)` (override or hook into state changes like `set_close`, `set_open`):
        *   **Logic**:
            1.  Call `super()._handle_subscription_ μετα(...)`.
            2.  If `self.cf_linked_user_id`:
                *   Update `self.cf_linked_user_id.cf_subscription_tier` based on `self.stage_id.category` (e.g., 'closed' -> 'free', 'progress' -> product's tier).
                *   This mapping needs to be robust (e.g. if subscription template product defines the tier).
    *   `action_sync_payment_provider_id(self)`:
        *   **Logic (Example for Stripe if direct integration or via connector)**:
            1.  If Odoo's payment acquirer has the subscription ID from Stripe (e.g., a Stripe connector might store this), fetch and update `self.cf_payment_provider_subscription_id`.
            > This might be more relevant if Odoo isn't the sole master for subscription creation initiated by the payment provider.

##### 3.3.2.2. `models/product_template.py` (Extending `product.template`)

*   **`_inherit`**: `product.template`
*   **Fields**:
    *   `cf_subscription_tier_provided`:
        *   Type: `fields.Selection`
        *   String: "CreativeFlow Tier Provided"
        *   `selection`: `[('free', 'Free'), ('pro', 'Pro'), ('team', 'Team'), ('enterprise', 'Enterprise')]`
        *   `help`: "The CreativeFlow subscription tier this product represents when sold as a subscription."
    *   `cf_credits_granted_on_period_start`:
        *   Type: `fields.Float`
        *   String: "Credits Granted Per Period"
        *   `digits`: `(16, 4)`
        *   `default`: `0.0`
        *   `help`: "Number of credits automatically granted to the user when a subscription period for this product starts/renews."

#### 3.3.3. Views

##### 3.3.3.1. `views/sale_subscription_views.xml`

*   Inherit `sale.subscription` form view (`sale_subscription.sale_subscription_view_form`):
    *   Add a "CreativeFlow" tab or group.
    *   Display fields: `cf_linked_user_id` (readonly), `cf_subscription_tier_product` (readonly), `cf_initial_credits_on_period_start` (readonly), `cf_payment_provider_subscription_id`.

##### 3.3.3.2. `views/product_template_views.xml`

*   Inherit `product.template` form view (`product.product_template_form_view`):
    *   Under "Sales" tab or a new "CreativeFlow Subscription" tab:
    *   Add fields: `cf_subscription_tier_provided`, `cf_credits_granted_on_period_start`.
    *   Make these fields visible only if `recurring_invoice == True`.

#### 3.3.4. Security

##### 3.3.4.1. `security/ir.model.access.csv`

| id                                           | name                                                   | model_id/id                 | group_id/id         | perm_read | perm_write | perm_create | perm_unlink |
| :------------------------------------------- | :----------------------------------------------------- | :-------------------------- | :------------------ | :-------- | :--------- | :---------- | :---------- |
| access_sale_subscription_cf_fields_admin     | sale.subscription.cf.fields.admin.access               | model_sale_subscription     | account.group_account_manager | 1         | 1          | 0           | 0           |
| access_product_template_cf_fields_admin      | product.template.cf.fields.admin.access                | model_product_template      | sales_team.group_sale_manager | 1         | 1          | 1           | 1           |
> Access to `sale.subscription` and `product.template` records themselves is handled by their respective base modules. This focuses on access to *new fields*.

### 3.4. Module: `creativeflow_brand_workbench_management`

**Purpose**: To provide Odoo models and basic UI for managing CreativeFlow Brand Kits and Workbenches. These are primarily for administrative overview or linking to Odoo entities like users or subscriptions if needed, as the main management is expected on the CreativeFlow platform.

**Namespace**: `odoo.addons.creativeflow_brand_workbench_management`

#### 3.4.1. Manifest (`__manifest__.py`)

*   **`name`**: "CreativeFlow Brand Kit & Workbench Management"
*   **`version`**: "18.0.1.0.0"
*   **`summary`**: "Basic Odoo models for CreativeFlow Brand Kits and Workbenches."
*   **`category`**: "CreativeFlow/Content Management"
*   **`author`**: "CreativeFlow AI Team"
*   **`website`**: "https://creativeflow.ai"
*   **`depends`**: `['base', 'mail', 'attachment_indexation', 'creativeflow_user_extensions']`
*   **`data`**:
    *   `security/ir.model.access.csv`
    *   `views/brand_kit_views.xml`
    *   `views/workbench_views.xml`
    *   `views/brand_workbench_menus.xml`
*   **`installable`**: `True`
*   **`application`**: `False`
*   **`auto_install`**: `False`

#### 3.4.2. Models

##### 3.4.2.1. `models/brand_kit.py`

*   **`_name`**: `creativeflow.brand.kit`
*   **`_description`**: "CreativeFlow Brand Kit"
*   **`_inherit`**: `['mail.thread', 'mail.activity.mixin']`
*   **Fields**:
    *   `name`: `fields.Char` (String: "Name", `required=True`)
    *   `user_id`: `fields.Many2one` (`comodel_name='res.users'`, String: "Owner", `required=True`, `index=True`)
    *   `cf_team_id_external`: `fields.Char` (String: "CreativeFlow Team ID (External)", `help`: "External ID of the team owning this brand kit, if applicable.")
    *   `colors_json`: `fields.Text` (String: "Colors (JSON)", `help`: "JSON string representing color palettes. E.g., [{'name': 'Primary', 'hex': '#FF0000'}]")
    *   `fonts_json`: `fields.Text` (String: "Fonts (JSON)", `help`: "JSON string representing font definitions. E.g., [{'name': 'Heading', 'family': 'Arial'}]")
    *   `logo_ids`: `fields.Many2many` (`comodel_name='ir.attachment'`, `relation='creativeflow_brand_kit_logo_rel'`, `column1='brand_kit_id'`, `column2='attachment_id'`, String: "Logos", `domain="[('res_model', '=', False), ('res_id', '=', False)]"`)
        > `ir.attachment` can be used to store logos. Ensure attachments are not linked to a specific `res_model` and `res_id` if they are general brand kit assets.
    *   `style_preferences_json`: `fields.Text` (String: "Style Preferences (JSON)")
    *   `is_default_for_user`: `fields.Boolean` (String: "Default Brand Kit for User")
    *   `cf_external_brand_kit_id`: `fields.Char` (String: "CreativeFlow Brand Kit ID (External)", `index=True`)
*   **Methods**:
    *   `@api.constrains('user_id', 'is_default_for_user')`
        `_check_unique_default_for_user(self)`:
        *   **Logic**: Ensure a user can only have one default brand kit. If `is_default_for_user` is True, search for other brand kits for the same user that are also default. If found, raise `ValidationError`.

##### 3.4.2.2. `models/workbench.py`

*   **`_name`**: `creativeflow.workbench`
*   **`_description`**: "CreativeFlow Workbench"
*   **`_inherit`**: `['mail.thread', 'mail.activity.mixin']`
*   **Fields**:
    *   `name`: `fields.Char` (String: "Name", `required=True`)
    *   `user_id`: `fields.Many2one` (`comodel_name='res.users'`, String: "Owner", `required=True`, `index=True`)
    *   `default_brand_kit_id`: `fields.Many2one` (`comodel_name='creativeflow.brand.kit'`, String: "Default Brand Kit", `domain="[('user_id', '=', user_id)]"`)
    *   `cf_project_ids_external`: `fields.Text` (String: "CreativeFlow Project IDs (JSON)", `help`: "JSON list of external CreativeFlow project identifiers belonging to this workbench.")
    *   `cf_external_workbench_id`: `fields.Char` (String: "CreativeFlow Workbench ID (External)", `index=True`)

#### 3.4.3. Views

##### 3.4.3.1. `views/brand_kit_views.xml`

*   **Tree View**: Fields: `name`, `user_id`, `is_default_for_user`, `cf_external_brand_kit_id`.
*   **Form View**: Fields arranged logically: `name`, `user_id`, `cf_team_id_external`, `is_default_for_user`, `cf_external_brand_kit_id`, and then `colors_json`, `fonts_json`, `style_preferences_json` (as text areas or using a custom widget if advanced display is needed for JSON in Odoo admin), `logo_ids` (using `many2many_binary` widget or similar for attachments).
*   **Search View**: Search by `name`, `user_id`. Filter by `is_default_for_user`.

##### 3.4.3.2. `views/workbench_views.xml`

*   **Tree View**: Fields: `name`, `user_id`, `default_brand_kit_id`, `cf_external_workbench_id`.
*   **Form View**: Fields: `name`, `user_id`, `default_brand_kit_id`, `cf_external_workbench_id`, `cf_project_ids_external` (as text area).
*   **Search View**: Search by `name`, `user_id`.

##### 3.4.3.3. `views/brand_workbench_menus.xml`

*   Main Menu: "CreativeFlow Content"
    *   Submenu: "Brand Kits" (action: `creativeflow_brand_kit_action`)
    *   Submenu: "Workbenches" (action: `creativeflow_workbench_action`)

#### 3.4.4. Security

##### 3.4.4.1. `security/ir.model.access.csv`

| id                                            | name                                             | model_id/id                         | group_id/id               | perm_read | perm_write | perm_create | perm_unlink |
| :-------------------------------------------- | :----------------------------------------------- | :---------------------------------- | :------------------------ | :-------- | :--------- | :---------- | :---------- |
| access_brand_kit_admin                        | creativeflow.brand.kit.admin.access              | model_creativeflow_brand_kit        | base.group_system         | 1         | 1          | 1           | 1           |
| access_brand_kit_user                         | creativeflow.brand.kit.user.access               | model_creativeflow_brand_kit        | base.group_user           | 1         | 1          | 1           | 1           |
| access_workbench_admin                        | creativeflow.workbench.admin.access              | model_creativeflow_workbench        | base.group_system         | 1         | 1          | 1           | 1           |
| access_workbench_user                         | creativeflow.workbench.user.access               | model_creativeflow_workbench        | base.group_user           | 1         | 1          | 1           | 1           |
> Record rules will be needed to restrict users to only manage their own brand kits/workbenches unless they are administrators.

### 3.5. Module: `creativeflow_support_ux_customizations`

**Purpose**: To customize the user experience of Odoo's Helpdesk and Knowledge modules, applying CreativeFlow branding and potentially adjusting workflows for a better fit with the platform's support strategy.

**Namespace**: `odoo.addons.creativeflow_support_ux_customizations`

#### 3.5.1. Manifest (`__manifest__.py`)

*   **`name`**: "CreativeFlow Support UX Customizations"
*   **`version`**: "18.0.1.0.0"
*   **`summary`**: "Customizes Odoo Helpdesk & Knowledge modules for CreativeFlow branding and UX."
*   **`category`**: "CreativeFlow/Support"
*   **`author`**: "CreativeFlow AI Team"
*   **`website`**: "https://creativeflow.ai"
*   **`depends`**: `['helpdesk', 'knowledge', 'website']` (website for portal view customizations)
*   **`data`**:
    *   `views/helpdesk_ticket_views.xml`
    *   `views/knowledge_article_views.xml`
    *   `views/support_portal_templates.xml` (for branding shared header/footer on portal)
*   **`assets`**:
    python
    'web.assets_frontend': [
        'creativeflow_support_ux_customizations/static/src/scss/creativeflow_branding.scss',
        # Potentially JS for minor UX tweaks if needed
        # 'creativeflow_support_ux_customizations/static/src/js/portal_enhancements.js',
    ],
    'web.assets_backend': [ # If backend views need CSS overrides
        # 'creativeflow_support_ux_customizations/static/src/scss/backend_branding.scss',
    ]
    
*   **`installable`**: `True`
*   **`application`**: `False`
*   **`auto_install`**: `False`

#### 3.5.2. Models

No new models or direct Python model extensions are planned for this module initially. Customizations are primarily view-based (XML, QWeb) and CSS/JS based. If complex workflow changes are needed that require Python logic, model extensions would be added here.

#### 3.5.3. Views

##### 3.5.3.1. `views/helpdesk_ticket_views.xml`

*   Inherit `helpdesk.ticket` portal form view (e.g., `helpdesk.portal_my_ticket`):
    *   Modify QWeb template to apply CreativeFlow branding (CSS classes, logos).
    *   Potentially re-arrange fields or simplify language for CreativeFlow users.
*   Inherit `helpdesk.ticket` backend form/tree views:
    *   Minor adjustments if needed to align with CreativeFlow operational workflows (e.g., adding quick links, changing field labels).

##### 3.5.3.2. `views/knowledge_article_views.xml`

*   Inherit `knowledge.article` portal views (e.g., `knowledge.knowledge_article_view_frontend`):
    *   Modify QWeb templates to apply CreativeFlow branding.
    *   Adjust layout for better readability and integration with the CreativeFlow aesthetic.
*   Inherit `knowledge.category` portal views similarly.

##### 3.5.3.3. `views/support_portal_templates.xml`

*   Define or inherit common portal layout templates (e.g., `website.layout` if applicable to Helpdesk/Knowledge portals).
*   Override header/footer sections to inject CreativeFlow branding, navigation links back to the main CreativeFlow app, etc.
*   Example:
    xml
    <template id="creativeflow_support_portal_layout" inherit_id="portal.portal_layout" name="CreativeFlow Support Portal Layout">
        <xpath expr="//header//nav" position="attributes">
            <attribute name="class" separator=" " add="cf-portal-header"/>
        </xpath>
        <!-- Further branding customizations -->
    </template>
    

#### 3.5.4. Static Assets

##### 3.5.4.1. `static/src/scss/creativeflow_branding.scss` (or .css)

*   **Purpose**: To apply CreativeFlow's visual identity (colors, fonts, logos, layout adjustments) to the Odoo Helpdesk and Knowledge portal pages.
*   **Content**:
    *   Define CSS variables for CreativeFlow brand colors, fonts.
    *   Override default Odoo portal styles for:
        *   Header, footer elements.
        *   Navigation bars.
        *   Buttons, form inputs.
        *   Typography (headings, body text).
        *   Specific Helpdesk/Knowledge element styling (e.g., ticket list items, article layout).
    *   Ensure responsiveness of custom styles.
    *   Example SCSS structure:
        scss
        // CF Variables
        $cf-primary-color: #your_brand_primary;
        $cf-font-family: 'Your Brand Font', sans-serif;

        // Overrides for Odoo Portal
        .o_portal_wrap {
          // ...
        }
        header.o_header_standard nav.navbar {
          background-color: $cf-primary-color;
          // ...
        }
        // Helpdesk specific
        .o_portal_helpdesk_ticket {
          // ...
        }
        // Knowledge specific
        .o_knowledge_content {
          // ...
        }
        

#### 3.5.5. Security

No new models, so `ir.model.access.csv` is not strictly required unless new fields are added to existing models that need specific permissions. Access to Helpdesk/Knowledge functionality itself is managed by their respective Odoo modules.

## 4. Cross-Module Considerations & API Design (Odoo Internal)

While this repository focuses on Odoo customizations, these modules will need to interact, and Odoo itself will interact with the broader CreativeFlow platform.

*   **User Synchronization**: The `cf_external_user_id` on `res.users` will be key for linking Odoo users to the main platform users. A separate service/process (outside this repo, likely in the main backend) will be responsible for syncing user data and ensuring this link is established, potentially upon user registration in the main platform or first interaction that requires Odoo data.
*   **Credit Balance Synchronization**: `res.users.credit_balance` in Odoo is primarily a read-only reflection or a tightly controlled field. The main platform's billing/credit service (which might call Odoo controller endpoints or use a message queue) will be the source of truth for credit balance changes. The `action_debit_credits` and `action_credit_credits` methods in Odoo serve as the mechanism for Odoo to *record* these changes initiated by the platform and update its local copy of the balance.
*   **Subscription Status Sync**: The `creativeflow_billing_subscription_extensions` module ensures that when an Odoo subscription's state changes (e.g., activated, cancelled), the linked `res.users` record's `cf_subscription_tier` is updated. This Odoo user data can then be queried by the main platform.
*   **API for External Platform Interaction**:
    *   If the main CreativeFlow platform needs to instruct Odoo to perform actions (e.g., "debit X credits for user Y for action Z"), secure Odoo controller endpoints will be necessary.
        *   **Authentication**: Service-to-service API key or OAuth2 client credentials.
        *   **Endpoint Example**: `POST /api/v1/creativeflow/user/<external_user_id>/debit_credits`
            *   Payload: `{ "action_identifier": "sample_generation", "amount": 0.25, "reference_details": { "generation_id": "ext_gen_123" }, "description": "Sample generation cost" }`
            *   Odoo controller would find the `res.users` by `cf_external_user_id`, then call the appropriate `action_debit_credits` method.
    *   Similarly for querying data from Odoo (e.g., user's subscription status if Odoo is the master for this).
*   **Idempotency**: Methods like `action_debit_credits` should be designed with idempotency in mind if called via potentially unreliable external APIs, e.g., by checking if a transaction for the same external reference already exists.

## 5. Future Considerations / Potential Extensions

*   **Brand Kit/Workbench Synchronization**: More robust synchronization of Brand Kit and Workbench data between Odoo and the main platform if these are actively managed in both systems rather than Odoo just holding references.
*   **Custom Widgets for JSON Fields**: For `colors_json`, `fonts_json`, etc., custom Odoo JavaScript widgets could be developed for a richer editing experience in the Odoo backend if admins need to manipulate this data directly in Odoo frequently.
*   **Advanced Reporting**: Odoo's reporting engine could be leveraged to create custom reports on credit usage, popular actions, etc., based on the data stored in these custom modules.

This SDS provides a foundational design. Specific implementation details, especially around API interactions and complex business logic within methods, will be further refined during the development phase for each module.