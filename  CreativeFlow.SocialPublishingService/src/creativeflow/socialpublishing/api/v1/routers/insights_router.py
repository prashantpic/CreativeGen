"""
FastAPI router for fetching platform-specific insights like trending hashtags
or best times to post.
"""
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from ....application.services import InsightsAggregationService
from ....dependencies import (get_current_user_id,
                            get_insights_aggregation_service)
from ..schemas import insights_schemas

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/{platform}/hashtags",
    response_model=insights_schemas.HashtagResponse,
    summary="Get Trending Hashtags",
    operation_id="get_trending_hashtags_insights__platform__hashtags_post",
)
async def get_trending_hashtags(
    platform: str,
    request_payload: insights_schemas.HashtagRequest,
    current_user_id: str = Depends(get_current_user_id),
    insights_service: InsightsAggregationService = Depends(
        get_insights_aggregation_service
    ),
):
    """
    Fetches trending hashtag suggestions for a given platform based on
    keywords and industry.

    Results are cached to improve performance and reduce API calls.
    """
    logger.info(
        "Fetching hashtags for user '%s', platform '%s', keywords '%s'",
        current_user_id,
        platform,
        request_payload.keywords,
    )
    response = await insights_service.get_trending_hashtags(
        user_id=current_user_id, platform=platform, request_payload=request_payload
    )
    return response


@router.get(
    "/{platform}/best-times",
    response_model=insights_schemas.BestTimeToPostResponse,
    summary="Get Best Times to Post",
    operation_id="get_best_times_to_post_insights__platform__best_times_get",
)
async def get_best_times_to_post(
    platform: str,
    connection_id: UUID = Query(...),
    current_user_id: str = Depends(get_current_user_id),
    insights_service: InsightsAggregationService = Depends(
        get_insights_aggregation_service
    ),
):
    """
    Fetches the best times to post for a specific connected account on a platform.

    This typically requires analysis of the account's follower engagement data,
    so a valid `connection_id` is required. Results are cached.
    """
    logger.info(
        "Fetching best times to post for user '%s', platform '%s', connection '%s'",
        current_user_id,
        platform,
        connection_id,
    )
    response = await insights_service.get_best_times_to_post(
        user_id=current_user_id, platform=platform, connection_id=connection_id
    )
    return response