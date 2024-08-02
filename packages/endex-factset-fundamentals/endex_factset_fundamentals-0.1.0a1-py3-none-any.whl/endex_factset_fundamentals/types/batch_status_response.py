# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["BatchStatusResponse", "Data", "DataError"]


class DataError(BaseModel):
    id: Optional[str] = None
    """A UUID for this particular occurrence of the problem."""

    code: Optional[str] = None
    """status"""

    title: Optional[str] = None
    """The plain text error message"""


class Data(BaseModel):
    id: Optional[str] = None
    """the id of batch request."""

    end_time: Optional[datetime] = FieldInfo(alias="endTime", default=None)
    """Time when the batch request is ended.

    This is in Eastern Time Zone. The date-time format is expressed as
    [YYYY-MM-DD]T[HH:MM:SSS], following ISO 8601.
    """

    error: Optional[DataError] = None

    start_time: Optional[datetime] = FieldInfo(alias="startTime", default=None)
    """Time when the batch request is started.

    This is in Eastern Time Zone. The date-time format is expressed as
    [YYYY-MM-DD]T[HH:MM:SSS], following ISO 8601.
    """

    status: Optional[Literal["queued", "executing", "created", "failed"]] = None


class BatchStatusResponse(BaseModel):
    data: Optional[Data] = None
