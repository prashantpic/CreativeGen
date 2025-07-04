```python
from typing import Optional

from pydantic import BaseModel


class StatusResponseSchema(BaseModel):
    """A generic response schema for status updates (e.g., after a DELETE)."""
    status: str = "success"
    message: Optional[str] = None
```