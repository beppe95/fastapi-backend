from typing import Optional

from pydantic import BaseModel, Field


class BaseError(BaseModel):
    message: str = Field(..., description="Error message or description")


class BaseIdentifiedError(BaseError):
    identifier: Optional[str] = Field(..., description="Unique identifier which this error references to")


class NotFoundError(BaseIdentifiedError):
    """The entity does not exist"""
