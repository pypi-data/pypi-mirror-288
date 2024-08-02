# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ProfileResponse", "Data", "DataAddress", "DataError", "DataExchange"]


class DataAddress(BaseModel):
    city: Optional[str] = None
    """City where the company head quarters are located"""

    country: Optional[str] = None
    """Full Country Name of the country where the company head quarters are located"""

    phone_number: Optional[str] = FieldInfo(alias="phoneNumber", default=None)
    """Phone number of the company"""

    state: Optional[str] = None
    """State code for which state the company head quarters are located"""

    state_name: Optional[str] = FieldInfo(alias="stateName", default=None)
    """Full State Name of the state where the company head quarters are located"""

    street_line1: Optional[str] = FieldInfo(alias="streetLine1", default=None)
    """Street line where the company head quarters are located"""

    street_line2: Optional[str] = FieldInfo(alias="streetLine2", default=None)
    """
    Additional Street line where the company head quarters are located, if available
    """

    website: Optional[str] = None
    """Website of the company"""

    zip: Optional[str] = None
    """Zipcode of the city where the company head quarters are located"""


class DataError(BaseModel):
    code: Optional[str] = None
    """status"""

    detail: Optional[str] = None
    """Error details explanation"""

    title: Optional[str] = None
    """The plain text error message"""


class DataExchange(BaseModel):
    exchange_id: Optional[str] = FieldInfo(alias="exchangeId", default=None)
    """The id of the exchange."""

    full_name: Optional[str] = FieldInfo(alias="fullName", default=None)
    """The full name of the exchange."""


class Data(BaseModel):
    address: Optional[DataAddress] = None

    business_summary: Optional[str] = FieldInfo(alias="businessSummary", default=None)
    """Summary of the security being requested"""

    ceo: Optional[str] = None
    """A chief executive officer (CEO) is the highest-ranking executive in a company"""

    error: Optional[DataError] = None

    exchange: Optional[DataExchange] = None
    """The name of the exchange for the security being requested."""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security's best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    industry: Optional[str] = None
    """The industry classification for this security.

    The industry level 5 RBIC (Revere Business Industry Classification) system is
    used in classification. For more info, visit:
    [OA page](https://my.apps.factset.com/oa/pages/17498)
    """

    industry_id: Optional[str] = FieldInfo(alias="industryId", default=None)
    """The industry classification Id for this security.

    The industry level 5 RBIC (Revere Business Industry Classification) system is
    used in classification. For more info, visit:
    [OA page](https://my.apps.factset.com/oa/pages/17498)
    """

    market_capitalization: Optional[int] = FieldInfo(alias="marketCapitalization", default=None)
    """The market capitalization of a company.

    It is the total value of the company's outstanding shares of common stock
    """

    name: Optional[str] = None
    """Name of the security"""

    number_of_employees: Optional[int] = FieldInfo(alias="numberOfEmployees", default=None)
    """Number of employees working in the company"""

    pe_ratio: Optional[float] = FieldInfo(alias="peRatio", default=None)
    """
    The price-earnings ratio (P/E ratio) is the ratio for valuing a company that
    measures its current share price relative to its per-share earnings (EPS)
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    sector: Optional[str] = None
    """The sector classification for this security.

    The sector level 2 RBIC (Revere Business Industry Classification) system is used
    in classification. For more info, visit:
    [OA page](https://my.apps.factset.com/oa/pages/17498)
    """

    sector_id: Optional[str] = FieldInfo(alias="sectorId", default=None)
    """The sector classification Id for this security.

    The sector level 2 RBIC (Revere Business Industry Classification) system is used
    in classification. For more info, visit:
    [OA page](https://my.apps.factset.com/oa/pages/17498)
    """

    shares_outstanding: Optional[int] = FieldInfo(alias="sharesOutstanding", default=None)
    """The number of common shares that a company has issued and are held by investors"""

    ticker_region: Optional[str] = FieldInfo(alias="tickerRegion", default=None)
    """FactSet Ticker-Region for the requested security."""

    total_market_capitalization: Optional[int] = FieldInfo(alias="totalMarketCapitalization", default=None)
    """The total public shares for the company's listed equity.

    This aggregates across all share classes, with including non-traded shares.
    """

    year_founded: Optional[int] = FieldInfo(alias="yearFounded", default=None)
    """The year this security is founded"""


class ProfileResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of profile objects"""
