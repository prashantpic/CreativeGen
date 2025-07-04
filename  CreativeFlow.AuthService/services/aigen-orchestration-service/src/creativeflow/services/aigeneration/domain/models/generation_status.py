from enum import Enum

class GenerationStatus(str, Enum):
    """
    Defines the possible statuses for an AI creative generation request.
    The string inheritance allows it to be easily serialized to JSON.
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