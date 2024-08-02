# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_fundamentals import EndexFactsetFundamentals, AsyncEndexFactsetFundamentals
from endex_factset_fundamentals.types.company_reports import FinancialResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFinancialStatement:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetFundamentals) -> None:
        financial_statement = client.company_reports.financial_statement.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
        )
        assert_matches_type(FinancialResponse, financial_statement, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetFundamentals) -> None:
        financial_statement = client.company_reports.financial_statement.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
            limit=0,
            update_type="RP",
        )
        assert_matches_type(FinancialResponse, financial_statement, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetFundamentals) -> None:
        response = client.company_reports.financial_statement.with_raw_response.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        financial_statement = response.parse()
        assert_matches_type(FinancialResponse, financial_statement, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetFundamentals) -> None:
        with client.company_reports.financial_statement.with_streaming_response.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            financial_statement = response.parse()
            assert_matches_type(FinancialResponse, financial_statement, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFinancialStatement:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        financial_statement = await async_client.company_reports.financial_statement.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
        )
        assert_matches_type(FinancialResponse, financial_statement, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        financial_statement = await async_client.company_reports.financial_statement.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
            limit=0,
            update_type="RP",
        )
        assert_matches_type(FinancialResponse, financial_statement, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        response = await async_client.company_reports.financial_statement.with_raw_response.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        financial_statement = await response.parse()
        assert_matches_type(FinancialResponse, financial_statement, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        async with async_client.company_reports.financial_statement.with_streaming_response.retrieve(
            id="IBM-US",
            periodicity="ANN",
            statement_type="BS",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            financial_statement = await response.parse()
            assert_matches_type(FinancialResponse, financial_statement, path=["response"])

        assert cast(Any, response.is_closed) is True
