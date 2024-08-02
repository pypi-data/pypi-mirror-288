# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.company_reports import fundamental_retrieve_params
from ...types.company_reports.company_fundamentals_response import CompanyFundamentalsResponse

__all__ = ["FundamentalsResource", "AsyncFundamentalsResource"]


class FundamentalsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FundamentalsResourceWithRawResponse:
        return FundamentalsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FundamentalsResourceWithStreamingResponse:
        return FundamentalsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyFundamentalsResponse:
        """
        Returns detailed insights on specified publicly traded company's various key
        financial measures or fundamentals like cash per share, dividend, EPS, EBIT etc.
        All values provided in the response are absolute.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. <p>**\\**ids limit** = 50
              per request\\**</p>

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/company-reports/fundamentals",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"ids": ids}, fundamental_retrieve_params.FundamentalRetrieveParams),
            ),
            cast_to=CompanyFundamentalsResponse,
        )


class AsyncFundamentalsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFundamentalsResourceWithRawResponse:
        return AsyncFundamentalsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFundamentalsResourceWithStreamingResponse:
        return AsyncFundamentalsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyFundamentalsResponse:
        """
        Returns detailed insights on specified publicly traded company's various key
        financial measures or fundamentals like cash per share, dividend, EPS, EBIT etc.
        All values provided in the response are absolute.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. <p>**\\**ids limit** = 50
              per request\\**</p>

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/company-reports/fundamentals",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"ids": ids}, fundamental_retrieve_params.FundamentalRetrieveParams),
            ),
            cast_to=CompanyFundamentalsResponse,
        )


class FundamentalsResourceWithRawResponse:
    def __init__(self, fundamentals: FundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.retrieve = to_raw_response_wrapper(
            fundamentals.retrieve,
        )


class AsyncFundamentalsResourceWithRawResponse:
    def __init__(self, fundamentals: AsyncFundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.retrieve = async_to_raw_response_wrapper(
            fundamentals.retrieve,
        )


class FundamentalsResourceWithStreamingResponse:
    def __init__(self, fundamentals: FundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.retrieve = to_streamed_response_wrapper(
            fundamentals.retrieve,
        )


class AsyncFundamentalsResourceWithStreamingResponse:
    def __init__(self, fundamentals: AsyncFundamentalsResource) -> None:
        self._fundamentals = fundamentals

        self.retrieve = async_to_streamed_response_wrapper(
            fundamentals.retrieve,
        )
