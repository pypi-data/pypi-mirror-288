# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import metric_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.metrics_response import MetricsResponse

__all__ = ["MetricsResource", "AsyncMetricsResource"]


class MetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        category: Literal[
            "INCOME_STATEMENT",
            "BALANCE_SHEET",
            "CASH_FLOW",
            "RATIOS",
            "FINANCIAL_SERVICES",
            "INDUSTRY_METRICS",
            "PENSION_AND_POSTRETIREMENT",
            "MARKET_DATA",
            "MISCELLANEOUS",
            "DATES",
        ]
        | NotGiven = NOT_GIVEN,
        metric_data_type: str | NotGiven = NOT_GIVEN,
        subcategory: Literal[
            "ASSETS",
            "BALANCE_SHEET",
            "HEALTHCARE",
            "LIABILITIES",
            "PER_SHARE",
            "SHAREHOLDERS_EQUITY",
            "SUPPLEMENTAL",
            "CASH_FLOW",
            "CHANGE_IN_CASH",
            "FINANCING",
            "INVESTING",
            "OPERATING",
            "DATES",
            "INCOME_STATEMENT",
            "NON-OPERATING",
            "RETAIL",
            "AIRLINES",
            "BANK",
            "BANKING",
            "HOTELS_AND_GAMING",
            "METALS_AND_MINING",
            "OIL_AND_GAS",
            "PHARMACEUTICAL",
            "REIT",
            "MARKET_DATA",
            "CLASSIFICATION",
            "CORPORATE_DATA",
            "FINANCIAL_RECORDS",
            "INDICATOR",
            "EMPLOYEES_AND_MANAGEMENT",
            "PENSION_AND_POSTRETIREMENT",
            "FINANCIAL",
            "GROWTH_RATE",
            "LIQUIDITY",
            "PROFITABILITY",
            "SIZE",
            "VALUATION",
            "OTHER",
            "HOMEBUILDING",
            "NET_INCOME",
            "TELECOM",
            "UTILITY",
            "INSURANCE",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricsResponse:
        """
        Returns list of available FF\\__\\** metrics that can be used in the `metrics`
        parameter of related endpoints. These are related to FactSet Fundamentals
        standardized data. As Reported will be available in future endpoints. Leave
        Category and Subcategory blank to request all available items. The Endpoint Data
        model is optimized for time-series data with periodicity. Some items in this
        list are non-time series. **For methodology definitions, reference the
        `OApageID` or `OAurl` response items to launch the available methodology page.**

        Args:
          category: Filters the list of FF\\__\\** metrics by major category -

              - **INCOME_STATEMENT** = Income Statement line items, such as Sales, Gross
                Profit, Net Income.
              - **BALANCE_SHEET** = Balance Sheet line items, such as Assets, Liabilities, and
                Shareholders Equity.
              - **CASH_FLOW** = Cash Flow Statement line items, such as Financing activities,
                Operation, and Per Share.
              - **RATIOS** = Pre-calculated Ratios, including Financial, Growth Rates,
                Profitability, Liquidity, Size, and Valuation.
              - **FINANCIAL_SERVICES** = Financial Statement Items modified for Financial
                Services companies.
              - **INDUSTRY_METRICS** = Industry Specific Line Items or Modifications. View
                subcategory for list of Industries.
              - **PENSION_AND_POSTRETIREMENT** = Accumulated Pension Benefit Obligations and
                related data.
              - **MARKET_DATA** = General Market Data, such as Shares Outstanding. _Note -
                /factset-prices/prices/ endpoints may be better suited for pricing-related
                market data._
              - **MISCELLANEOUS** = Corporation Data, Financial Records details, Indicators.
              - **DATES** = Relevant Dates

          metric_data_type: Returns general data type of the metrics like integer, float or strings, when
              left blankmetrics with all data types would be returned

          subcategory: Sub-Category Filter for the Primary Category Requested. Choose a related
              sub-category for the Category requested-

              - **INCOME_STATEMENT** - INCOME_STATEMENT, NON-OPERATING, PER_SHARE,
                SUPPLEMENTAL, OTHER
              - **BALANCE_SHEET** - ASSETS, BALANCE_SHEET, HEALTHCARE, LIABILITIES, PER_SHARE,
                SHAREHOLDERS_EQUITY, SUPPLEMENTAL
              - **CASH_FLOW** - CASH_FLOW, CHANGE_IN_CASH, FINANCING, INVESTING, OPERATING,
                PER_SHARE, SUPPLEMENTAL
              - **RATIOS** - FINANCIAL, GROWTH_RATE, LIQUIDITY, PROFITABILITY, SIZE, VALUATION
              - **FINANCIAL_SERVICES** - BALANCE_SHEET, INCOME_STATEMENT, SUPPLEMENTAL
              - **INDUSTRY_METRICS** - AIRLINES, BANKING, HOTELS_AND_GAMING,
                METALS_AND_MINING, OIL_AND_GAS, PHARMACEUTICAL, REIT, RETAIL, BANK, INSURANCE,
                UTILITY
              - **PENSION_AND_POSTRETIREMENT** - PENSION_AND_POSTRETIREMENT
              - **MARKET_DATA** - MARKET_DATA
              - **MISCELLANEOUS** - CLASSIFICATION, CORPORATE_DATA, FINANCIAL_RECORDS,
                INDICATOR, EMPLOYEES_AND_MANAGEMENT
              - **DATES** - DATES

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category": category,
                        "metric_data_type": metric_data_type,
                        "subcategory": subcategory,
                    },
                    metric_list_params.MetricListParams,
                ),
            ),
            cast_to=MetricsResponse,
        )


class AsyncMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        category: Literal[
            "INCOME_STATEMENT",
            "BALANCE_SHEET",
            "CASH_FLOW",
            "RATIOS",
            "FINANCIAL_SERVICES",
            "INDUSTRY_METRICS",
            "PENSION_AND_POSTRETIREMENT",
            "MARKET_DATA",
            "MISCELLANEOUS",
            "DATES",
        ]
        | NotGiven = NOT_GIVEN,
        metric_data_type: str | NotGiven = NOT_GIVEN,
        subcategory: Literal[
            "ASSETS",
            "BALANCE_SHEET",
            "HEALTHCARE",
            "LIABILITIES",
            "PER_SHARE",
            "SHAREHOLDERS_EQUITY",
            "SUPPLEMENTAL",
            "CASH_FLOW",
            "CHANGE_IN_CASH",
            "FINANCING",
            "INVESTING",
            "OPERATING",
            "DATES",
            "INCOME_STATEMENT",
            "NON-OPERATING",
            "RETAIL",
            "AIRLINES",
            "BANK",
            "BANKING",
            "HOTELS_AND_GAMING",
            "METALS_AND_MINING",
            "OIL_AND_GAS",
            "PHARMACEUTICAL",
            "REIT",
            "MARKET_DATA",
            "CLASSIFICATION",
            "CORPORATE_DATA",
            "FINANCIAL_RECORDS",
            "INDICATOR",
            "EMPLOYEES_AND_MANAGEMENT",
            "PENSION_AND_POSTRETIREMENT",
            "FINANCIAL",
            "GROWTH_RATE",
            "LIQUIDITY",
            "PROFITABILITY",
            "SIZE",
            "VALUATION",
            "OTHER",
            "HOMEBUILDING",
            "NET_INCOME",
            "TELECOM",
            "UTILITY",
            "INSURANCE",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricsResponse:
        """
        Returns list of available FF\\__\\** metrics that can be used in the `metrics`
        parameter of related endpoints. These are related to FactSet Fundamentals
        standardized data. As Reported will be available in future endpoints. Leave
        Category and Subcategory blank to request all available items. The Endpoint Data
        model is optimized for time-series data with periodicity. Some items in this
        list are non-time series. **For methodology definitions, reference the
        `OApageID` or `OAurl` response items to launch the available methodology page.**

        Args:
          category: Filters the list of FF\\__\\** metrics by major category -

              - **INCOME_STATEMENT** = Income Statement line items, such as Sales, Gross
                Profit, Net Income.
              - **BALANCE_SHEET** = Balance Sheet line items, such as Assets, Liabilities, and
                Shareholders Equity.
              - **CASH_FLOW** = Cash Flow Statement line items, such as Financing activities,
                Operation, and Per Share.
              - **RATIOS** = Pre-calculated Ratios, including Financial, Growth Rates,
                Profitability, Liquidity, Size, and Valuation.
              - **FINANCIAL_SERVICES** = Financial Statement Items modified for Financial
                Services companies.
              - **INDUSTRY_METRICS** = Industry Specific Line Items or Modifications. View
                subcategory for list of Industries.
              - **PENSION_AND_POSTRETIREMENT** = Accumulated Pension Benefit Obligations and
                related data.
              - **MARKET_DATA** = General Market Data, such as Shares Outstanding. _Note -
                /factset-prices/prices/ endpoints may be better suited for pricing-related
                market data._
              - **MISCELLANEOUS** = Corporation Data, Financial Records details, Indicators.
              - **DATES** = Relevant Dates

          metric_data_type: Returns general data type of the metrics like integer, float or strings, when
              left blankmetrics with all data types would be returned

          subcategory: Sub-Category Filter for the Primary Category Requested. Choose a related
              sub-category for the Category requested-

              - **INCOME_STATEMENT** - INCOME_STATEMENT, NON-OPERATING, PER_SHARE,
                SUPPLEMENTAL, OTHER
              - **BALANCE_SHEET** - ASSETS, BALANCE_SHEET, HEALTHCARE, LIABILITIES, PER_SHARE,
                SHAREHOLDERS_EQUITY, SUPPLEMENTAL
              - **CASH_FLOW** - CASH_FLOW, CHANGE_IN_CASH, FINANCING, INVESTING, OPERATING,
                PER_SHARE, SUPPLEMENTAL
              - **RATIOS** - FINANCIAL, GROWTH_RATE, LIQUIDITY, PROFITABILITY, SIZE, VALUATION
              - **FINANCIAL_SERVICES** - BALANCE_SHEET, INCOME_STATEMENT, SUPPLEMENTAL
              - **INDUSTRY_METRICS** - AIRLINES, BANKING, HOTELS_AND_GAMING,
                METALS_AND_MINING, OIL_AND_GAS, PHARMACEUTICAL, REIT, RETAIL, BANK, INSURANCE,
                UTILITY
              - **PENSION_AND_POSTRETIREMENT** - PENSION_AND_POSTRETIREMENT
              - **MARKET_DATA** - MARKET_DATA
              - **MISCELLANEOUS** - CLASSIFICATION, CORPORATE_DATA, FINANCIAL_RECORDS,
                INDICATOR, EMPLOYEES_AND_MANAGEMENT
              - **DATES** - DATES

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category": category,
                        "metric_data_type": metric_data_type,
                        "subcategory": subcategory,
                    },
                    metric_list_params.MetricListParams,
                ),
            ),
            cast_to=MetricsResponse,
        )


class MetricsResourceWithRawResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.list = to_raw_response_wrapper(
            metrics.list,
        )


class AsyncMetricsResourceWithRawResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.list = async_to_raw_response_wrapper(
            metrics.list,
        )


class MetricsResourceWithStreamingResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.list = to_streamed_response_wrapper(
            metrics.list,
        )


class AsyncMetricsResourceWithStreamingResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.list = async_to_streamed_response_wrapper(
            metrics.list,
        )
