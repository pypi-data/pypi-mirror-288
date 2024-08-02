# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_fundamentals import EndexFactsetFundamentals, AsyncEndexFactsetFundamentals
from endex_factset_fundamentals.types import (
    BatchResultResponse,
    BatchStatusResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatchProcessing:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_result(self, client: EndexFactsetFundamentals) -> None:
        batch_processing = client.batch_processing.result(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchResultResponse, batch_processing, path=["response"])

    @parametrize
    def test_raw_response_result(self, client: EndexFactsetFundamentals) -> None:
        response = client.batch_processing.with_raw_response.result(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_processing = response.parse()
        assert_matches_type(BatchResultResponse, batch_processing, path=["response"])

    @parametrize
    def test_streaming_response_result(self, client: EndexFactsetFundamentals) -> None:
        with client.batch_processing.with_streaming_response.result(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_processing = response.parse()
            assert_matches_type(BatchResultResponse, batch_processing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_status(self, client: EndexFactsetFundamentals) -> None:
        batch_processing = client.batch_processing.status(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchStatusResponse, batch_processing, path=["response"])

    @parametrize
    def test_raw_response_status(self, client: EndexFactsetFundamentals) -> None:
        response = client.batch_processing.with_raw_response.status(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_processing = response.parse()
        assert_matches_type(BatchStatusResponse, batch_processing, path=["response"])

    @parametrize
    def test_streaming_response_status(self, client: EndexFactsetFundamentals) -> None:
        with client.batch_processing.with_streaming_response.status(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_processing = response.parse()
            assert_matches_type(BatchStatusResponse, batch_processing, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBatchProcessing:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_result(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        batch_processing = await async_client.batch_processing.result(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchResultResponse, batch_processing, path=["response"])

    @parametrize
    async def test_raw_response_result(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        response = await async_client.batch_processing.with_raw_response.result(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_processing = await response.parse()
        assert_matches_type(BatchResultResponse, batch_processing, path=["response"])

    @parametrize
    async def test_streaming_response_result(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        async with async_client.batch_processing.with_streaming_response.result(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_processing = await response.parse()
            assert_matches_type(BatchResultResponse, batch_processing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_status(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        batch_processing = await async_client.batch_processing.status(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchStatusResponse, batch_processing, path=["response"])

    @parametrize
    async def test_raw_response_status(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        response = await async_client.batch_processing.with_raw_response.status(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_processing = await response.parse()
        assert_matches_type(BatchStatusResponse, batch_processing, path=["response"])

    @parametrize
    async def test_streaming_response_status(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        async with async_client.batch_processing.with_streaming_response.status(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_processing = await response.parse()
            assert_matches_type(BatchStatusResponse, batch_processing, path=["response"])

        assert cast(Any, response.is_closed) is True
