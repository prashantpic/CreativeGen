# Specification

# 1. Files

- **Path:** erp/odoo-creativeflow-custom/creativeflow_user_extensions/__init__.py  
**Description:** Initializes the Python submodules for the creativeflow_user_extensions Odoo module.  
**Template:** Odoo Module Init (Python)  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - Section 5.2.2 (User Management Odoo Mod.)
    
**Purpose:** To make Python models and other Python code within this module discoverable by Odoo.  
**Logic Description:** Imports the 'models' subdirectory.  
**Documentation:**
    
    - **Summary:** Standard Odoo Python module initializer.
    
**Namespace:** odoo.addons.creativeflow_user_extensions  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_user_extensions/__manifest__.py  
**Description:** Manifest file for the creativeflow_user_extensions Odoo module. Defines module metadata, dependencies, and data files.  
**Template:** Odoo Manifest (Python Dict)  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Dependency Management
    
**Requirement Ids:**
    
    - Section 5.2.2 (User Management Odoo Mod.)
    - REQ-016
    
**Purpose:** To declare the module to Odoo, specify its properties, dependencies (e.g., 'base', 'mail'), and data files to be loaded.  
**Logic Description:** Dictionary containing 'name', 'version', 'summary', 'category', 'author', 'website', 'depends', 'data', 'installable', 'application'. Dependencies should include 'base'. Data files will list XML views and security files.  
**Documentation:**
    
    - **Summary:** Defines the 'CreativeFlow User Extensions' module for Odoo.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_user_extensions/models/__init__.py  
**Description:** Initializes the Python models for the creativeflow_user_extensions module.  
**Template:** Odoo Models Init (Python)  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Models Init  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    - Section 5.2.2 (User Management Odoo Mod.)
    
**Purpose:** To make individual model files within the 'models' directory discoverable by the module.  
**Logic Description:** Imports specific model files like 'res_users.py'.  
**Documentation:**
    
    - **Summary:** Standard Odoo models directory initializer.
    
**Namespace:** odoo.addons.creativeflow_user_extensions.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_user_extensions/models/res_users.py  
**Description:** Extends the Odoo 'res.users' model to add CreativeFlow-specific fields.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** res_users  
**Type:** Odoo Model Extension  
**Relative Path:** models/res_users.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** credit_balance  
**Type:** fields.Float  
**Attributes:**   
    - **Name:** cf_subscription_tier  
**Type:** fields.Selection  
**Attributes:**   
    - **Name:** cf_external_user_id  
**Type:** fields.Char  
**Attributes:**   
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Credit Balance Storage
    - Subscription Tier Tracking
    - External User ID Mapping
    
**Requirement Ids:**
    
    - REQ-016
    - Section 5.2.2 (User Management Odoo Mod.)
    
**Purpose:** To store CreativeFlow-specific user attributes like credit balance and subscription tier directly on the user model for easy access and integration with Odoo functionalities.  
**Logic Description:** Inherits from 'res.users'. Defines fields: credit_balance (Float, string='Credit Balance', readonly=True, help='User current credit balance, synced from platform.'), cf_subscription_tier (Selection, string='CF Subscription Tier', selection=[('free','Free'),('pro','Pro'),('team','Team'),('enterprise','Enterprise')]), cf_external_user_id (Char, string='CreativeFlow User ID', help='User ID from the main CreativeFlow platform if different from Odoo ID'). Related fields might also be added to res.partner if users are primarily managed as partners.  
**Documentation:**
    
    - **Summary:** Adds CreativeFlow specific fields to the standard Odoo user model.
    
**Namespace:** odoo.addons.creativeflow_user_extensions.models.res_users  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_user_extensions/views/res_users_views.xml  
**Description:** XML views to display CreativeFlow-specific fields on the 'res.users' form and tree views.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** res_users_views  
**Type:** Odoo View Definition  
**Relative Path:** views/res_users_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - User Profile UI Extension
    
**Requirement Ids:**
    
    - REQ-016
    - Section 5.2.2 (User Management Odoo Mod.)
    
**Purpose:** To make the custom CreativeFlow user fields visible and manageable within the Odoo user interface.  
**Logic Description:** Defines <record> elements for ir.ui.view. Inherits existing 'res.users.form' and 'res.users.tree' views to add new fields (credit_balance, cf_subscription_tier, cf_external_user_id) in appropriate sections, possibly under a new 'CreativeFlow' tab or group.  
**Documentation:**
    
    - **Summary:** Customizes Odoo user views to include CreativeFlow fields.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_user_extensions/security/ir.model.access.csv  
**Description:** Defines access rights for the custom models and fields in the creativeflow_user_extensions module.  
**Template:** Odoo Security (CSV)  
**Dependency Level:** 1  
**Name:** ir.model.access  
**Type:** Odoo Access Control List  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Data Access Control
    
**Requirement Ids:**
    
    - Section 5.2.2 (User Management Odoo Mod.)
    
**Purpose:** To specify which user groups have read, write, create, and delete permissions for any new models or fields introduced by this module.  
**Logic Description:** CSV file with columns: id, name, model_id/id, group_id/id, perm_read, perm_write, perm_create, perm_unlink. Entries will grant appropriate groups (e.g., base.group_user, base.group_system) access to the custom fields added to res.users.  
**Documentation:**
    
    - **Summary:** Manages access permissions for creativeflow_user_extensions module entities.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/__init__.py  
**Description:** Initializes the Python submodules for the creativeflow_credits Odoo module.  
**Template:** Odoo Module Init (Python)  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To make Python models and other Python code within this module discoverable by Odoo.  
**Logic Description:** Imports the 'models' subdirectory.  
**Documentation:**
    
    - **Summary:** Standard Odoo Python module initializer for credit management.
    
**Namespace:** odoo.addons.creativeflow_credits  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/__manifest__.py  
**Description:** Manifest file for the creativeflow_credits Odoo module. Defines module metadata, dependencies (e.g., 'creativeflow_user_extensions', 'mail'), and data files.  
**Template:** Odoo Manifest (Python Dict)  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Credit System Core
    
**Requirement Ids:**
    
    - REQ-016
    - Section 5.2.2 (Business Logic component, Custom Odoo Modules)
    
**Purpose:** To declare the CreativeFlow Credit System module to Odoo, specifying its properties, dependencies, and data files for managing user credits.  
**Logic Description:** Dictionary containing 'name', 'version', 'summary', 'category', 'author', 'website', 'depends': ['base', 'mail', 'creativeflow_user_extensions'], 'data': ['security/ir.model.access.csv', 'views/credit_transaction_views.xml', 'views/credit_action_cost_views.xml', 'views/credit_menus.xml', 'data/credit_action_cost_data.xml'], 'installable', 'application'.  
**Documentation:**
    
    - **Summary:** Defines the 'CreativeFlow Credit System' module for Odoo.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/models/__init__.py  
**Description:** Initializes the Python models for the creativeflow_credits module.  
**Template:** Odoo Models Init (Python)  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Models Init  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To make individual model files like 'credit_transaction.py' and 'credit_action_cost.py' discoverable.  
**Logic Description:** Imports 'credit_transaction', 'credit_action_cost', and potentially 'res_users_credit_mixin'.  
**Documentation:**
    
    - **Summary:** Standard Odoo models directory initializer for credit system.
    
**Namespace:** odoo.addons.creativeflow_credits.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/models/credit_transaction.py  
**Description:** Defines the 'creativeflow.credit.transaction' model for logging credit changes.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** credit_transaction  
**Type:** Odoo Model  
**Relative Path:** models/credit_transaction.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', string='User', required=True, ondelete='cascade'  
    - **Name:** amount  
**Type:** fields.Float  
**Attributes:** string='Amount', required=True, digits='Credit Amount'  
    - **Name:** type  
**Type:** fields.Selection  
**Attributes:** string='Type', selection=[('debit','Debit'),('credit','Credit')], required=True  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** string='Description'  
    - **Name:** reference_document  
**Type:** fields.Reference  
**Attributes:** selection=[('creativeflow.generation.request.external','Generation Request ID (External)'),('creativeflow.api.call.external','API Call ID (External)'), ('sale.order','Sale Order')], string='Reference'  
    - **Name:** transaction_date  
**Type:** fields.Datetime  
**Attributes:** string='Date', default=fields.Datetime.now, required=True  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit Transaction Logging
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To maintain an auditable log of all credit additions and deductions for users.  
**Logic Description:** Model 'creativeflow.credit.transaction' inherits from 'mail.thread'. Fields include: user_id (Many2one res.users), amount (Float, positive for credit, negative for debit), type (Selection 'credit'/'debit'), description (Text), reference_document (Reference for linking to source of transaction e.g. generation ID from external system, API call ID, or SO for purchase), transaction_date (Datetime). Consider custom decimal precision for credits.  
**Documentation:**
    
    - **Summary:** Stores individual credit transactions for users.
    
**Namespace:** odoo.addons.creativeflow_credits.models.credit_transaction  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/models/credit_action_cost.py  
**Description:** Defines the 'creativeflow.credit.action.cost' model for configuring credit costs of different platform actions.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** credit_action_cost  
**Type:** Odoo Model  
**Relative Path:** models/credit_action_cost.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** string='Action Name', required=True, help='Unique identifier for the billable action, e.g., sample_generation, final_generation_hd'  
    - **Name:** cost  
**Type:** fields.Float  
**Attributes:** string='Credit Cost', required=True, digits='Credit Amount', help='Number of credits this action costs.'  
    - **Name:** description  
**Type:** fields.Text  
**Attributes:** string='Description'  
    - **Name:** is_active  
**Type:** fields.Boolean  
**Attributes:** string='Active', default=True  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Configurable Credit Costs
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To allow administrators to define and manage the credit cost associated with various billable actions within the CreativeFlow platform.  
**Logic Description:** Model 'creativeflow.credit.action.cost'. Fields: name (Char, unique action identifier like 'sample_generation'), cost (Float), description (Text), is_active (Boolean).  
**Documentation:**
    
    - **Summary:** Manages the credit costs for different platform features/actions.
    
**Namespace:** odoo.addons.creativeflow_credits.models.credit_action_cost  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/models/res_users_credit_mixin.py  
**Description:** A mixin or extension for 'res.users' to handle credit deduction and addition logic.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** res_users_credit_mixin  
**Type:** Odoo Model Extension/Mixin  
**Relative Path:** models/res_users_credit_mixin.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    - DomainService
    
**Members:**
    
    
**Methods:**
    
    - **Name:** action_debit_credits  
**Parameters:**
    
    - self
    - action_name
    - reference_details=None
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** action_credit_credits  
**Parameters:**
    
    - self
    - amount
    - description
    - reference_details=None
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** _get_action_cost  
**Parameters:**
    
    - self
    - action_name
    
**Return Type:** float  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Credit Deduction Logic
    - Credit Addition Logic
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To centralize the business logic for modifying a user's credit balance and logging the transaction. This will be called by other services or Odoo actions.  
**Logic Description:** Extends 'res.users' (from 'creativeflow_user_extensions'). Method 'action_debit_credits(self, action_name, reference_details=None)': Fetches cost from 'creativeflow.credit.action.cost' for 'action_name'. If user has sufficient 'credit_balance', deducts cost, creates a 'credit.transaction' record with type 'debit', and returns True. Else, raises UserError or returns False. Method 'action_credit_credits(self, amount, description, reference_details=None)': Adds 'amount' to 'credit_balance', creates a 'credit.transaction' record with type 'credit'. Ensure atomicity if possible.  
**Documentation:**
    
    - **Summary:** Adds methods to res.users for managing credit balances and transactions.
    
**Namespace:** odoo.addons.creativeflow_credits.models.res_users_credit_mixin  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/views/credit_transaction_views.xml  
**Description:** XML views for 'creativeflow.credit.transaction' (tree, form).  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** credit_transaction_views  
**Type:** Odoo View Definition  
**Relative Path:** views/credit_transaction_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit Transaction UI
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To allow administrators to view and manage credit transaction logs.  
**Logic Description:** Defines tree and form views for 'creativeflow.credit.transaction' model, showing fields like user_id, amount, type, description, reference_document, transaction_date. Form view might be read-only.  
**Documentation:**
    
    - **Summary:** Provides UI for viewing credit transactions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/views/credit_action_cost_views.xml  
**Description:** XML views for 'creativeflow.credit.action.cost' (tree, form).  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** credit_action_cost_views  
**Type:** Odoo View Definition  
**Relative Path:** views/credit_action_cost_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit Action Cost UI
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To allow administrators to configure the credit costs for different platform actions.  
**Logic Description:** Defines tree and form views for 'creativeflow.credit.action.cost' model, showing fields: name, cost, description, is_active.  
**Documentation:**
    
    - **Summary:** Provides UI for managing credit costs of actions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/views/credit_menus.xml  
**Description:** XML definition for menu items related to the credit system.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** credit_menus  
**Type:** Odoo Menu Definition  
**Relative Path:** views/credit_menus.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Navigation for Credits
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To provide navigation paths in the Odoo backend for accessing credit system configurations and logs.  
**Logic Description:** Defines <menuitem> elements for accessing 'creativeflow.credit.transaction' and 'creativeflow.credit.action.cost' views, likely under a main 'CreativeFlow Credits' menu.  
**Documentation:**
    
    - **Summary:** Creates menu entries for credit system management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/data/credit_action_cost_data.xml  
**Description:** XML file to load initial/default data for credit action costs.  
**Template:** Odoo Data (XML)  
**Dependency Level:** 2  
**Name:** credit_action_cost_data  
**Type:** Odoo Data Definition  
**Relative Path:** data/credit_action_cost_data.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Default Credit Costs
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To populate the 'creativeflow.credit.action.cost' table with predefined costs for standard actions upon module installation.  
**Logic Description:** Contains <record> elements for 'creativeflow.credit.action.cost' model. Example records: ('sample_generation', 0.25), ('final_generation_standard', 1.0), ('export_hd', 2.0).  
**Documentation:**
    
    - **Summary:** Initializes default credit costs for platform actions.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_credits/security/ir.model.access.csv  
**Description:** Defines access rights for credit system models.  
**Template:** Odoo Security (CSV)  
**Dependency Level:** 1  
**Name:** ir.model.access_credits  
**Type:** Odoo Access Control List  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit System Data Access Control
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To secure access to credit transaction logs and action cost configurations.  
**Logic Description:** CSV entries for 'creativeflow.credit.transaction' (e.g., admin read/write, user read-own if portal access) and 'creativeflow.credit.action.cost' (admin read/write).  
**Documentation:**
    
    - **Summary:** Manages access permissions for credit system entities.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_billing_subscription_extensions/__init__.py  
**Description:** Initializes Python submodules for creativeflow_billing_subscription_extensions.  
**Template:** Odoo Module Init (Python)  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - Section 3.4
    
**Purpose:** To make Python models within this module discoverable by Odoo.  
**Logic Description:** Imports the 'models' subdirectory.  
**Documentation:**
    
    - **Summary:** Initializer for billing and subscription extension module.
    
**Namespace:** odoo.addons.creativeflow_billing_subscription_extensions  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_billing_subscription_extensions/__manifest__.py  
**Description:** Manifest for creativeflow_billing_subscription_extensions module.  
**Template:** Odoo Manifest (Python Dict)  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Subscription Logic Extension
    
**Requirement Ids:**
    
    - Section 3.4
    - Section 5.2.2 (Billing & Subscription Odoo Mod.)
    
**Purpose:** To declare the module for extending Odoo's subscription functionalities for CreativeFlow.  
**Logic Description:** Dictionary with 'name', 'version', 'summary', 'depends': ['sale_subscription', 'creativeflow_user_extensions'], 'data': ['views/sale_subscription_views.xml', 'security/ir.model.access.csv'], 'installable', 'application': False.  
**Documentation:**
    
    - **Summary:** Defines extensions to Odoo's billing and subscription management for CreativeFlow.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_billing_subscription_extensions/models/__init__.py  
**Description:** Initializes models for creativeflow_billing_subscription_extensions.  
**Template:** Odoo Models Init (Python)  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Models Init  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    - Section 3.4
    
**Purpose:** To load model extensions for subscriptions.  
**Logic Description:** Imports 'sale_subscription.py'.  
**Documentation:**
    
    - **Summary:** Models initializer for subscription extensions.
    
**Namespace:** odoo.addons.creativeflow_billing_subscription_extensions.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_billing_subscription_extensions/models/sale_subscription.py  
**Description:** Extends the 'sale.subscription' model for CreativeFlow specific subscription logic.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** sale_subscription  
**Type:** Odoo Model Extension  
**Relative Path:** models/sale_subscription.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** cf_linked_user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', string='CreativeFlow User', help='Link to the CreativeFlow user if different from partner.'  
    - **Name:** cf_initial_credits_granted  
**Type:** fields.Float  
**Attributes:** string='Initial Credits Granted', help='Credits granted upon start of this subscription period.'  
    - **Name:** cf_payment_provider_subscription_id  
**Type:** fields.Char  
**Attributes:** string='Payment Provider Subscription ID', help='Subscription ID from Stripe/PayPal.'  
    
**Methods:**
    
    - **Name:** _prepare_creativeflow_invoice_values  
**Parameters:**
    
    - self
    - invoice_values
    
**Return Type:** dict  
**Attributes:** protected  
    - **Name:** _grant_initial_credits  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** protected  
    
**Implemented Features:**
    
    - Custom Subscription Fields
    - Subscription Event Hooks
    
**Requirement Ids:**
    
    - Section 3.4
    - REQ-016
    
**Purpose:** To add fields and logic specific to CreativeFlow subscriptions, such as linking to platform users or managing initial credit grants.  
**Logic Description:** Inherits 'sale.subscription'. Adds fields like 'cf_linked_user_id' (Many2one res.users), 'cf_initial_credits_granted' (Float). May override methods like '_recurring_create_invoice' or '_prepare_invoice_values' to interact with the credit system (call 'action_credit_credits' on user) or add CF-specific invoice lines. Add logic to update 'cf_subscription_tier' on linked 'res.users' upon subscription state changes.  
**Documentation:**
    
    - **Summary:** Customizes Odoo subscriptions for CreativeFlow needs.
    
**Namespace:** odoo.addons.creativeflow_billing_subscription_extensions.models.sale_subscription  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_billing_subscription_extensions/views/sale_subscription_views.xml  
**Description:** XML views to display CreativeFlow-specific fields on 'sale.subscription' forms.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** sale_subscription_views  
**Type:** Odoo View Definition  
**Relative Path:** views/sale_subscription_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Subscription UI Extension
    
**Requirement Ids:**
    
    - Section 3.4
    
**Purpose:** To make custom CreativeFlow subscription fields visible in the Odoo UI.  
**Logic Description:** Defines <record> for ir.ui.view. Inherits 'sale_subscription.sale_subscription_view_form' to add new fields ('cf_linked_user_id', 'cf_initial_credits_granted', 'cf_payment_provider_subscription_id').  
**Documentation:**
    
    - **Summary:** Customizes Odoo subscription views.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_billing_subscription_extensions/security/ir.model.access.csv  
**Description:** Access rights for creativeflow_billing_subscription_extensions module fields.  
**Template:** Odoo Security (CSV)  
**Dependency Level:** 1  
**Name:** ir.model.access_subscription_ext  
**Type:** Odoo Access Control List  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Subscription Extension Data Access
    
**Requirement Ids:**
    
    - Section 3.4
    
**Purpose:** To control access to custom fields added to subscriptions.  
**Logic Description:** Grants appropriate groups access to new fields on sale.subscription.  
**Documentation:**
    
    - **Summary:** Access control for subscription extension fields.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/__init__.py  
**Description:** Initializes Python submodules for creativeflow_brand_workbench_management.  
**Template:** Odoo Module Init (Python)  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To load Python models for brand kits and workbenches.  
**Logic Description:** Imports 'models'.  
**Documentation:**
    
    - **Summary:** Initializer for brand kit and workbench management module.
    
**Namespace:** odoo.addons.creativeflow_brand_workbench_management  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/__manifest__.py  
**Description:** Manifest for creativeflow_brand_workbench_management.  
**Template:** Odoo Manifest (Python Dict)  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Brand Kit Management
    - Workbench Management
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To declare the module for managing CreativeFlow brand kits and workbenches within Odoo.  
**Logic Description:** Dictionary with 'name', 'version', 'summary', 'depends': ['base', 'mail', 'attachment_indexation' (for logo search)], 'data': ['security/ir.model.access.csv', 'views/brand_kit_views.xml', 'views/workbench_views.xml', 'views/brand_workbench_menus.xml'], 'installable', 'application': False.  
**Documentation:**
    
    - **Summary:** Module for managing brand kits and workbenches in Odoo for CreativeFlow.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/models/__init__.py  
**Description:** Initializes models for brand kits and workbenches.  
**Template:** Odoo Models Init (Python)  
**Dependency Level:** 1  
**Name:** __init__  
**Type:** Python Models Init  
**Relative Path:** models/__init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Model Discovery
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To load 'brand_kit.py' and 'workbench.py' models.  
**Logic Description:** Imports 'brand_kit', 'workbench'.  
**Documentation:**
    
    - **Summary:** Models initializer for brand and workbench management.
    
**Namespace:** odoo.addons.creativeflow_brand_workbench_management.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/models/brand_kit.py  
**Description:** Defines the 'creativeflow.brand.kit' model.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** brand_kit  
**Type:** Odoo Model  
**Relative Path:** models/brand_kit.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** string='Name', required=True  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', string='Owner', required=True  
    - **Name:** cf_team_id_external  
**Type:** fields.Char  
**Attributes:** string='CreativeFlow Team ID', help='External ID of the team owning this brand kit.'  
    - **Name:** colors_json  
**Type:** fields.Text  
**Attributes:** string='Colors (JSON)', help='JSON string representing color palettes.'  
    - **Name:** fonts_json  
**Type:** fields.Text  
**Attributes:** string='Fonts (JSON)', help='JSON string representing font definitions.'  
    - **Name:** logo_ids  
**Type:** fields.Many2many  
**Attributes:** comodel_name='ir.attachment', string='Logos', relation='creativeflow_brand_kit_logo_rel', column1='brand_kit_id', column2='attachment_id'  
    - **Name:** style_preferences_json  
**Type:** fields.Text  
**Attributes:** string='Style Preferences (JSON)'  
    - **Name:** is_default_for_user  
**Type:** fields.Boolean  
**Attributes:** string='Default for User'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Brand Kit Data Storage
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To store and manage brand kit assets and preferences within Odoo for CreativeFlow users.  
**Logic Description:** Model 'creativeflow.brand.kit' inherits 'mail.thread'. Fields: name, user_id (owner), cf_team_id_external (if teams are managed outside Odoo), colors_json (Text), fonts_json (Text), logo_ids (Many2many ir.attachment), style_preferences_json (Text), is_default_for_user (Boolean).  
**Documentation:**
    
    - **Summary:** Stores brand kit information like colors, fonts, logos.
    
**Namespace:** odoo.addons.creativeflow_brand_workbench_management.models.brand_kit  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/models/workbench.py  
**Description:** Defines the 'creativeflow.workbench' model.  
**Template:** Odoo Model (Python)  
**Dependency Level:** 2  
**Name:** workbench  
**Type:** Odoo Model  
**Relative Path:** models/workbench.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** string='Name', required=True  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', string='Owner', required=True  
    - **Name:** default_brand_kit_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.brand.kit', string='Default Brand Kit'  
    - **Name:** cf_project_ids_external  
**Type:** fields.Text  
**Attributes:** string='CreativeFlow Project IDs (JSON)', help='JSON list of external project IDs belonging to this workbench.'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Workbench Data Storage
    - Workbench Organization Rules (via constraints/logic)
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To allow users to organize their CreativeFlow projects into workbenches within Odoo.  
**Logic Description:** Model 'creativeflow.workbench' inherits 'mail.thread'. Fields: name, user_id (owner), default_brand_kit_id (Many2one creativeflow.brand.kit), cf_project_ids_external (Text, storing JSON array of external project identifiers). Actual projects might be managed in the main CF platform and only referenced here.  
**Documentation:**
    
    - **Summary:** Stores workbench information, acting as a container for projects.
    
**Namespace:** odoo.addons.creativeflow_brand_workbench_management.models.workbench  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/views/brand_kit_views.xml  
**Description:** XML views for 'creativeflow.brand.kit'.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** brand_kit_views  
**Type:** Odoo View Definition  
**Relative Path:** views/brand_kit_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Brand Kit UI
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To provide an interface for managing brand kits in Odoo.  
**Logic Description:** Defines tree and form views for 'creativeflow.brand.kit', showing name, owner, logos, and other relevant fields. JSON fields might be displayed as simple text areas or with custom widgets if complex editing is needed in Odoo.  
**Documentation:**
    
    - **Summary:** UI for brand kit management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/views/workbench_views.xml  
**Description:** XML views for 'creativeflow.workbench'.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** workbench_views  
**Type:** Odoo View Definition  
**Relative Path:** views/workbench_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Workbench UI
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To provide an interface for managing workbenches in Odoo.  
**Logic Description:** Defines tree and form views for 'creativeflow.workbench', showing name, owner, default brand kit, and potentially a display for linked external project IDs.  
**Documentation:**
    
    - **Summary:** UI for workbench management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/views/brand_workbench_menus.xml  
**Description:** Menu items for Brand Kit and Workbench management.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** brand_workbench_menus  
**Type:** Odoo Menu Definition  
**Relative Path:** views/brand_workbench_menus.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Admin Navigation for Brand/Workbench
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To create Odoo backend menu entries for Brand Kits and Workbenches.  
**Logic Description:** Defines <menuitem> elements under a 'CreativeFlow Content' or similar top-level menu.  
**Documentation:**
    
    - **Summary:** Menu entries for brand and workbench management.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_brand_workbench_management/security/ir.model.access.csv  
**Description:** Access rights for brand kit and workbench models.  
**Template:** Odoo Security (CSV)  
**Dependency Level:** 1  
**Name:** ir.model.access_brand_workbench  
**Type:** Odoo Access Control List  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Brand/Workbench Data Access Control
    
**Requirement Ids:**
    
    - Section 5.2.2 (Content Management Odoo Mod.)
    
**Purpose:** To secure access to brand kit and workbench data.  
**Logic Description:** CSV entries for 'creativeflow.brand.kit' and 'creativeflow.workbench', granting appropriate permissions to user groups (e.g., users can manage their own, admins can manage all).  
**Documentation:**
    
    - **Summary:** Manages access permissions for brand kit and workbench entities.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_support_ux_customizations/__init__.py  
**Description:** Initializes Python submodules for creativeflow_support_ux_customizations.  
**Template:** Odoo Module Init (Python)  
**Dependency Level:** 0  
**Name:** __init__  
**Type:** Python Module Init  
**Relative Path:** __init__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Initialization
    
**Requirement Ids:**
    
    - REQ-021
    - Section 3.7
    
**Purpose:** To load Python models (if any extensions are needed) for support UX.  
**Logic Description:** May import 'models' if model extensions are required, otherwise might be empty if only views/static assets are changed.  
**Documentation:**
    
    - **Summary:** Initializer for support UX customization module.
    
**Namespace:** odoo.addons.creativeflow_support_ux_customizations  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_support_ux_customizations/__manifest__.py  
**Description:** Manifest for creativeflow_support_ux_customizations module.  
**Template:** Odoo Manifest (Python Dict)  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Helpdesk UX Customization
    - Knowledge Base UX Customization
    
**Requirement Ids:**
    
    - REQ-021
    - Section 3.7
    - Section 5.2.2 (Business Logic component, Custom Odoo Modules)
    
**Purpose:** To declare the module for customizing Odoo Helpdesk and Knowledge views for CreativeFlow branding and workflows.  
**Logic Description:** Dictionary with 'name', 'version', 'summary', 'depends': ['helpdesk', 'knowledge', 'website' (if portal views are customized)], 'data': ['views/helpdesk_ticket_views.xml', 'views/knowledge_article_views.xml'], 'assets': {'web.assets_frontend': ['creativeflow_support_ux_customizations/static/src/css/creativeflow_branding.css']}, 'installable', 'application': False.  
**Documentation:**
    
    - **Summary:** Module for customizing Odoo Helpdesk and Knowledge UX.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_support_ux_customizations/views/helpdesk_ticket_views.xml  
**Description:** XML views to customize 'helpdesk.ticket' appearance and potentially workflows.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** helpdesk_ticket_views  
**Type:** Odoo View Definition  
**Relative Path:** views/helpdesk_ticket_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Helpdesk View Customization
    
**Requirement Ids:**
    
    - REQ-021
    - Section 3.7
    
**Purpose:** To align Odoo Helpdesk views with CreativeFlow branding and potentially simplify or enhance workflows.  
**Logic Description:** Inherits existing 'helpdesk.ticket_view_form', 'helpdesk.ticket_view_tree', and portal/website views for tickets. Modifies layouts, adds/removes fields, or applies custom CSS classes for branding. May include QWeb templates for portal customizations.  
**Documentation:**
    
    - **Summary:** Customizes Odoo Helpdesk ticket views.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_support_ux_customizations/views/knowledge_article_views.xml  
**Description:** XML views to customize 'knowledge.article' appearance for the portal.  
**Template:** Odoo View (XML)  
**Dependency Level:** 3  
**Name:** knowledge_article_views  
**Type:** Odoo View Definition  
**Relative Path:** views/knowledge_article_views.xml  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Knowledge Base View Customization
    
**Requirement Ids:**
    
    - REQ-021
    - Section 3.7
    
**Purpose:** To align Odoo Knowledge Base article views with CreativeFlow branding.  
**Logic Description:** Inherits existing website/portal views for 'knowledge.article' and 'knowledge.category'. Modifies layouts and applies custom CSS classes for branding.  
**Documentation:**
    
    - **Summary:** Customizes Odoo Knowledge Base article views.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** erp/odoo-creativeflow-custom/creativeflow_support_ux_customizations/static/src/css/creativeflow_branding.css  
**Description:** CSS file for CreativeFlow branding customizations on Helpdesk and Knowledge portal pages.  
**Template:** CSS  
**Dependency Level:** 2  
**Name:** creativeflow_branding  
**Type:** Static Asset (CSS)  
**Relative Path:** static/src/css/creativeflow_branding.css  
**Repository Id:** REPO-ODOO-CUSTOMIZATIONS-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Support Portal Branding
    
**Requirement Ids:**
    
    - REQ-021
    
**Purpose:** To apply CreativeFlow specific styles (colors, fonts, layout tweaks) to the Odoo Helpdesk and Knowledge portal interfaces.  
**Logic Description:** Contains CSS rules targeting Odoo Helpdesk and Knowledge portal elements to align them with CreativeFlow's visual identity. This might include overriding default Odoo styles for headers, footers, buttons, typography, etc.  
**Documentation:**
    
    - **Summary:** Custom CSS for branding Odoo support portal elements.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_advanced_credit_rules
  - use_custom_subscription_workflows
  - brand_kit_team_sharing_enabled
  
- **Database Configs:**
  
  - odoo_db_host
  - odoo_db_port
  - odoo_db_user
  - odoo_db_password
  - odoo_db_name
  


---

