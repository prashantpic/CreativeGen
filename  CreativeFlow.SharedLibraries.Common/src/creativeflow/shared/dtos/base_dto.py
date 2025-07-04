"""
Defines a base Pydantic model for all Data Transfer Objects (DTOs).
"""
from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    A base Pydantic model for all DTOs in the application.

    This class includes common configurations to ensure consistency across all
    data transfer objects.

    Attributes:
        model_config (ConfigDict): Pydantic model configuration.
            - from_attributes=True: Allows creating models from ORM objects.
            - populate_by_name=True: Allows populating model fields by either
              field name or alias.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )