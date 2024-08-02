# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["FinancialStatementRetrieveParams"]


class FinancialStatementRetrieveParams(TypedDict, total=False):
    id: Required[str]
    """The requested security identifier.

    Accepted ID types include Market Ticker, SEDOL, ISIN, CUSIP, or FactSet
    Permanent Id.
    """

    periodicity: Required[Literal["ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "YTD"]]
    """Periodicity or frequency of the fiscal periods, where

    - **ANN** = Annual - Original,
    - **ANN_R** = Annual - Latest - _Includes Restatements_,
    - **QTR** = Quarterly - Original,
    - **QTR_R** = Quarterly - Latest - _Includes Restatements_,
    - **SEMI** = Semi-Annual,
    - **SEMI_R** = Semi-Annual - Latest - _Includes Restatements_,
    - **LTM** = Last Twelve Months,
    - **YTD** = Year-to-date.

    Please note that the coverage for SEMI_R may be limited as fewer companies
    report with this periodicity.
    """

    statement_type: Required[Annotated[Literal["BS", "CF", "IS"], PropertyInfo(alias="statementType")]]
    """The type of financial statement being requested."""

    limit: int
    """The time period for the returned data.

    Within range of 1 to 100. If not specified default will be 4.
    """

    update_type: Annotated[Literal["RP", "RF"], PropertyInfo(alias="updateType")]
    """Update Status Flag:

    - **RP** = Include preliminary data,
    - **RF** = Only final data
    """
