# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import fundamental_list_params, fundamental_create_params
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
from ..types.fundamentals_response import FundamentalsResponse

__all__ = ["FundamentalsResource", "AsyncFundamentalsResource"]


class FundamentalsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FundamentalsResourceWithRawResponse:
        return FundamentalsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FundamentalsResourceWithStreamingResponse:
        return FundamentalsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: fundamental_create_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundamentalsResponse:
        """Retrieves FactSet Fundamental standardized data for specified securities.

        Use
        the `/metrics` endpoint to retrieve a full list of valid metrics or data items.

        The `/fundamentals` endpoint currently supports Long Running asynchronous
        requests up to **20 minutes** via batch parameter. Id limits are increased to
        30000 ids per request when using batch capability. This 30000 id limit has been
        derived based on single metric for one day. This feature is available for all
        users.

        Args:
          data: Fundamentals request body elements

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/fundamentals",
            body=maybe_transform({"data": data}, fundamental_create_params.FundamentalCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FundamentalsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        periodicity: Literal[
            "ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "LTM_R", "LTM_SEMI", "LTMSG", "YTD"
        ]
        | NotGiven = NOT_GIVEN,
        update_type: Literal["RP", "RF"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundamentalsResponse:
        """Retrieves FactSet Fundamental standardized data for specified securities.

        Use
        the `/metrics` endpoint to retrieve a full list of valid metrics or data items.

        The `/fundamentals` endpoint currently supports Long Running asynchronous
        requests up to **20 minutes** via batch parameter. Id limits are increased to
        2000 ids per request when using batch capability. This 2000 id limit has been
        derived based on single metric for one day. This feature is available for all
        users.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** =
              1000 per non-batch request / 2000 per batch request*</p> *<p>Make note, GET
              Method URL request lines are also limited to a total length of 8192 bytes (8KB).
              In cases where the service allows for thousands of ids, which may lead to
              exceeding this request line limit of 8KB, it's advised for any requests with
              large request lines to be requested through the respective "POST" method.</p>\\**

          metrics: Requested List of Financial Statement Items or Ratios. Use /metrics endpoint for
              a complete list of available FF\\__* metric items. <p>*When requesting multiple
              metrics, you cannot mix metric data types (e.g. strings and floats). Please use
              /metrics endpoints for context on metric dataType to avoid null data.\\**</p>
              <p>**\\**metrics limit** = 1600 per request*</p> *<p>Make note, GET Method URL
              request lines are also limited to a total length of 8192 bytes (8KB). In cases
              where the service allows for thousands of metrics, which may lead to exceeding
              this request line limit of 8KB, its advised for any requests with large request
              lines to be requested through the respective "POST" method.</p>\\**

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond with an HTTP Status Code of 202. Once a batch request is submitted,
              use batch status to see if the job has been completed. Once completed, retrieve
              the results of the request via batch-result. When using Batch, ids limit is
              increased to 30000 ids per request, though limits on query string via GET method
              still apply. It's advised to submit large lists of ids via POST method.

          currency: Currency code for currency values. For a list of currency ISO codes, visit
              Online Assistant Page [OA1470](https://my.apps.factset.com/oa/pages/1470).

              Giving input as "DOC" would give the values in reporting currency for the
              requested ids.

          fiscal_period_end: The fiscal period end expressed YYYY-MM-DD. Calendar date that will fall back to
              the most recently completed period during resolution.

          fiscal_period_start: The fiscal period start expressed as YYYY-MM-DD. Calendar date that will fall
              back to the most recent completed period during resolution.

          periodicity: Periodicity or frequency of the fiscal periods, where

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

          update_type:
              Update Status Flag:

              - **RP** = Include preliminary data,
              - **RF** = Only final data

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/fundamentals",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "metrics": metrics,
                        "batch": batch,
                        "currency": currency,
                        "fiscal_period_end": fiscal_period_end,
                        "fiscal_period_start": fiscal_period_start,
                        "periodicity": periodicity,
                        "update_type": update_type,
                    },
                    fundamental_list_params.FundamentalListParams,
                ),
            ),
            cast_to=FundamentalsResponse,
        )


class AsyncFundamentalsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFundamentalsResourceWithRawResponse:
        return AsyncFundamentalsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFundamentalsResourceWithStreamingResponse:
        return AsyncFundamentalsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: fundamental_create_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundamentalsResponse:
        """Retrieves FactSet Fundamental standardized data for specified securities.

        Use
        the `/metrics` endpoint to retrieve a full list of valid metrics or data items.

        The `/fundamentals` endpoint currently supports Long Running asynchronous
        requests up to **20 minutes** via batch parameter. Id limits are increased to
        30000 ids per request when using batch capability. This 30000 id limit has been
        derived based on single metric for one day. This feature is available for all
        users.

        Args:
          data: Fundamentals request body elements

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/fundamentals",
            body=await async_maybe_transform({"data": data}, fundamental_create_params.FundamentalCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FundamentalsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        periodicity: Literal[
            "ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "LTM_R", "LTM_SEMI", "LTMSG", "YTD"
        ]
        | NotGiven = NOT_GIVEN,
        update_type: Literal["RP", "RF"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundamentalsResponse:
        """Retrieves FactSet Fundamental standardized data for specified securities.

        Use
        the `/metrics` endpoint to retrieve a full list of valid metrics or data items.

        The `/fundamentals` endpoint currently supports Long Running asynchronous
        requests up to **20 minutes** via batch parameter. Id limits are increased to
        2000 ids per request when using batch capability. This 2000 id limit has been
        derived based on single metric for one day. This feature is available for all
        users.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** =
              1000 per non-batch request / 2000 per batch request*</p> *<p>Make note, GET
              Method URL request lines are also limited to a total length of 8192 bytes (8KB).
              In cases where the service allows for thousands of ids, which may lead to
              exceeding this request line limit of 8KB, it's advised for any requests with
              large request lines to be requested through the respective "POST" method.</p>\\**

          metrics: Requested List of Financial Statement Items or Ratios. Use /metrics endpoint for
              a complete list of available FF\\__* metric items. <p>*When requesting multiple
              metrics, you cannot mix metric data types (e.g. strings and floats). Please use
              /metrics endpoints for context on metric dataType to avoid null data.\\**</p>
              <p>**\\**metrics limit** = 1600 per request*</p> *<p>Make note, GET Method URL
              request lines are also limited to a total length of 8192 bytes (8KB). In cases
              where the service allows for thousands of metrics, which may lead to exceeding
              this request line limit of 8KB, its advised for any requests with large request
              lines to be requested through the respective "POST" method.</p>\\**

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond with an HTTP Status Code of 202. Once a batch request is submitted,
              use batch status to see if the job has been completed. Once completed, retrieve
              the results of the request via batch-result. When using Batch, ids limit is
              increased to 30000 ids per request, though limits on query string via GET method
              still apply. It's advised to submit large lists of ids via POST method.

          currency: Currency code for currency values. For a list of currency ISO codes, visit
              Online Assistant Page [OA1470](https://my.apps.factset.com/oa/pages/1470).

              Giving input as "DOC" would give the values in reporting currency for the
              requested ids.

          fiscal_period_end: The fiscal period end expressed YYYY-MM-DD. Calendar date that will fall back to
              the most recently completed period during resolution.

          fiscal_period_start: The fiscal period start expressed as YYYY-MM-DD. Calendar date that will fall
              back to the most recent completed period during resolution.

          periodicity: Periodicity or frequency of the fiscal periods, where

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

          update_type:
              Update Status Flag:

              - **RP** = Include preliminary data,
              - **RF** = Only final data

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/fundamentals",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "metrics": metrics,
                        "batch": batch,
                        "currency": currency,
                        "fiscal_period_end": fiscal_period_end,
                        "fiscal_period_start": fiscal_period_start,
                        "periodicity": periodicity,
                        "update_type": update_type,
                    },
                    fundamental_list_params.FundamentalListParams,
                ),
            ),
            cast_to=FundamentalsResponse,
        )


class FundamentalsResourceWithRawResponse:
    def __init__(self, fundamentals: FundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.create = to_raw_response_wrapper(
            fundamentals.create,
        )
        self.list = to_raw_response_wrapper(
            fundamentals.list,
        )


class AsyncFundamentalsResourceWithRawResponse:
    def __init__(self, fundamentals: AsyncFundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.create = async_to_raw_response_wrapper(
            fundamentals.create,
        )
        self.list = async_to_raw_response_wrapper(
            fundamentals.list,
        )


class FundamentalsResourceWithStreamingResponse:
    def __init__(self, fundamentals: FundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.create = to_streamed_response_wrapper(
            fundamentals.create,
        )
        self.list = to_streamed_response_wrapper(
            fundamentals.list,
        )


class AsyncFundamentalsResourceWithStreamingResponse:
    def __init__(self, fundamentals: AsyncFundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.create = async_to_streamed_response_wrapper(
            fundamentals.create,
        )
        self.list = async_to_streamed_response_wrapper(
            fundamentals.list,
        )
