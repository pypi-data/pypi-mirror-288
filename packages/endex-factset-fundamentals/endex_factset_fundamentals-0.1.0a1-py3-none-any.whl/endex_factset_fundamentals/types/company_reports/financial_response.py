# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["FinancialResponse", "Data", "DataItem"]


class DataItem(BaseModel):
    display_level: Optional[str] = FieldInfo(alias="displayLevel", default=None)
    """Describes the level of displaying the item"""

    display_order: Optional[int] = FieldInfo(alias="displayOrder", default=None)
    """Describes the order of displaying the item"""

    name: Optional[str] = None
    """Name of the metric"""

    value: Optional[List[Optional[float]]] = None


class Data(BaseModel):
    fiscal_year: Optional[List[Optional[str]]] = FieldInfo(alias="fiscalYear", default=None)

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security's best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    items: Optional[List[DataItem]] = None

    report_date: Optional[List[Optional[str]]] = FieldInfo(alias="reportDate", default=None)

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""


class FinancialResponse(BaseModel):
    data: Optional[List[Data]] = None
