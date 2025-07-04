from enum import Enum


class GenerationStatus(str, Enum):
    """
    Enumeration of all possible statuses for an AI Generation Request.
    This provides a standardized, controlled vocabulary for the request lifecycle.
    """
    PENDING = "PENDING"
    VALIDATING_CREDITS = "VALIDATING_CREDITS"
    PUBLISHING_TO_QUEUE = "PUBLISHING_TO_QUEUE"
    PROCESSING_SAMPLES = "PROCESSING_SAMPLES"
    AWAITING_SELECTION = "AWAITING_SELECTION"
    PROCESSING_FINAL = "PROCESSING_FINAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CONTENT_REJECTED = "CONTENT_REJECTED"