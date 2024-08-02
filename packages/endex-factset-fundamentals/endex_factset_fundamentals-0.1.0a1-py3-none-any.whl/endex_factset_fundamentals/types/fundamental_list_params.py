# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FundamentalListParams"]


class FundamentalListParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids.<p>**\\**ids limit** = 1000 per non-batch request / 2000 per batch
    request*</p> *<p>Make note, GET Method URL request lines are also limited to a
    total length of 8192 bytes (8KB). In cases where the service allows for
    thousands of ids, which may lead to exceeding this request line limit of 8KB,
    it's advised for any requests with large request lines to be requested through
    the respective "POST" method.</p>\\**
    """

    metrics: Required[List[str]]
    """Requested List of Financial Statement Items or Ratios.

    Use /metrics endpoint for a complete list of available FF\\__* metric items.
    <p>*When requesting multiple metrics, you cannot mix metric data types (e.g.
    strings and floats). Please use /metrics endpoints for context on metric
    dataType to avoid null data.\\**</p> <p>**\\**metrics limit** = 1600 per
    request*</p> *<p>Make note, GET Method URL request lines are also limited to a
    total length of 8192 bytes (8KB). In cases where the service allows for
    thousands of metrics, which may lead to exceeding this request line limit of
    8KB, its advised for any requests with large request lines to be requested
    through the respective "POST" method.</p>\\**
    """

    batch: Literal["Y", "N"]
    """
    Enables the ability to asynchronously "batch" the request, supporting a
    long-running request for up to 20 minutes. Upon requesting batch=Y, the service
    will respond with an HTTP Status Code of 202. Once a batch request is submitted,
    use batch status to see if the job has been completed. Once completed, retrieve
    the results of the request via batch-result. When using Batch, ids limit is
    increased to 30000 ids per request, though limits on query string via GET method
    still apply. It's advised to submit large lists of ids via POST method.
    """

    currency: str
    """Currency code for currency values.

    For a list of currency ISO codes, visit Online Assistant Page
    [OA1470](https://my.apps.factset.com/oa/pages/1470).

    Giving input as "DOC" would give the values in reporting currency for the
    requested ids.
    """

    fiscal_period_end: Annotated[str, PropertyInfo(alias="fiscalPeriodEnd")]
    """The fiscal period end expressed YYYY-MM-DD.

    Calendar date that will fall back to the most recently completed period during
    resolution.
    """

    fiscal_period_start: Annotated[str, PropertyInfo(alias="fiscalPeriodStart")]
    """The fiscal period start expressed as YYYY-MM-DD.

    Calendar date that will fall back to the most recent completed period during
    resolution.
    """

    periodicity: Literal["ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "LTM_R", "LTM_SEMI", "LTMSG", "YTD"]
    """Periodicity or frequency of the fiscal periods, where

    - **ANN** = Annual - Original,
    - **ANN_R** = Annual - Latest - _Includes Restatements_,
    - **QTR** = Quarterly - Original,
    - **QTR_R** = Quarterly - Latest - _Includes Restatements_,
    - **SEMI** = Semi-Annual,
    - **SEMI_R** = Semi-Annual - Latest - _Includes Restatements_,
    - **LTM** = Last Twelve Months,
    - **LTM_R** = Last Twelve Months - Latest - _Includes Restatements_,
    - **LTMSG** = Last Twelve Months Global
      [OA17959](https://my.apps.factset.com/oa/pages/17959),
    - **LTM_SEMI** = Last Twelve Months, Semi-Annually Reported Data,
    - **YTD** = Year-to-date.

    Please note that the coverage for SEMI_R and LTM_R may be limited as fewer
    companies report with these periodicities.
    """

    update_type: Annotated[Literal["RP", "RF"], PropertyInfo(alias="updateType")]
    """Update Status Flag:

    - **RP** = Include preliminary data,
    - **RF** = Only final data
    """
