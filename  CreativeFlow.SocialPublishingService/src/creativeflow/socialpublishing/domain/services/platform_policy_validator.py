"""
Domain service to validate content against platform-specific policies
before attempting to publish.
"""
from typing import List, Optional, Tuple

from ...api.v1.schemas import publishing_schemas


class PlatformPolicyValidator:
    """
    Encapsulates logic for checking if content adheres to requirements
    of a specific social media platform.
    """

    async def validate_content_for_platform(
        self,
        platform: str,
        content_text: Optional[str],
        assets: List[publishing_schemas.GeneratedAsset],
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates content against platform-specific policies.

        This method contains placeholder logic. Real-world implementation would
        involve more complex rules, possibly fetching metadata for assets to
        check dimensions, duration, etc.

        Args:
            platform: The name of the social media platform (e.g., "twitter").
            content_text: The text content of the post.
            assets: A list of media assets to be included in the post.

        Returns:
            A tuple containing a boolean (True if valid, False otherwise) and
            an optional error message string if invalid.
        """
        platform_lower = platform.lower()

        if platform_lower == "twitter":
            # Twitter/X character limit (basic check)
            limit = 280
            if content_text and len(content_text) > limit:
                return (
                    False,
                    f"Content exceeds Twitter's character limit of {limit} characters.",
                )

        elif platform_lower == "instagram":
            if not assets:
                return False, "Instagram posts require at least one image or video."
            # Placeholder for aspect ratio/resolution checks
            # for asset in assets:
            #     if asset.asset_type == 'image':
            #         # Check asset.metadata for dimensions
            #         pass

        elif platform_lower == "tiktok":
            if not assets:
                return False, "TikTok posts require a video."
            if any(asset.asset_type != "video" for asset in assets):
                return False, "Only video assets can be posted to TikTok."
            # Placeholder for video duration checks

        # Add more platform-specific rules here
        # ...

        return True, None