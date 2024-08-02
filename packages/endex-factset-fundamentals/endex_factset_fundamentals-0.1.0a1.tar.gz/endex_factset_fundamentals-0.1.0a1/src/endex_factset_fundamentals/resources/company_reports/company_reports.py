# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .profile import (
    ProfileResource,
    AsyncProfileResource,
    ProfileResourceWithRawResponse,
    AsyncProfileResourceWithRawResponse,
    ProfileResourceWithStreamingResponse,
    AsyncProfileResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .fundamentals import (
    FundamentalsResource,
    AsyncFundamentalsResource,
    FundamentalsResourceWithRawResponse,
    AsyncFundamentalsResourceWithRawResponse,
    FundamentalsResourceWithStreamingResponse,
    AsyncFundamentalsResourceWithStreamingResponse,
)
from .financial_statement import (
    FinancialStatementResource,
    AsyncFinancialStatementResource,
    FinancialStatementResourceWithRawResponse,
    AsyncFinancialStatementResourceWithRawResponse,
    FinancialStatementResourceWithStreamingResponse,
    AsyncFinancialStatementResourceWithStreamingResponse,
)

__all__ = ["CompanyReportsResource", "AsyncCompanyReportsResource"]


class CompanyReportsResource(SyncAPIResource):
    @cached_property
    def financial_statement(self) -> FinancialStatementResource:
        return FinancialStatementResource(self._client)

    @cached_property
    def profile(self) -> ProfileResource:
        return ProfileResource(self._client)

    @cached_property
    def fundamentals(self) -> FundamentalsResource:
        return FundamentalsResource(self._client)

    @cached_property
    def with_raw_response(self) -> CompanyReportsResourceWithRawResponse:
        return CompanyReportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompanyReportsResourceWithStreamingResponse:
        return CompanyReportsResourceWithStreamingResponse(self)


class AsyncCompanyReportsResource(AsyncAPIResource):
    @cached_property
    def financial_statement(self) -> AsyncFinancialStatementResource:
        return AsyncFinancialStatementResource(self._client)

    @cached_property
    def profile(self) -> AsyncProfileResource:
        return AsyncProfileResource(self._client)

    @cached_property
    def fundamentals(self) -> AsyncFundamentalsResource:
        return AsyncFundamentalsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCompanyReportsResourceWithRawResponse:
        return AsyncCompanyReportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompanyReportsResourceWithStreamingResponse:
        return AsyncCompanyReportsResourceWithStreamingResponse(self)


class CompanyReportsResourceWithRawResponse:
    def __init__(self, company_reports: CompanyReportsResource) -> None:
        self._company_reports = company_reports

    @cached_property
    def financial_statement(self) -> FinancialStatementResourceWithRawResponse:
        return FinancialStatementResourceWithRawResponse(self._company_reports.financial_statement)

    @cached_property
    def profile(self) -> ProfileResourceWithRawResponse:
        return ProfileResourceWithRawResponse(self._company_reports.profile)

    @cached_property
    def fundamentals(self) -> FundamentalsResourceWithRawResponse:
        return FundamentalsResourceWithRawResponse(self._company_reports.fundamentals)


class AsyncCompanyReportsResourceWithRawResponse:
    def __init__(self, company_reports: AsyncCompanyReportsResource) -> None:
        self._company_reports = company_reports

    @cached_property
    def financial_statement(self) -> AsyncFinancialStatementResourceWithRawResponse:
        return AsyncFinancialStatementResourceWithRawResponse(self._company_reports.financial_statement)

    @cached_property
    def profile(self) -> AsyncProfileResourceWithRawResponse:
        return AsyncProfileResourceWithRawResponse(self._company_reports.profile)

    @cached_property
    def fundamentals(self) -> AsyncFundamentalsResourceWithRawResponse:
        return AsyncFundamentalsResourceWithRawResponse(self._company_reports.fundamentals)


class CompanyReportsResourceWithStreamingResponse:
    def __init__(self, company_reports: CompanyReportsResource) -> None:
        self._company_reports = company_reports

    @cached_property
    def financial_statement(self) -> FinancialStatementResourceWithStreamingResponse:
        return FinancialStatementResourceWithStreamingResponse(self._company_reports.financial_statement)

    @cached_property
    def profile(self) -> ProfileResourceWithStreamingResponse:
        return ProfileResourceWithStreamingResponse(self._company_reports.profile)

    @cached_property
    def fundamentals(self) -> FundamentalsResourceWithStreamingResponse:
        return FundamentalsResourceWithStreamingResponse(self._company_reports.fundamentals)


class AsyncCompanyReportsResourceWithStreamingResponse:
    def __init__(self, company_reports: AsyncCompanyReportsResource) -> None:
        self._company_reports = company_reports

    @cached_property
    def financial_statement(self) -> AsyncFinancialStatementResourceWithStreamingResponse:
        return AsyncFinancialStatementResourceWithStreamingResponse(self._company_reports.financial_statement)

    @cached_property
    def profile(self) -> AsyncProfileResourceWithStreamingResponse:
        return AsyncProfileResourceWithStreamingResponse(self._company_reports.profile)

    @cached_property
    def fundamentals(self) -> AsyncFundamentalsResourceWithStreamingResponse:
        return AsyncFundamentalsResourceWithStreamingResponse(self._company_reports.fundamentals)
