# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import date
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["FundamentalsResponse", "Data"]


class Data(BaseModel):
    fiscal_period: Optional[int] = FieldInfo(alias="fiscalPeriod", default=None)
    """Fiscal Period indicator.

    Returns an integer representing the fiscal period for the requested item and
    periodicity. QUARTERLY CODE: 1-Fist Quarter; 2-Second Quarter; 3-Third Quarter;
    4-Fourth Quarter. SEMI-CODE: 1-First Semi-annual Period; 2-Second Semi-annual
    Period.
    """

    currency: Optional[str] = None
    """Currency code for the data.

    For a list of currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    eps_report_date: Optional[date] = FieldInfo(alias="epsReportDate", default=None)
    """The date the EPS was reported for the requested periodicity.

    In YYYY-MM-DD format. Unavailable data returned as 0001-01-01.
    """

    fiscal_end_date: Optional[date] = FieldInfo(alias="fiscalEndDate", default=None)
    """The normalized data the fiscal period ended."""

    fiscal_period_length: Optional[int] = FieldInfo(alias="fiscalPeriodLength", default=None)
    """Length of the fiscal period in days."""

    fiscal_year: Optional[int] = FieldInfo(alias="fiscalYear", default=None)
    """Fiscal year of the reported period in YYYY format."""

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

    periodicity: Optional[
        Literal["ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "CAL", "LTM", "LTM_R", "LTMSG", "LTM_SEMI", "YTD"]
    ] = None
    """
    Periodicity or frequency of the fiscal periods, where ANN = Annual Original,
    ANN_R = Annual Latest, QTR = Quarterly Original, QTR_R = Quarterly Latest, SEMI
    = Semi-Annual Original, SEMI_R = Semi-Annual Latest, LTM = Last Twelve Months
    Original, LTM_R = Last Twelve Months Latest, LTMSG = Last Twelve Months Global,
    [OA17959](https://my.apps.factset.com/oa/pages/17959), LTM_SEMI = Last Twelve
    Months - Semi-Annual Data and YTD = Year-to-date. Please note that the coverage
    for SEMI_R and LTM_R may be limited as fewer companies report with these
    periodicities.
    """

    report_date: Optional[date] = FieldInfo(alias="reportDate", default=None)
    """The date the reported fiscal period ended."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    update_type: Optional[Literal["Preliminary", "Final"]] = FieldInfo(alias="updateType", default=None)
    """
    Update Type: Preliminary - The period is updated from a report that usually
    contains limited or only key information., Final - The period is updated from a
    report where detailed information is available in financial statements including
    the notes to the line items.
    """

    value: Union[Optional[str], Optional[float], None] = None
    """Value of the data metric requested.

    Note that the type of value is 'object', and depending on the data metric
    requested, the value could be an object representation of a string or double.
    """


class FundamentalsResponse(BaseModel):
    data: Optional[List[Data]] = None
