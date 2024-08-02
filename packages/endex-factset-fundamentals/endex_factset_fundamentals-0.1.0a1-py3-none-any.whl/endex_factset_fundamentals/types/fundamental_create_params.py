# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FundamentalCreateParams", "Data", "DataFiscalPeriod"]


class FundamentalCreateParams(TypedDict, total=False):
    data: Required[Data]
    """Fundamentals request body elements"""


class DataFiscalPeriod(TypedDict, total=False):
    end: str
    """The fiscal period end expressed YYYY-MM-DD.

    Calendar date that will fall back to the most recent completed period during
    resolution.
    """

    start: str
    """The fiscal period start expressed as YYYY-MM-DD.

    Calendar date that will fall back to the most recently completed period during
    resolution.
    """


class Data(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids.

    <p>ids limit =  1000 per non-batch request / 30000 per batch request</p>
    """

    metrics: Required[List[str]]
    """Requested List of Financial Statement Items or Ratios.

    Use /metrics endpoint for a complete list of available FF\\__\\** metric items.
    """

    batch: Literal["Y", "N"]
    """
    Enables the ability to asynchronously "batch" the request, supporting a
    long-running request for up to 20 minutes. Upon requesting batch=Y, the service
    will respond back with an HTTP Status Code of 202. Once a batch request is
    submitted, use batch status to see if the job has been completed. Once
    completed, retrieve the results of the request via batch-result. When using
    Batch, ids limit is increased to 30000 ids per request, though limits on query
    string via GET method still apply. It's advised to submit large lists of ids via
    POST method.
    """

    currency: str
    """Currency code for currency values.

    For a list of currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    fiscal_period: Annotated[DataFiscalPeriod, PropertyInfo(alias="fiscalPeriod")]

    periodicity: Literal["ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "LTM_R", "LTMSG", "LTM_SEMI", "YTD"]
    """Periodicity or frequency of the fiscal periods, where

    - **ANN** = Annual Original,
    - **ANN_R** = Annual Latest - _Includes Restatements_,
    - **QTR** = Quarterly,
    - **QTR_R** = Quarterly Latest - _Includes Restatements_,
    - **SEMI** = Semi-Annual,
    - **SEMI_R** = Semi-Annual Latest - _Includes Restatements_,
    - **LTM** = Last Twelve Months,
    - **LTM_R** = Last Twelve Months Latest - _Includes Restatements_,
    - **LTM_SEMI** = Last Twelve Months - Semi-Annually Reported Data,
    - **LTMSG** = Last Twelve Months Global
      [OA17959](https://my.apps.factset.com/oa/pages/17959) and
    - **YTD** = Year-to-date

    Please note that the coverage for SEMI_R and LTM_R may be limited as fewer
    companies report with these periodicities.
    """

    update_type: Annotated[Literal["RP", "RF"], PropertyInfo(alias="updateType")]
    """Update Status flag:

    - **RP** = Include preliminary data,
    - **RF** = Only final data
    """
