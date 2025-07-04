"""
Defines a base Pydantic model with common configurations to be inherited by other DTOs.
This ensures consistency in data model definitions across the platform.

Requirement Mapping: NFR-009 (Modularity)
"""
import pydantic


def to_camel_case(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.

    For example, 'user_profile_image' becomes 'userProfileImage'.

    Args:
        snake_str: The string in snake_case format.

    Returns:
        The string in camelCase format.
    """
    if "_" not in snake_str:
        return snake_str
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])


class SharedBaseModel(pydantic.BaseModel):
    """
    A shared base model that provides common Pydantic configurations.

    - `populate_by_name`: Allows populating model fields by either their name or alias.
    - `from_attributes`: Enables creating models from ORM objects (previously `orm_mode`).
    - `alias_generator`: Automatically generates camelCase aliases for snake_case field names.
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        alias_generator=to_camel_case,
    )

    def to_dict_by_alias(self, **kwargs) -> dict:
        """
        Converts the model to a dictionary using field aliases (camelCase).

        This is a convenience method for `model_dump(by_alias=True)`.

        Args:
            **kwargs: Additional arguments to pass to `model_dump`.

        Returns:
            A dictionary representation of the model with camelCase keys.
        """
        return self.model_dump(by_alias=True, **kwargs)