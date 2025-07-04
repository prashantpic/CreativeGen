# Specification

# 1. Files

- **Path:** erp/odoo-customizations/creativeflow_core/__init__.py  
**Description:** Initializes the Python package for the core CreativeFlow Odoo module, importing models and other sub-modules. This is essential for Odoo to recognize and load the module's Python components.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_core/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo for business logic)
    - Section 5.2.2 (Business Logic component description)
    
**Purpose:** Makes Python files in this module importable.  
**Logic Description:** Contains import statements for subdirectories like 'models'. For example: from . import models  
**Documentation:**
    
    - **Summary:** Core module Python package initializer.
    
**Namespace:** odoo.addons.creativeflow_core  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_core/__manifest__.py  
**Description:** Manifest file for the core CreativeFlow Odoo module. Defines module metadata, dependencies (e.g., on 'base', 'mail'), data files, and version. This file is critical for Odoo's module loading and management system.  
**Template:** Odoo Module Manifest  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** creativeflow_core/__manifest__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo for business logic)
    - Section 5.2.2 (Business Logic component description)
    
**Purpose:** Declares the Odoo module, its name, version, dependencies, and data files.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'category', 'depends' (e.g., ['base', 'web']), 'data' (list of XML files), 'installable', 'application'.  
**Documentation:**
    
    - **Summary:** Defines metadata and dependencies for the creativeflow_core Odoo module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_core/models/__init__.py  
**Description:** Initializes the Python package for models within the creativeflow_core module. Imports all model files defined in this directory.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_core/models/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Initialization
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo for business logic)
    
**Purpose:** Makes model files in this directory importable.  
**Logic Description:** Contains import statements for model files, e.g., from . import res_partner_extension  
**Documentation:**
    
    - **Summary:** Initializes Python models for creativeflow_core.
    
**Namespace:** odoo.addons.creativeflow_core.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_core/models/res_partner_extension.py  
**Description:** Extends Odoo's 'res.partner' model (contacts/users) to add CreativeFlow-specific fields relevant for Odoo's context, if any, beyond the main user management system. This could include fields like synced credit balance or subscription tier display for Odoo admin views.  
**Template:** Odoo Model Extension  
**Dependency Level:** 2  
**Name:** res_partner_extension  
**Type:** Odoo Model  
**Relative Path:** creativeflow_core/models/res_partner_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    - Active Record
    
**Members:**
    
    - **Name:** _inherit  
**Type:** str  
**Attributes:** private  
    - **Name:** cf_synced_credit_balance  
**Type:** fields.Float  
**Attributes:** public  
    - **Name:** cf_synced_subscription_tier  
**Type:** fields.Char  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** action_sync_with_platform  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - User Data Extension for Odoo Context
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo for business logic)
    - comp.backend.odoo.userMgmtModule
    
**Purpose:** Adds platform-specific fields to Odoo's contact/user model for internal Odoo views or processes.  
**Logic Description:** Inherits 'res.partner'. Defines new fields using Odoo's fields API (e.g., fields.Float, fields.Char). May include methods for syncing data with the main CreativeFlow platform if Odoo needs to reflect certain states.  
**Documentation:**
    
    - **Summary:** Extends res.partner model with CreativeFlow specific synchronized data.
    
**Namespace:** odoo.addons.creativeflow_core.models.res_partner_extension  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_core/views/res_partner_views_extension.xml  
**Description:** XML file to extend existing 'res.partner' views (form, tree) to display the new CreativeFlow-specific fields. This makes the extended information visible in Odoo's user interface.  
**Template:** Odoo View XML  
**Dependency Level:** 3  
**Name:** res_partner_views_extension  
**Type:** Odoo View  
**Relative Path:** creativeflow_core/views/res_partner_views_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Display Extended User Data in UI
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo for business logic)
    
**Purpose:** Modifies Odoo contact/user views to show custom fields.  
**Logic Description:** Uses Odoo's XML view inheritance mechanism. Specifies <record> elements to inherit existing views (e.g., 'view_partner_form') and adds new <field> elements within <xpath> expressions to place them on the form or in list views.  
**Documentation:**
    
    - **Summary:** Extends Odoo res.partner views to include CreativeFlow fields.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_core/security/ir.model.access.csv  
**Description:** Defines access control lists (ACLs) for models in the creativeflow_core module, specifying which user groups have read, write, create, or delete permissions.  
**Template:** Odoo Security CSV  
**Dependency Level:** 3  
**Name:** ir.model.access  
**Type:** Odoo Security  
**Relative Path:** creativeflow_core/security/ir.model.access  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Access Control
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo for business logic)
    
**Purpose:** Manages permissions for models within this module.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Each row defines permissions for a specific model and group.  
**Documentation:**
    
    - **Summary:** Access rights for creativeflow_core models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/__init__.py  
**Description:** Initializes the Python package for the subscription and billing CreativeFlow Odoo module.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_subscription_billing/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    
**Purpose:** Makes Python files in this module importable.  
**Logic Description:** Contains import statements for subdirectories like 'models', 'controllers', 'services'. E.g., from . import models  
**Documentation:**
    
    - **Summary:** Subscription & Billing module Python package initializer.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/__manifest__.py  
**Description:** Manifest file for the CreativeFlow Subscription & Billing module. Defines dependencies on Odoo apps like 'sale_subscription', 'account', 'payment', and potentially 'creativeflow_core'. Lists data files for payment acquirers, subscription product templates.  
**Template:** Odoo Module Manifest  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** creativeflow_subscription_billing/__manifest__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Declares the module, its dependencies (e.g., sale_subscription, payment, account, creativeflow_core), and data files.  
**Logic Description:** Python dictionary specifying 'name', 'version', 'depends': ['sale_subscription', 'payment', 'account', 'creativeflow_core'], 'data': ['security/ir.model.access.csv', 'views/subscription_views.xml', 'data/payment_acquirer_data.xml', 'data/subscription_product_data.xml'].  
**Documentation:**
    
    - **Summary:** Defines metadata for the CreativeFlow Subscription & Billing Odoo module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/models/__init__.py  
**Description:** Initializes the Python package for models within the subscription and billing module.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_subscription_billing/models/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Initialization
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    
**Purpose:** Makes model files importable.  
**Logic Description:** Imports model files: from . import res_partner_billing_extension, sale_subscription_extension, account_payment_acquirer, credit_management  
**Documentation:**
    
    - **Summary:** Initializes Python models for subscription and billing.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/models/res_partner_billing_extension.py  
**Description:** Extends 'res.partner' to add credit balance field and methods for credit management specific to CreativeFlow logic within Odoo. This is distinct from the main platform's user credit balance but might be synced or used for Odoo-internal processes.  
**Template:** Odoo Model Extension  
**Dependency Level:** 2  
**Name:** res_partner_billing_extension  
**Type:** Odoo Model  
**Relative Path:** creativeflow_subscription_billing/models/res_partner_billing_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    - Active Record
    
**Members:**
    
    - **Name:** _inherit  
**Type:** str  
**Attributes:** private  
    - **Name:** cf_credit_balance  
**Type:** fields.Float  
**Attributes:** public  
**Notes:** Credit balance specific to Odoo context  
    - **Name:** cf_subscription_ids  
**Type:** fields.One2many  
**Attributes:** public  
**Notes:** Link to sale.subscription records  
    
**Methods:**
    
    - **Name:** add_credits  
**Parameters:**
    
    - amount
    - description=None
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** deduct_credits  
**Parameters:**
    
    - amount
    - description=None
    - related_document=None
    
**Return Type:** boolean  
**Attributes:** public  
    - **Name:** _create_credit_transaction_log  
**Parameters:**
    
    - amount
    - description
    - transaction_type
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - Odoo-side Credit Balance Management
    - User Subscription Linking
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    - comp.backend.odoo.billingSubModule
    
**Purpose:** Adds and manages credit balance on Odoo partner records, logs transactions.  
**Logic Description:** Inherits 'res.partner'. Defines 'cf_credit_balance' field. Methods 'add_credits' and 'deduct_credits' modify this balance and create corresponding log entries (potentially in a custom 'cf.credit.transaction.log' model). Ensures sufficient balance before deduction. Handles logic related to subscription tiers if impacting credits.  
**Documentation:**
    
    - **Summary:** Manages partner-specific credit balance and transaction logging within Odoo.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.models.res_partner_billing_extension  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/models/sale_subscription_extension.py  
**Description:** Extends Odoo's 'sale.subscription' model to add custom fields or logic specific to CreativeFlow, such as linking to platform-specific plans, handling grace periods, or specific dunning email triggers.  
**Template:** Odoo Model Extension  
**Dependency Level:** 2  
**Name:** sale_subscription_extension  
**Type:** Odoo Model  
**Relative Path:** creativeflow_subscription_billing/models/sale_subscription_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    - Active Record
    
**Members:**
    
    - **Name:** _inherit  
**Type:** str  
**Attributes:** private  
    - **Name:** cf_platform_plan_id  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** cf_credit_allotment_per_cycle  
**Type:** fields.Float  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _recurring_invoice  
**Parameters:**
    
    
**Return Type:** super  
**Attributes:** public  
**Notes:** Override to add custom logic before/after invoice creation e.g., credit top-up  
    - **Name:** action_sync_status_to_platform  
**Parameters:**
    
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Custom Subscription Logic
    - Platform Plan Linking
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    
**Purpose:** Customizes Odoo subscriptions for CreativeFlow needs, e.g. mapping to platform plans, custom actions on renewal.  
**Logic Description:** Inherits 'sale.subscription'. Adds fields for platform-specific plan identifiers or features. Overrides existing methods like '_recurring_invoice' to implement custom logic on subscription renewal or status changes. May interact with credit balance logic.  
**Documentation:**
    
    - **Summary:** Extends Odoo's sale.subscription model for CreativeFlow.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.models.sale_subscription_extension  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/models/account_payment_acquirer_extension.py  
**Description:** Extends Odoo's 'payment.acquirer' model to potentially store additional configuration for Stripe/PayPal specific to CreativeFlow or to customize webhook handling logic.  
**Template:** Odoo Model Extension  
**Dependency Level:** 2  
**Name:** account_payment_acquirer_extension  
**Type:** Odoo Model  
**Relative Path:** creativeflow_subscription_billing/models/account_payment_acquirer_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** _inherit  
**Type:** str  
**Attributes:** private  
    - **Name:** cf_custom_config  
**Type:** fields.Text  
**Attributes:** public  
    
**Methods:**
    
    - **Name:** _get_default_payment_method_id  
**Parameters:**
    
    
**Return Type:** super  
**Attributes:** public  
**Notes:** Potentially customize default payment method selection  
    
**Implemented Features:**
    
    - Payment Acquirer Customization
    
**Requirement Ids:**
    
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Allows for specific configurations or behavior overrides for payment acquirers (Stripe, PayPal).  
**Logic Description:** Inherits 'payment.acquirer'. Adds any custom configuration fields needed. May override methods related to transaction processing or webhook handling if Odoo's base behavior needs adjustment for CreativeFlow.  
**Documentation:**
    
    - **Summary:** Extends Odoo's payment.acquirer model.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.models.account_payment_acquirer_extension  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/controllers/__init__.py  
**Description:** Initializes the Python package for controllers within the subscription and billing module.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_subscription_billing/controllers/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Controller Initialization
    
**Requirement Ids:**
    
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Makes controller files importable.  
**Logic Description:** Imports controller files: from . import payment_webhook_controller  
**Documentation:**
    
    - **Summary:** Initializes Python controllers for subscription and billing.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.controllers  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/controllers/payment_webhook_controller.py  
**Description:** Defines Odoo HTTP controllers to handle incoming webhook notifications from payment gateways like Stripe and PayPal. These webhooks inform Odoo about payment success, failures, subscription updates, etc.  
**Template:** Odoo Controller  
**Dependency Level:** 3  
**Name:** payment_webhook_controller  
**Type:** Odoo Controller  
**Relative Path:** creativeflow_subscription_billing/controllers/payment_webhook_controller  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - MVC
    - Webhook Handler
    
**Members:**
    
    
**Methods:**
    
    - **Name:** stripe_webhook  
**Parameters:**
    
    - **kwargs
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** public|http route='/payment/stripe/webhook' auth='public' methods=['POST'] csrf=False  
    - **Name:** paypal_webhook  
**Parameters:**
    
    - **kwargs
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** public|http route='/payment/paypal/webhook' auth='public' methods=['POST'] csrf=False  
    - **Name:** _process_stripe_event  
**Parameters:**
    
    - event_data
    
**Return Type:** None  
**Attributes:** private  
    - **Name:** _process_paypal_event  
**Parameters:**
    
    - event_data
    
**Return Type:** None  
**Attributes:** private  
    
**Implemented Features:**
    
    - Payment Gateway Webhook Handling
    
**Requirement Ids:**
    
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Receives and processes webhook notifications from Stripe and PayPal.  
**Logic Description:** Defines HTTP routes for Stripe and PayPal webhooks. Verifies webhook signatures. Parses event data (e.g., 'invoice.payment_succeeded', 'customer.subscription.updated'). Calls internal Odoo service methods or model methods to update subscription statuses, create payments, generate invoices, or handle payment failures based on the event.  
**Documentation:**
    
    - **Summary:** Handles webhook events from payment providers like Stripe and PayPal.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.controllers.payment_webhook_controller  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/services/__init__.py  
**Description:** Initializes the Python package for services within the subscription and billing module.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_subscription_billing/services/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Service Initialization
    
**Requirement Ids:**
    
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Makes service files importable.  
**Logic Description:** Imports service files: from . import billing_service  
**Documentation:**
    
    - **Summary:** Initializes Python services for subscription and billing.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/services/billing_service.py  
**Description:** Contains business logic services related to billing, subscription management, and payment processing that might be too complex for model methods or need to orchestrate multiple models. For instance, handling complex dunning logic or tax calculations if not fully covered by base Odoo.  
**Template:** Odoo Service  
**Dependency Level:** 3  
**Name:** billing_service  
**Type:** Odoo Service  
**Relative Path:** creativeflow_subscription_billing/services/billing_service  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Service Layer
    
**Members:**
    
    
**Methods:**
    
    - **Name:** process_payment_confirmation  
**Parameters:**
    
    - payment_data
    - acquirer_short_code
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** handle_subscription_renewal  
**Parameters:**
    
    - subscription_id
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** apply_taxes_to_invoice  
**Parameters:**
    
    - invoice_id
    
**Return Type:** None  
**Attributes:** public  
    - **Name:** trigger_dunning_process  
**Parameters:**
    
    - subscription_id
    
**Return Type:** None  
**Attributes:** public  
    
**Implemented Features:**
    
    - Advanced Billing Logic
    - Tax Calculation Orchestration
    - Dunning Process Management
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Encapsulates complex billing and subscription lifecycle logic.  
**Logic Description:** Methods for processing confirmed payments from webhooks, managing subscription renewals (e.g., credit top-ups), applying tax rules (potentially interacting with Odoo's tax engine), and initiating dunning sequences for failed payments. Interacts with various Odoo models like 'sale.subscription', 'account.move', 'res.partner'.  
**Documentation:**
    
    - **Summary:** Provides core services for managing billing, subscriptions, and payments within Odoo.
    
**Namespace:** odoo.addons.creativeflow_subscription_billing.services.billing_service  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/data/payment_acquirer_data.xml  
**Description:** XML data file to configure payment acquirers like Stripe and PayPal within Odoo. Sets up API keys (placeholders, actual keys via Odoo UI/env vars), URLs, and other acquirer-specific settings.  
**Template:** Odoo Data XML  
**Dependency Level:** 3  
**Name:** payment_acquirer_data  
**Type:** Odoo Data  
**Relative Path:** creativeflow_subscription_billing/data/payment_acquirer_data  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Payment Acquirer Configuration
    
**Requirement Ids:**
    
    - INT-003 (Payment processing integrated with Odoo)
    
**Purpose:** Initializes and configures payment acquirers (Stripe, PayPal).  
**Logic Description:** Contains <record> elements for 'payment.acquirer' model, defining Stripe and PayPal acquirers with their respective provider codes, state (test/enabled), and placeholder API credentials. Also defines payment methods associated with these acquirers.  
**Documentation:**
    
    - **Summary:** Data for setting up payment acquirers.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/data/subscription_product_data.xml  
**Description:** XML data file to define subscription products (e.g., Free, Pro, Team, Enterprise tiers) in Odoo. These products are used in sale orders and subscriptions, linking to pricing and features.  
**Template:** Odoo Data XML  
**Dependency Level:** 3  
**Name:** subscription_product_data  
**Type:** Odoo Data  
**Relative Path:** creativeflow_subscription_billing/data/subscription_product_data  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Subscription Plan Definition
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    
**Purpose:** Defines the various subscription plans/products offered.  
**Logic Description:** Contains <record> elements for 'product.template' or 'product.product' models, creating records for each subscription tier (Free, Pro, Team, Enterprise). Specifies product type as 'service', subscription-related fields (e.g., recurring invoice plan), pricing, and potentially links to specific credit allotments or features.  
**Documentation:**
    
    - **Summary:** Data for defining subscription products.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/views/subscription_views.xml  
**Description:** XML views for managing subscriptions, credit balances, and billing related information within Odoo's backend interface.  
**Template:** Odoo View XML  
**Dependency Level:** 3  
**Name:** subscription_views  
**Type:** Odoo View  
**Relative Path:** creativeflow_subscription_billing/views/subscription_views  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin UI for Billing Management
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    
**Purpose:** Defines Odoo admin views for managing subscription plans, viewing customer subscriptions, and credit balances.  
**Logic Description:** Contains <record> elements for 'ir.ui.view' and 'ir.actions.act_window' defining form, tree, and search views for custom billing models or extended Odoo models (e.g., sale.subscription, res.partner with credit balance). Also defines menu items to access these views.  
**Documentation:**
    
    - **Summary:** Odoo views related to subscription and billing management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_subscription_billing/security/ir.model.access.csv  
**Description:** Defines access control for models within the subscription and billing module.  
**Template:** Odoo Security CSV  
**Dependency Level:** 3  
**Name:** ir.model.access  
**Type:** Odoo Security  
**Relative Path:** creativeflow_subscription_billing/security/ir.model.access  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Billing Model Access Control
    
**Requirement Ids:**
    
    - Section 3.4 (Subscription and Billing functions often in Odoo)
    
**Purpose:** Manages permissions for billing and subscription models.  
**Logic Description:** CSV defining access rights for models like extended 'res.partner', 'sale.subscription', and any custom billing/credit models to specific user groups (e.g., Billing Manager, Sales User).  
**Documentation:**
    
    - **Summary:** Access rights for subscription and billing models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/__init__.py  
**Description:** Initializes the Python package for the CreativeFlow Helpdesk Odoo module.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_helpdesk/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    
**Purpose:** Makes Python files in this module importable.  
**Logic Description:** Imports 'models' subdirectory if any custom models or extensions are defined.  
**Documentation:**
    
    - **Summary:** Helpdesk module Python package initializer.
    
**Namespace:** odoo.addons.creativeflow_helpdesk  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/__manifest__.py  
**Description:** Manifest file for the CreativeFlow Helpdesk module. Declares dependencies on Odoo's 'helpdesk', 'website_helpdesk' (for portal access), 'knowledge' (or 'website_knowledge') modules.  
**Template:** Odoo Module Manifest  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** creativeflow_helpdesk/__manifest__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    
**Purpose:** Declares the helpdesk module and its dependencies (e.g., helpdesk, knowledge, website_helpdesk).  
**Logic Description:** Python dictionary specifying 'name', 'version', 'depends': ['helpdesk', 'knowledge', 'website_helpdesk', 'creativeflow_core'], 'data': ['security/ir.model.access.csv', 'views/helpdesk_views_extension.xml', 'data/helpdesk_team_data.xml'].  
**Documentation:**
    
    - **Summary:** Defines metadata for the CreativeFlow Helpdesk Odoo module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/models/__init__.py  
**Description:** Initializes models for the helpdesk module, if any extensions are made.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_helpdesk/models/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Initialization
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    
**Purpose:** Imports any custom model extensions.  
**Logic Description:** from . import helpdesk_ticket_extension  
**Documentation:**
    
    - **Summary:** Models init for helpdesk.
    
**Namespace:** odoo.addons.creativeflow_helpdesk.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/models/helpdesk_ticket_extension.py  
**Description:** Extends Odoo's 'helpdesk.ticket' model to add fields or logic specific to CreativeFlow, such as linking tickets to specific platform features or user actions if needed.  
**Template:** Odoo Model Extension  
**Dependency Level:** 2  
**Name:** helpdesk_ticket_extension  
**Type:** Odoo Model  
**Relative Path:** creativeflow_helpdesk/models/helpdesk_ticket_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** _inherit  
**Type:** str  
**Attributes:** private  
    - **Name:** cf_related_feature_area  
**Type:** fields.Selection  
**Attributes:** public  
**Notes:** Selection field for platform areas  
    - **Name:** cf_user_subscription_tier_at_creation  
**Type:** fields.Char  
**Attributes:** public  
**Notes:** Capture user's tier when ticket is made  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Helpdesk Ticket Fields
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    - comp.backend.odoo.helpdeskModule
    
**Purpose:** Adds CreativeFlow-specific context to helpdesk tickets.  
**Logic Description:** Inherits 'helpdesk.ticket'. Adds fields like 'cf_related_feature_area' (e.g., 'AI Generation', 'Billing', 'Mobile App') or 'cf_user_subscription_tier_at_creation' to provide more context for support agents.  
**Documentation:**
    
    - **Summary:** Extends Odoo helpdesk.ticket model for CreativeFlow.
    
**Namespace:** odoo.addons.creativeflow_helpdesk.models.helpdesk_ticket_extension  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/data/helpdesk_team_data.xml  
**Description:** XML data file to create default helpdesk teams, stages, and potentially ticket types relevant for CreativeFlow support (e.g., Technical Support, Billing Support).  
**Template:** Odoo Data XML  
**Dependency Level:** 3  
**Name:** helpdesk_team_data  
**Type:** Odoo Data  
**Relative Path:** creativeflow_helpdesk/data/helpdesk_team_data  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Helpdesk Team Configuration
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    
**Purpose:** Initializes helpdesk teams and related configurations.  
**Logic Description:** Contains <record> elements for 'helpdesk.team' model, creating default support teams. May also define 'helpdesk.stage' records for ticket lifecycle management tailored to CreativeFlow.  
**Documentation:**
    
    - **Summary:** Data for setting up default helpdesk teams and stages.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/views/helpdesk_views_extension.xml  
**Description:** XML file to extend 'helpdesk.ticket' views to display new custom fields or modify layout for CreativeFlow support agents.  
**Template:** Odoo View XML  
**Dependency Level:** 3  
**Name:** helpdesk_views_extension  
**Type:** Odoo View  
**Relative Path:** creativeflow_helpdesk/views/helpdesk_views_extension  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Customized Helpdesk UI
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    
**Purpose:** Modifies helpdesk ticket views for CreativeFlow context.  
**Logic Description:** Uses Odoo's XML view inheritance to add new fields (like 'cf_related_feature_area') to the ticket form view, or to customize list views and search filters for support agents.  
**Documentation:**
    
    - **Summary:** Extends Odoo helpdesk views.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_helpdesk/security/ir.model.access.csv  
**Description:** Defines access control for any custom models or ensures appropriate access to extended helpdesk models within this module.  
**Template:** Odoo Security CSV  
**Dependency Level:** 3  
**Name:** ir.model.access  
**Type:** Odoo Security  
**Relative Path:** creativeflow_helpdesk/security/ir.model.access  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Helpdesk Model Access Control
    
**Requirement Ids:**
    
    - Section 3.7 (Support and Help System via Odoo modules)
    
**Purpose:** Manages permissions for helpdesk related models.  
**Logic Description:** CSV defining access rights for extended 'helpdesk.ticket' or any custom support-related models for groups like 'Support Agent', 'Support Manager'.  
**Documentation:**
    
    - **Summary:** Access rights for helpdesk models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/__init__.py  
**Description:** Initializes the Python package for the Template Catalog Odoo module if platform templates are managed via Odoo.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_template_catalog/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Makes Python files for template catalog module importable.  
**Logic Description:** Imports 'models' subdirectory.  
**Documentation:**
    
    - **Summary:** Template Catalog module Python package initializer.
    
**Namespace:** odoo.addons.creativeflow_template_catalog  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/__manifest__.py  
**Description:** Manifest file for the CreativeFlow Template Catalog module. Defines dependencies and data files for managing template metadata in Odoo.  
**Template:** Odoo Module Manifest  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Manifest  
**Relative Path:** creativeflow_template_catalog/__manifest__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Declares the template catalog module.  
**Logic Description:** Python dictionary specifying 'name', 'version', 'depends': ['base', 'creativeflow_core'], 'data': ['security/ir.model.access.csv', 'views/template_views.xml', 'data/template_category_data.xml'].  
**Documentation:**
    
    - **Summary:** Defines metadata for the CreativeFlow Template Catalog Odoo module.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/models/__init__.py  
**Description:** Initializes models for the template catalog module.  
**Template:** Odoo Module Python Init  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Init  
**Relative Path:** creativeflow_template_catalog/models/__init__  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - Module
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Initialization
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Imports template catalog model files.  
**Logic Description:** from . import creative_template, template_category  
**Documentation:**
    
    - **Summary:** Models init for template catalog.
    
**Namespace:** odoo.addons.creativeflow_template_catalog.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/models/creative_template.py  
**Description:** Odoo model to store metadata for CreativeFlow templates, such as name, description, category, tags, preview image URL (MinIO path), and potentially a JSON representation of the template structure if not too complex.  
**Template:** Odoo Model  
**Dependency Level:** 2  
**Name:** creative_template  
**Type:** Odoo Model  
**Relative Path:** creativeflow_template_catalog/models/creative_template  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private  
**Default Value:** 'creativeflow.template'  
    - **Name:** _description  
**Type:** str  
**Attributes:** private  
**Default Value:** 'CreativeFlow Template'  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
**Is Required:** True  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** public  
    - **Name:** category_id  
**Type:** fields.Many2one  
**Attributes:** public  
**Related Model:** creativeflow.template.category  
    - **Name:** tags  
**Type:** fields.Char  
**Attributes:** public  
**Notes:** Comma-separated tags  
    - **Name:** preview_image_url  
**Type:** fields.Char  
**Attributes:** public  
    - **Name:** template_json_data  
**Type:** fields.Text  
**Attributes:** public  
**Notes:** JSON data for the template structure  
    - **Name:** is_active  
**Type:** fields.Boolean  
**Attributes:** public  
**Default Value:** True  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Template Metadata Management
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Stores and manages metadata about creative templates available on the platform.  
**Logic Description:** Defines fields for template name, description, category, tags, preview URL, and actual template data (e.g., as JSON). This allows admins to manage the template library through Odoo's UI.  
**Documentation:**
    
    - **Summary:** Odoo model for CreativeFlow template metadata.
    
**Namespace:** odoo.addons.creativeflow_template_catalog.models.creative_template  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/models/template_category.py  
**Description:** Odoo model for categorizing creative templates (e.g., 'Social Media Post', 'Banner Ad', 'Industry Specific').  
**Template:** Odoo Model  
**Dependency Level:** 2  
**Name:** template_category  
**Type:** Odoo Model  
**Relative Path:** creativeflow_template_catalog/models/template_category  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - ORM
    
**Members:**
    
    - **Name:** _name  
**Type:** str  
**Attributes:** private  
**Default Value:** 'creativeflow.template.category'  
    - **Name:** _description  
**Type:** str  
**Attributes:** private  
**Default Value:** 'CreativeFlow Template Category'  
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** public  
**Is Required:** True  
    - **Name:** parent_id  
**Type:** fields.Many2one  
**Attributes:** public  
**Related Model:** creativeflow.template.category  
**Notes:** For hierarchical categories  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Template Categorization
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Manages categories for organizing creative templates.  
**Logic Description:** Defines fields for category name and an optional parent category to allow for hierarchical categorization of templates.  
**Documentation:**
    
    - **Summary:** Odoo model for template categories.
    
**Namespace:** odoo.addons.creativeflow_template_catalog.models.template_category  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/views/template_views.xml  
**Description:** XML views for managing creative templates and their categories in Odoo's backend.  
**Template:** Odoo View XML  
**Dependency Level:** 3  
**Name:** template_views  
**Type:** Odoo View  
**Relative Path:** creativeflow_template_catalog/views/template_views  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin UI for Template Management
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Defines Odoo admin views for template and category management.  
**Logic Description:** Contains <record> elements for 'ir.ui.view' and 'ir.actions.act_window' defining form, tree, and search views for 'creativeflow.template' and 'creativeflow.template.category' models. Includes menu items for easy access.  
**Documentation:**
    
    - **Summary:** Odoo views for managing creative templates and categories.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-customizations/creativeflow_template_catalog/security/ir.model.access.csv  
**Description:** Defines access control for template catalog models.  
**Template:** Odoo Security CSV  
**Dependency Level:** 3  
**Name:** ir.model.access  
**Type:** Odoo Security  
**Relative Path:** creativeflow_template_catalog/security/ir.model.access  
**Repository Id:** REPO-ODOO-ERP-PLATFORM-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Template Catalog Model Access Control
    
**Requirement Ids:**
    
    - comp.backend.odoo.contentMgmtModule
    
**Purpose:** Manages permissions for template and category models.  
**Logic Description:** CSV defining access rights for 'creativeflow.template' and 'creativeflow.template.category' models to specific user groups (e.g., Content Manager, Administrator).  
**Documentation:**
    
    - **Summary:** Access rights for template catalog models.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_custom_credit_logic_in_odoo
  - enable_extended_helpdesk_fields
  - manage_templates_in_odoo
  
- **Database Configs:**
  
  - odoo_db_host (via odoo.conf)
  - odoo_db_port (via odoo.conf)
  - odoo_db_user (via odoo.conf)
  - odoo_db_password (via odoo.conf)
  - odoo_db_name (via odoo.conf)
  


---

