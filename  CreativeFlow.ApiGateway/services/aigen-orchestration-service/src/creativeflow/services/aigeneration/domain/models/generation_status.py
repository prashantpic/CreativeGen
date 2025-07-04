from enum import Enum

class GenerationStatus(str, Enum):
    """
    Defines the possible lifecycle statuses for a generation request.
    Inherits from str to be easily JSON serializable.
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