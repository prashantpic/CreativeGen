# This file serves to aggregate all model definitions from this directory
# into a single namespace. This is crucial for Alembic to discover all
# tables when autogenerating migrations. By importing them here, `env.py`
# can simply import `Base` from `app.models` and `Base.metadata` will
# contain the complete schema.

from ..db.base import Base

from .user_model import User
from .team_model import Team
from .team_member_model import TeamMember
from .brand_kit_model import BrandKit
from .workbench_model import Workbench
from .template_model import Template
from .project_model import Project
from .generation_request_model import GenerationRequest
from .asset_model import Asset
from .asset_version_model import AssetVersion
from .social_media_connection_model import SocialMediaConnection
from .api_client_model import APIClient
from .subscription_model import Subscription
from .credit_transaction_model import CreditTransaction
from .usage_log_model import UsageLog
from .session_model import Session
from .notification_model import Notification
from .ai_model_model import AIModel
from .ai_model_version_model import AIModelVersion
from .ai_model_validation_result_model import AIModelValidationResult
from .ai_model_deployment_model import AIModelDeployment
from .ai_model_feedback_model import AIModelFeedback