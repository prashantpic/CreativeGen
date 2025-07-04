from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, condecimal

class CreditBalanceDomain(BaseModel):
    """Internal domain model for a user's credit balance."""
    user_id: UUID = Field(..., description="The user's platform ID.")
    balance: condecimal(ge=0) = Field(..., description="The current credit balance.")
    last_updated_at: datetime = Field(..., description="Timestamp of the last balance update.")

class CreditDeductionRequestDomain(BaseModel):
    """
    Internal domain model representing a request to deduct credits for a specific action.
    """
    user_id: UUID = Field(..., description="The user's platform ID.")
    amount: condecimal(gt=0) = Field(..., description="The number of credits to deduct.")
    action_type: str = Field(..., description="The type of action consuming credits (e.g., 'sample_generation').")
    reference_id: Optional[str] = Field(None, description="An optional reference to the consuming entity (e.g., generation_request_id).")
    description: Optional[str] = Field(None, description="A human-readable description of the transaction.")

class CreditCost(BaseModel):
    """
    Represents the cost of a specific action in credits.
    """
    action_type: str = Field(..., description="The type of action.")
    cost: condecimal(ge=0) = Field(..., description="The cost in credits for the action.")
    is_variable: bool = Field(False, description="True if the cost is dynamic and not fixed.")