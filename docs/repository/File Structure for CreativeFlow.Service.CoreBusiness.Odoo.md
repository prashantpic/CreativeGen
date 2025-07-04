# Specification

# 1. Files

- **Path:** creativeflow_base/__manifest__.py  
**Description:** The manifest file for the CreativeFlow Base module. It defines the module's metadata, dependencies on core Odoo modules, and lists the data files (views, security) to be loaded. This module provides the foundation for all other custom CreativeFlow modules.  
**Template:** Odoo Manifest  
**Dependency Level:** 0  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Base Module Setup
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo Backend)
    
**Purpose:** Declares the base module, its dependencies (like web, auth_signup), and the order of its view and security file loading.  
**Logic Description:** This is a dictionary-based configuration file. It will contain keys for 'name', 'version', 'summary', 'author', 'website', 'category', 'depends', and 'data'. The 'depends' key will list ['base', 'web', 'auth_signup']. The 'data' key will list the paths to security and view XML files.  
**Documentation:**
    
    - **Summary:** Defines the core module properties and dependencies for the CreativeFlow Odoo application. It serves as the entry point for Odoo to recognize and load the base functionalities.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_base/models/res_users.py  
**Description:** Extends the core Odoo 'res.users' model to add fields specific to the CreativeFlow platform, such as subscription tier and credit balance. These fields provide a quick-lookup cache of data primarily managed by the billing system.  
**Template:** Odoo Model  
**Dependency Level:** 1  
**Name:** res_users  
**Type:** Model  
**Relative Path:** models/res_users.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    - Model Extension
    
**Members:**
    
    - **Name:** subscription_tier  
**Type:** fields.Selection  
**Attributes:**   
    - **Name:** credit_balance  
**Type:** fields.Float  
**Attributes:**   
    - **Name:** x_studio_brand_kit_ids  
**Type:** fields.One2many  
**Attributes:** comodel_name='creativeflow.brand_kit'  
    - **Name:** x_studio_workbench_ids  
**Type:** fields.One2many  
**Attributes:** comodel_name='creativeflow.workbench'  
    
**Methods:**
    
    - **Name:** deduct_credits  
**Parameters:**
    
    - self
    - amount
    - description
    
**Return Type:** bool  
**Attributes:** public  
    - **Name:** add_credits  
**Parameters:**
    
    - self
    - amount
    - description
    
**Return Type:** bool  
**Attributes:** public  
    
**Implemented Features:**
    
    - User Profile Extension
    - Credit Balance Management
    
**Requirement Ids:**
    
    - REQ-004
    - REQ-016
    - Section 3.1 (User Mgmt)
    - Section 3.4 (Subscription/Billing)
    
**Purpose:** To augment the standard Odoo user model with custom fields and methods required for the CreativeFlow platform's business logic.  
**Logic Description:** Inherits from 'res.users'. Adds a Selection field for 'subscription_tier' ('Free', 'Pro', 'Team', 'Enterprise'). Adds a Float field for 'credit_balance'. Defines the 'deduct_credits' method which checks for sufficient balance, subtracts the amount, and logs a transaction. Defines the 'add_credits' method which adds to the balance and logs the transaction. Logic will handle concurrency to prevent race conditions on credit balance.  
**Documentation:**
    
    - **Summary:** This file extends the 'res.users' model to include CreativeFlow-specific data like subscription level and credit balance. It also provides core methods for credit manipulation, which are central to the platform's freemium model.
    
**Namespace:** odoo.addons.creativeflow_base.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_base/security/ir.model.access.csv  
**Description:** Defines the default access control list (ACL) for the custom models introduced in the base module, ensuring proper permissions are set for different user groups.  
**Template:** Odoo Security  
**Dependency Level:** 1  
**Name:** ir.model.access  
**Type:** Configuration  
**Relative Path:** security/ir.model.access.csv  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Base Model Security
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo Backend)
    
**Purpose:** To provide foundational security settings for the custom Odoo models, specifying which user groups can perform read, write, create, and delete operations.  
**Logic Description:** A CSV file with columns: id, name, model_id:id, group_id:id, perm_read, perm_write, perm_create, perm_unlink. It will contain entries for any new models defined in this base module, granting appropriate permissions to user groups like 'base.group_user'.  
**Documentation:**
    
    - **Summary:** Configures the basic access rights for custom models, forming the lowest level of the security hierarchy for the CreativeFlow application.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_base/views/creativeflow_menus.xml  
**Description:** Defines the main application menu structure in the Odoo UI for the CreativeFlow AI platform, creating the primary navigation entry points for users.  
**Template:** Odoo View  
**Dependency Level:** 1  
**Name:** creativeflow_menus  
**Type:** View  
**Relative Path:** views/creativeflow_menus.xml  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Main Application Menu
    
**Requirement Ids:**
    
    - Section 2.1 (Odoo Backend)
    
**Purpose:** To create the top-level menu item for 'CreativeFlow AI' and its main sub-menus such as 'Dashboard', 'Projects', 'Brand Kits', etc.  
**Logic Description:** An XML file containing <record> tags for 'ir.ui.menu'. It will define a top-level menu (e.g., 'creativeflow_base.menu_root') and child menu items that link to specific Odoo actions defined in other modules.  
**Documentation:**
    
    - **Summary:** This XML file constructs the primary navigation structure for the CreativeFlow application within the Odoo backend UI.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_content_management/__manifest__.py  
**Description:** The manifest file for the Content Management module, defining its dependency on creativeflow_base and listing its own model, view, and security files.  
**Template:** Odoo Manifest  
**Dependency Level:** 1  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Content Management Module Setup
    
**Requirement Ids:**
    
    - REQ-004
    - REQ-010
    - REQ-011
    
**Purpose:** Declares the Content Management module and ensures it is loaded after the base module, making its features available to the system.  
**Logic Description:** A dictionary-based configuration file. The 'depends' key will list ['creativeflow_base']. The 'data' key will list the paths to its security CSV and all its view XML files.  
**Documentation:**
    
    - **Summary:** Defines the module that handles the core creative entities like Workbenches, Projects, and Brand Kits, specifying its dependencies and data files.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_content_management/models/creativeflow_workbench.py  
**Description:** Defines the Odoo model for a 'Workbench', which acts as a container for organizing multiple creative projects. It is linked to a user.  
**Template:** Odoo Model  
**Dependency Level:** 2  
**Name:** creativeflow_workbench  
**Type:** Model  
**Relative Path:** models/creativeflow_workbench.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required=True  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', required=True, ondelete='cascade'  
    - **Name:** project_ids  
**Type:** fields.One2many  
**Attributes:** comodel_name='creativeflow.project', inverse_name='workbench_id'  
    - **Name:** default_brand_kit_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.brand_kit'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Workbench Data Model
    
**Requirement Ids:**
    
    - REQ-010
    
**Purpose:** To create the database structure and business logic for the Workbench entity, representing a high-level container for creative work.  
**Logic Description:** Defines a new Odoo model named 'creativeflow.workbench'. It includes fields for its name, a many-to-one relationship with 'res.users' to establish ownership, and a one-to-many relationship with 'creativeflow.project' to contain projects.  
**Documentation:**
    
    - **Summary:** This file implements the data model for the Workbench concept, a primary organizational tool for users to group their creative projects.
    
**Namespace:** odoo.addons.creativeflow_content_management.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_content_management/models/creativeflow_project.py  
**Description:** Defines the Odoo model for a 'Project', which is the central hub for a specific creative campaign, containing assets and generation requests. It belongs to a Workbench.  
**Template:** Odoo Model  
**Dependency Level:** 3  
**Name:** creativeflow_project  
**Type:** Model  
**Relative Path:** models/creativeflow_project.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required=True  
    - **Name:** workbench_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.workbench', required=True, ondelete='cascade'  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', related='workbench_id.user_id', store=True  
    - **Name:** brand_kit_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.brand_kit'  
    - **Name:** asset_ids  
**Type:** fields.One2many  
**Attributes:** comodel_name='creativeflow.asset', inverse_name='project_id'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Data Model
    
**Requirement Ids:**
    
    - REQ-010
    
**Purpose:** To model a creative project, linking it to its parent workbench and associated assets and brand settings.  
**Logic Description:** Defines the 'creativeflow.project' model. It establishes a required many-to-one relationship with 'creativeflow.workbench'. It also includes fields for a project name, a link to an overriding brand kit, and relations to its contained assets. The user_id is denormalized from the workbench for easier querying.  
**Documentation:**
    
    - **Summary:** This file implements the data model for a Project, the core entity where users will manage their creative assets and generation workflows for a specific goal or campaign.
    
**Namespace:** odoo.addons.creativeflow_content_management.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_content_management/models/creativeflow_brand_kit.py  
**Description:** Defines the Odoo model for a 'Brand Kit', which stores brand-specific assets like colors, fonts, and logos for Pro+ users.  
**Template:** Odoo Model  
**Dependency Level:** 2  
**Name:** creativeflow_brand_kit  
**Type:** Model  
**Relative Path:** models/creativeflow_brand_kit.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** name  
**Type:** fields.Char  
**Attributes:** required=True  
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', required=True  
    - **Name:** colors  
**Type:** fields.Text  
**Attributes:** help='JSON string for color palette'  
    - **Name:** fonts  
**Type:** fields.Text  
**Attributes:** help='JSON string for font definitions'  
    - **Name:** logos  
**Type:** fields.Text  
**Attributes:** help='JSON string of logo asset MinIO paths'  
    - **Name:** is_default  
**Type:** fields.Boolean  
**Attributes:** default=False  
    
**Methods:**
    
    - **Name:** _set_default_brand_kit  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    
**Implemented Features:**
    
    - Brand Kit Data Model
    
**Requirement Ids:**
    
    - REQ-004
    
**Purpose:** To provide a persistent storage model for user-defined brand kits, enabling consistent branding across creative projects.  
**Logic Description:** Defines the 'creativeflow.brand_kit' model. Fields will store the brand kit's name, owner (user_id), and JSON data for colors, fonts, and logo paths. A boolean 'is_default' flag is included. A method will ensure only one brand kit per user can be the default at any time.  
**Documentation:**
    
    - **Summary:** This file implements the data model for Brand Kits, allowing users to store and reuse their brand's visual identity elements like colors, fonts, and logos.
    
**Namespace:** odoo.addons.creativeflow_content_management.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_content_management/views/project_views.xml  
**Description:** Defines the Odoo views (form, list/tree, kanban) for the Project model, enabling administrators and users to interact with projects through the Odoo UI.  
**Template:** Odoo View  
**Dependency Level:** 4  
**Name:** project_views  
**Type:** View  
**Relative Path:** views/project_views.xml  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project UI Views
    
**Requirement Ids:**
    
    - REQ-010
    
**Purpose:** To provide the user interface definitions for creating, viewing, and managing projects within Odoo.  
**Logic Description:** An XML file containing <record> tags for 'ir.ui.view'. It will define a form view for project details, a tree view for a list of projects, and a kanban view for a more visual project overview. Also defines the 'ir.actions.act_window' to link these views to a menu item.  
**Documentation:**
    
    - **Summary:** This XML file defines the various user interface views (form, list, etc.) for the Project model, controlling how project data is displayed and edited in the Odoo backend.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_billing_subscription/__manifest__.py  
**Description:** The manifest file for the Billing and Subscription module. It defines dependencies on the base module and Odoo's native 'sale_subscription' and 'account' modules.  
**Template:** Odoo Manifest  
**Dependency Level:** 1  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Billing Module Setup
    
**Requirement Ids:**
    
    - REQ-014
    - REQ-016
    - INT-003
    
**Purpose:** To declare the billing module, its dependencies on core business apps, and its data files, enabling subscription and credit management.  
**Logic Description:** A dictionary-based configuration file. The 'depends' key will list ['creativeflow_base', 'sale_subscription', 'account', 'payment']. The 'data' key will list security files, wizard views, and product data definitions.  
**Documentation:**
    
    - **Summary:** Defines the module responsible for all financial aspects of the platform, including subscriptions, payments, and the credit system. It links into Odoo's powerful accounting and subscription management applications.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_billing_subscription/models/creativeflow_credit_transaction.py  
**Description:** Defines the Odoo model to log every credit transaction, providing a detailed audit trail for credit purchases and consumption.  
**Template:** Odoo Model  
**Dependency Level:** 2  
**Name:** creativeflow_credit_transaction  
**Type:** Model  
**Relative Path:** models/creativeflow_credit_transaction.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** user_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='res.users', required=True  
    - **Name:** amount  
**Type:** fields.Float  
**Attributes:** required=True  
    - **Name:** description  
**Type:** fields.Char  
**Attributes:** required=True  
    - **Name:** generation_request_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.generation_request'  
    - **Name:** related_invoice_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='account.move'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Credit Transaction Logging
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To create an immutable log of all credit-related activities for auditing, reporting, and user visibility.  
**Logic Description:** Defines the 'creativeflow.credit_transaction' model. It includes fields for the user, the credit amount (positive for additions, negative for deductions), a description of the action, and links to related records like invoices or generation requests. This model is append-only.  
**Documentation:**
    
    - **Summary:** This file implements the data model for credit transactions, which serves as the ledger for all user credit activities, ensuring financial traceability.
    
**Namespace:** odoo.addons.creativeflow_billing_subscription.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_billing_subscription/controllers/payment_controllers.py  
**Description:** Defines Odoo controllers to handle incoming webhooks from payment gateways like Stripe and PayPal. These controllers process payment confirmation events.  
**Template:** Odoo Controller  
**Dependency Level:** 3  
**Name:** payment_controllers  
**Type:** Controller  
**Relative Path:** controllers/payment_controllers.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    - Webhook
    
**Members:**
    
    
**Methods:**
    
    - **Name:** stripe_webhook  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** @http.route('/payment/stripe/webhook', type='json', auth='public')  
    - **Name:** paypal_webhook  
**Parameters:**
    
    - self
    - **post
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** @http.route('/payment/paypal/webhook', type='json', auth='public')  
    
**Implemented Features:**
    
    - Stripe Webhook Handling
    - PayPal Webhook Handling
    
**Requirement Ids:**
    
    - REQ-014
    - INT-003
    
**Purpose:** To provide endpoints for payment gateways to send asynchronous notifications about payment status, enabling the system to react to events like successful payments or failures.  
**Logic Description:** This controller will have methods decorated with Odoo's `@http.route`. The 'stripe_webhook' method will receive JSON payloads from Stripe, verify the event signature, and then process events like 'checkout.session.completed' or 'invoice.paid' to confirm subscriptions or add credits to a user's account by calling the relevant model methods. Similar logic for PayPal.  
**Documentation:**
    
    - **Summary:** This file implements the webhook listeners for Stripe and PayPal. It is a critical integration point that allows the Odoo backend to be updated automatically based on real-world payment events.
    
**Namespace:** odoo.addons.creativeflow_billing_subscription.controllers  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_api/__manifest__.py  
**Description:** The manifest file for the custom API module. This module exposes RESTful endpoints for the frontend and other services to interact with the Odoo backend.  
**Template:** Odoo Manifest  
**Dependency Level:** 2  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom API Layer Setup
    
**Requirement Ids:**
    
    - Section 5.2.2 (Business Logic: Odoo)
    
**Purpose:** Declares the API module, ensuring it loads after all functional modules it depends on, to provide a clean, dedicated interface layer.  
**Logic Description:** A dictionary-based configuration file. The 'depends' key will list all other creativeflow modules, like ['creativeflow_content_management', 'creativeflow_billing_subscription']. This ensures the API controllers have access to all necessary models and logic.  
**Documentation:**
    
    - **Summary:** Defines the module that acts as the primary API gateway into the Odoo business logic, providing controlled access to platform functionalities for external consumers like the web frontend.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_api/controllers/generation_controller.py  
**Description:** Defines the REST API controller for handling AI creative generation requests. This is a critical endpoint that kicks off the asynchronous generation workflow.  
**Template:** Odoo Controller  
**Dependency Level:** 3  
**Name:** generation_controller  
**Type:** Controller  
**Relative Path:** controllers/generation_controller.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    - API Controller
    - Event Publisher
    
**Members:**
    
    
**Methods:**
    
    - **Name:** initiate_generation  
**Parameters:**
    
    - self
    - **kwargs
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** @http.route('/api/v1/generation/create', type='json', auth='user', methods=['POST'], csrf=False)  
    - **Name:** get_generation_status  
**Parameters:**
    
    - self
    - generation_id
    
**Return Type:** werkzeug.wrappers.Response  
**Attributes:** @http.route('/api/v1/generation/<uuid:generation_id>/status', type='http', auth='user', methods=['GET'])  
    
**Implemented Features:**
    
    - AI Generation Request API
    - Job Publishing to RabbitMQ
    
**Requirement Ids:**
    
    - REQ-016
    
**Purpose:** To receive generation requests from clients, validate them, deduct credits, create a tracking record, and publish a job message to RabbitMQ for processing by n8n.  
**Logic Description:** The 'initiate_generation' method will: 1. Authenticate the user. 2. Validate input parameters (prompt, format, etc.). 3. Check and deduct credits from the user's account using the 'res.users' model method. 4. Create a 'creativeflow.generation_request' record with status 'Pending'. 5. Call the RabbitMQ publisher service to send a message with the request details. 6. Return the `generation_request` ID to the client. The 'get_generation_status' endpoint will query the database for the status of a given request.  
**Documentation:**
    
    - **Summary:** This controller is the entry point for all AI generation tasks. It handles request validation, billing, and dispatches the task to the asynchronous workflow engine via a message queue.
    
**Namespace:** odoo.addons.creativeflow_api.controllers  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_integration_rabbitmq/services/rabbitmq_publisher.py  
**Description:** A service class responsible for establishing a connection to RabbitMQ and publishing messages to the appropriate exchanges and queues.  
**Template:** Python Service  
**Dependency Level:** 1  
**Name:** rabbitmq_publisher  
**Type:** Service  
**Relative Path:** services/rabbitmq_publisher.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    - Messaging Gateway
    
**Members:**
    
    - **Name:** connection  
**Type:** pika.BlockingConnection  
**Attributes:** private  
    - **Name:** channel  
**Type:** pika.channel.Channel  
**Attributes:** private  
    
**Methods:**
    
    - **Name:** __init__  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** _connect  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** private  
    - **Name:** publish_generation_job  
**Parameters:**
    
    - self
    - job_payload
    
**Return Type:** void  
**Attributes:** public  
    - **Name:** close_connection  
**Parameters:**
    
    - self
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - RabbitMQ Publishing Logic
    
**Requirement Ids:**
    
    - Section 5.2.2 (Business Logic: Odoo)
    
**Purpose:** To abstract the complexities of interacting with RabbitMQ, providing a simple, reusable service for other parts of the Odoo application to send messages.  
**Logic Description:** The class will use the 'pika' library. The constructor will initialize connection parameters from Odoo system parameters/config. The '_connect' method will establish the connection and channel. The 'publish_generation_job' method will serialize the job payload to JSON, declare the necessary exchange and queue (e.g., 'ai_jobs_exchange'), and publish the message using 'basic_publish' with delivery mode set to persistent.  
**Documentation:**
    
    - **Summary:** This service acts as a gateway to the RabbitMQ message broker, encapsulating connection management and message publishing logic to decouple the core business application from the messaging infrastructure.
    
**Namespace:** odoo.addons.creativeflow_integration_rabbitmq.services  
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_helpdesk/__manifest__.py  
**Description:** Manifest for the Helpdesk module, which customizes Odoo's native Helpdesk application for the CreativeFlow AI platform.  
**Template:** Odoo Manifest  
**Dependency Level:** 1  
**Name:** __manifest__  
**Type:** Configuration  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Helpdesk Module Setup
    
**Requirement Ids:**
    
    - Section 3.7 (Support System)
    - REQ-021
    
**Purpose:** To declare the helpdesk customization module and its dependency on the Odoo 'helpdesk' app.  
**Logic Description:** A dictionary-based configuration file. The 'depends' key will list ['creativeflow_base', 'helpdesk']. The 'data' key will list paths to any custom view files for the helpdesk portal.  
**Documentation:**
    
    - **Summary:** Defines the module that tailors the standard Odoo Helpdesk functionality to fit the specific needs of CreativeFlow AI users and support agents.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BusinessLogic
    
- **Path:** creativeflow_helpdesk/models/helpdesk_ticket.py  
**Description:** Extends the Odoo 'helpdesk.ticket' model to add relationships or fields that link support tickets directly to CreativeFlow-specific entities like projects or generation requests.  
**Template:** Odoo Model  
**Dependency Level:** 2  
**Name:** helpdesk_ticket  
**Type:** Model  
**Relative Path:** models/helpdesk_ticket.py  
**Repository Id:** REPO-SERVICE-COREBUSINESS-ODOO-001  
**Pattern Ids:**
    
    - Model Extension
    
**Members:**
    
    - **Name:** project_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.project'  
    - **Name:** generation_request_id  
**Type:** fields.Many2one  
**Attributes:** comodel_name='creativeflow.generation_request'  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Contextual Helpdesk Tickets
    
**Requirement Ids:**
    
    - REQ-021
    
**Purpose:** To provide richer context for support agents by linking tickets to the specific part of the application the user is having trouble with.  
**Logic Description:** Inherits from 'helpdesk.ticket'. Adds a Many2one field to 'creativeflow.project' and another to 'creativeflow.generation_request'. These fields will be optional and can be populated when a ticket is created from a specific context in the frontend application.  
**Documentation:**
    
    - **Summary:** This file extends the standard helpdesk ticket model, enriching it with links to core CreativeFlow entities. This allows support staff to have immediate context when handling user issues, leading to faster resolution.
    
**Namespace:** odoo.addons.creativeflow_helpdesk.models  
**Metadata:**
    
    - **Category:** BusinessLogic
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_paypal_payments
  - enable_live_chat_support
  - enable_user_template_saving
  - enable_progressive_profiling
  
- **Database Configs:**
  
  - ODOO_DB_HOST
  - ODOO_DB_PORT
  - ODOO_DB_USER
  - ODOO_DB_PASSWORD
  - ODOO_DB_NAME
  


---

