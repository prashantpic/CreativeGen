"""
Defines reusable pytest fixtures for setting up common test scenarios.
This helps simplify test setup and improves consistency.

Requirement Mapping: NFR-011 (Testability)
"""
import uuid
from unittest.mock import MagicMock

import pytest

from ..datamodels.common import UserContextDTO


@pytest.fixture
def mock_db_session() -> MagicMock:
    """
    Pytest fixture that provides a MagicMock for a database session.
    """
    return MagicMock()


@pytest.fixture
def sample_user_dto() -> UserContextDTO:
    """
    Pytest fixture that returns a pre-populated UserContextDTO instance.
    """
    return UserContextDTO(
        user_id=uuid.uuid4(),
        email="test.user@creativeflow.ai",
        roles=["pro_user"],
        permissions=["generate:image", "edit:project"],
        subscription_tier="Pro",
    )


@pytest.fixture
def test_correlation_id() -> str:
    """
    Pytest fixture that returns a unique correlation ID string for tests.
    """
    return f"test-correlation-id-{uuid.uuid4()}"