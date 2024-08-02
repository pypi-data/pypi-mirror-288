# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import List, Union, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SegmentsResponse", "Data"]


class Data(BaseModel):
    label: Optional[str] = None
    """Report labels of the segment type requested."""

    date: Optional[datetime.date] = None
    """Date for the period requested expressed in YYYY-MM-DD format"""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security's best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    metric: Optional[str] = None
    """The requested `metric` input, representing the Fundamental Data Item.

    For a definition of the item please use the /fundamentals/v#/metrics endpoint.
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    value: Union[Optional[str], Optional[float], None] = None
    """Value of the data metric requested.

    Note that the type of value is 'object', and depending on the data metric
    requested, the value could be an object representation of a string or double.
    """


class SegmentsResponse(BaseModel):
    data: Optional[List[Data]] = None
