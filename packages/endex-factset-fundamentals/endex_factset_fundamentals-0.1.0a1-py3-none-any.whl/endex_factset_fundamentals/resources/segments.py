# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import segment_list_params, segment_create_params
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
from ..types.segments_response import SegmentsResponse

__all__ = ["SegmentsResource", "AsyncSegmentsResource"]


class SegmentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SegmentsResourceWithRawResponse:
        return SegmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SegmentsResourceWithStreamingResponse:
        return SegmentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: segment_create_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SegmentsResponse:
        """
        Retrieves Sales Metrics data for specified companies.

        The `/segments` endpoint currently supports Long Running asynchronous requests
        up to **20 minutes** via batch parameter. Id limits are increased to 30000 ids
        per request when using batch capability.This 30000 id limit has been derived
        based on single metric for one day. This feature is available for all users.

        Args:
          data: Segments request body elements

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/segments",
            body=maybe_transform({"data": data}, segment_create_params.SegmentCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SegmentsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        metrics: Literal["SALES", "OPINC", "ASSETS", "DEP", "CAPEX"],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "ANN_R"] | NotGiven = NOT_GIVEN,
        segment_type: Literal["BUS", "GEO"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SegmentsResponse:
        """
        Retrieves Fundamentals Metrics data for individual companies.

        The `/segments` endpoint currently supports Long Running asynchronous requests
        up to **20 minutes** via batch parameter. Id limits are increased to 2000 ids
        per request when using batch capability.This 2000 id limit has been derived
        based on single metric for one day. This feature is available for all users.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** =
              1000 per non-batch request / 2000 per batch request*</p> *<p>Make note, GET
              Method URL request lines are also limited to a total length of 8192 bytes (8KB).
              In cases where the service allows for thousands of ids, which may lead to
              exceeding this request line limit of 8KB, it's advised for any requests with
              large request lines to be requested through the respective "POST" method.</p>\\**

          metrics: Metrics are the data items available for business and geographic segments, where

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

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond with an HTTP Status Code of 202. Once a batch request is submitted,
              use batch status to see if the job has been completed. Once completed, retrieve
              the results of the request via batch-result. When using Batch, ids limit is
              increased to 30000 ids per request, though limits on query string via GET method
              still apply. It's advised to submit large lists of ids via POST method.

          fiscal_period_end: The fiscal period end expressed YYYY-MM-DD. Calendar date that will fall back to
              the most recently completed period during resolution.

          fiscal_period_start: The fiscal period start expressed as YYYY-MM-DD. Calendar date that will fall
              back to the most recent completed period during resolution.

          periodicity: Periodicity or frequency of the fiscal periods, where

              - **ANN** = Annual - Original,
              - **ANN_R** = Annual - Latest - _Includes Restatements_

          segment_type: Segment type for the metrics, where

              - **BUS** = Business,
              - **GEO** = Geographic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/segments",
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
                        "fiscal_period_end": fiscal_period_end,
                        "fiscal_period_start": fiscal_period_start,
                        "periodicity": periodicity,
                        "segment_type": segment_type,
                    },
                    segment_list_params.SegmentListParams,
                ),
            ),
            cast_to=SegmentsResponse,
        )


class AsyncSegmentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSegmentsResourceWithRawResponse:
        return AsyncSegmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSegmentsResourceWithStreamingResponse:
        return AsyncSegmentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: segment_create_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SegmentsResponse:
        """
        Retrieves Sales Metrics data for specified companies.

        The `/segments` endpoint currently supports Long Running asynchronous requests
        up to **20 minutes** via batch parameter. Id limits are increased to 30000 ids
        per request when using batch capability.This 30000 id limit has been derived
        based on single metric for one day. This feature is available for all users.

        Args:
          data: Segments request body elements

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/segments",
            body=await async_maybe_transform({"data": data}, segment_create_params.SegmentCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SegmentsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        metrics: Literal["SALES", "OPINC", "ASSETS", "DEP", "CAPEX"],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "ANN_R"] | NotGiven = NOT_GIVEN,
        segment_type: Literal["BUS", "GEO"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SegmentsResponse:
        """
        Retrieves Fundamentals Metrics data for individual companies.

        The `/segments` endpoint currently supports Long Running asynchronous requests
        up to **20 minutes** via batch parameter. Id limits are increased to 2000 ids
        per request when using batch capability.This 2000 id limit has been derived
        based on single metric for one day. This feature is available for all users.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** =
              1000 per non-batch request / 2000 per batch request*</p> *<p>Make note, GET
              Method URL request lines are also limited to a total length of 8192 bytes (8KB).
              In cases where the service allows for thousands of ids, which may lead to
              exceeding this request line limit of 8KB, it's advised for any requests with
              large request lines to be requested through the respective "POST" method.</p>\\**

          metrics: Metrics are the data items available for business and geographic segments, where

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

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond with an HTTP Status Code of 202. Once a batch request is submitted,
              use batch status to see if the job has been completed. Once completed, retrieve
              the results of the request via batch-result. When using Batch, ids limit is
              increased to 30000 ids per request, though limits on query string via GET method
              still apply. It's advised to submit large lists of ids via POST method.

          fiscal_period_end: The fiscal period end expressed YYYY-MM-DD. Calendar date that will fall back to
              the most recently completed period during resolution.

          fiscal_period_start: The fiscal period start expressed as YYYY-MM-DD. Calendar date that will fall
              back to the most recent completed period during resolution.

          periodicity: Periodicity or frequency of the fiscal periods, where

              - **ANN** = Annual - Original,
              - **ANN_R** = Annual - Latest - _Includes Restatements_

          segment_type: Segment type for the metrics, where

              - **BUS** = Business,
              - **GEO** = Geographic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/segments",
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
                        "fiscal_period_end": fiscal_period_end,
                        "fiscal_period_start": fiscal_period_start,
                        "periodicity": periodicity,
                        "segment_type": segment_type,
                    },
                    segment_list_params.SegmentListParams,
                ),
            ),
            cast_to=SegmentsResponse,
        )


class SegmentsResourceWithRawResponse:
    def __init__(self, segments: SegmentsResource) -> None:
        self._segments = segments

        self.create = to_raw_response_wrapper(
            segments.create,
        )
        self.list = to_raw_response_wrapper(
            segments.list,
        )


class AsyncSegmentsResourceWithRawResponse:
    def __init__(self, segments: AsyncSegmentsResource) -> None:
        self._segments = segments

        self.create = async_to_raw_response_wrapper(
            segments.create,
        )
        self.list = async_to_raw_response_wrapper(
            segments.list,
        )


class SegmentsResourceWithStreamingResponse:
    def __init__(self, segments: SegmentsResource) -> None:
        self._segments = segments

        self.create = to_streamed_response_wrapper(
            segments.create,
        )
        self.list = to_streamed_response_wrapper(
            segments.list,
        )


class AsyncSegmentsResourceWithStreamingResponse:
    def __init__(self, segments: AsyncSegmentsResource) -> None:
        self._segments = segments

        self.create = async_to_streamed_response_wrapper(
            segments.create,
        )
        self.list = async_to_streamed_response_wrapper(
            segments.list,
        )
