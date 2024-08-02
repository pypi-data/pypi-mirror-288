# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SegmentCreateParams", "Data", "DataFiscalPeriod"]


class SegmentCreateParams(TypedDict, total=False):
    data: Required[Data]
    """Segments request body elements"""


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

    metrics: Required[str]
    """Metrics are the data items available for business and geographic segments, where

    - **SALES** = Sales/Revenue - Total revenues from the business line/geographic
      region,
    - **OPINC** = Operating Income/Loss - Operating income generated from the
      business line/geographic region,
    - **ASSETS** = Total Assets - Total assets from the business line/geographic
      region,
    - **DEP** = Depreciation Exp - Depreciation expense resulting from the business
      line/geographic segment,
    - **CAPEX** = Capital Expenditures - Capital expenditures resulting from the
      business line/geographic region
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

    fiscal_period: Annotated[DataFiscalPeriod, PropertyInfo(alias="fiscalPeriod")]

    periodicity: Literal["ANN", "ANN_R"]
    """Periodicity or frequency of the fiscal periods, where

    - **ANN** = Annual Original,
    - **ANN_R** = Annual Latest - _Includes Restatements_,
    """

    segment_type: Annotated[Literal["BUS", "GEO"], PropertyInfo(alias="segmentType")]
    """Segment type for the metrics, where

    - **BUS** = Business,
    - **GEO** = Geographic
    """
