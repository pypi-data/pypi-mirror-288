# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

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
from ...types.company_reports import financial_statement_retrieve_params
from ...types.company_reports.financial_response import FinancialResponse

__all__ = ["FinancialStatementResource", "AsyncFinancialStatementResource"]


class FinancialStatementResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FinancialStatementResourceWithRawResponse:
        return FinancialStatementResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FinancialStatementResourceWithStreamingResponse:
        return FinancialStatementResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        id: str,
        periodicity: Literal["ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "YTD"],
        statement_type: Literal["BS", "CF", "IS"],
        limit: int | NotGiven = NOT_GIVEN,
        update_type: Literal["RP", "RF"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FinancialResponse:
        """
        Returns company financial data (preliminary or final) for specified security and
        statement type (income statement, balance sheet, cash flow), for various fiscal
        reporting periods. All values provided in the response are absolute.

        Args:
          id: The requested security identifier. Accepted ID types include Market Ticker,
              SEDOL, ISIN, CUSIP, or FactSet Permanent Id.

          periodicity: Periodicity or frequency of the fiscal periods, where

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

          statement_type: The type of financial statement being requested.

          limit: The time period for the returned data. Within range of 1 to 100. If not
              specified default will be 4.

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
            "/company-reports/financial-statement",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "periodicity": periodicity,
                        "statement_type": statement_type,
                        "limit": limit,
                        "update_type": update_type,
                    },
                    financial_statement_retrieve_params.FinancialStatementRetrieveParams,
                ),
            ),
            cast_to=FinancialResponse,
        )


class AsyncFinancialStatementResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFinancialStatementResourceWithRawResponse:
        return AsyncFinancialStatementResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFinancialStatementResourceWithStreamingResponse:
        return AsyncFinancialStatementResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        id: str,
        periodicity: Literal["ANN", "ANN_R", "QTR", "QTR_R", "SEMI", "SEMI_R", "LTM", "YTD"],
        statement_type: Literal["BS", "CF", "IS"],
        limit: int | NotGiven = NOT_GIVEN,
        update_type: Literal["RP", "RF"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FinancialResponse:
        """
        Returns company financial data (preliminary or final) for specified security and
        statement type (income statement, balance sheet, cash flow), for various fiscal
        reporting periods. All values provided in the response are absolute.

        Args:
          id: The requested security identifier. Accepted ID types include Market Ticker,
              SEDOL, ISIN, CUSIP, or FactSet Permanent Id.

          periodicity: Periodicity or frequency of the fiscal periods, where

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

          statement_type: The type of financial statement being requested.

          limit: The time period for the returned data. Within range of 1 to 100. If not
              specified default will be 4.

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
            "/company-reports/financial-statement",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "id": id,
                        "periodicity": periodicity,
                        "statement_type": statement_type,
                        "limit": limit,
                        "update_type": update_type,
                    },
                    financial_statement_retrieve_params.FinancialStatementRetrieveParams,
                ),
            ),
            cast_to=FinancialResponse,
        )


class FinancialStatementResourceWithRawResponse:
    def __init__(self, financial_statement: FinancialStatementResource) -> None:
        self._financial_statement = financial_statement

        self.retrieve = to_raw_response_wrapper(
            financial_statement.retrieve,
        )


class AsyncFinancialStatementResourceWithRawResponse:
    def __init__(self, financial_statement: AsyncFinancialStatementResource) -> None:
        self._financial_statement = financial_statement

        self.retrieve = async_to_raw_response_wrapper(
            financial_statement.retrieve,
        )


class FinancialStatementResourceWithStreamingResponse:
    def __init__(self, financial_statement: FinancialStatementResource) -> None:
        self._financial_statement = financial_statement

        self.retrieve = to_streamed_response_wrapper(
            financial_statement.retrieve,
        )


class AsyncFinancialStatementResourceWithStreamingResponse:
    def __init__(self, financial_statement: AsyncFinancialStatementResource) -> None:
        self._financial_statement = financial_statement

        self.retrieve = async_to_streamed_response_wrapper(
            financial_statement.retrieve,
        )
