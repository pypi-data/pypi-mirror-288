# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_fundamentals import EndexFactsetFundamentals, AsyncEndexFactsetFundamentals
from endex_factset_fundamentals.types import SegmentsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSegments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetFundamentals) -> None:
        segment = client.segments.create(
            data={
                "ids": ["AAPL-US"],
                "metrics": "SALES",
            },
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetFundamentals) -> None:
        segment = client.segments.create(
            data={
                "ids": ["AAPL-US"],
                "periodicity": "ANN",
                "fiscal_period": {
                    "start": "2012-01-01",
                    "end": "2014-01-01",
                },
                "metrics": "SALES",
                "segment_type": "BUS",
                "batch": "Y",
            },
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetFundamentals) -> None:
        response = client.segments.with_raw_response.create(
            data={
                "ids": ["AAPL-US"],
                "metrics": "SALES",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        segment = response.parse()
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetFundamentals) -> None:
        with client.segments.with_streaming_response.create(
            data={
                "ids": ["AAPL-US"],
                "metrics": "SALES",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            segment = response.parse()
            assert_matches_type(SegmentsResponse, segment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetFundamentals) -> None:
        segment = client.segments.list(
            ids=["string", "string", "string"],
            metrics="SALES",
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetFundamentals) -> None:
        segment = client.segments.list(
            ids=["string", "string", "string"],
            metrics="SALES",
            batch="Y",
            fiscal_period_end="2018-03-01",
            fiscal_period_start="2017-09-01",
            periodicity="ANN",
            segment_type="BUS",
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetFundamentals) -> None:
        response = client.segments.with_raw_response.list(
            ids=["string", "string", "string"],
            metrics="SALES",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        segment = response.parse()
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetFundamentals) -> None:
        with client.segments.with_streaming_response.list(
            ids=["string", "string", "string"],
            metrics="SALES",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            segment = response.parse()
            assert_matches_type(SegmentsResponse, segment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSegments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        segment = await async_client.segments.create(
            data={
                "ids": ["AAPL-US"],
                "metrics": "SALES",
            },
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        segment = await async_client.segments.create(
            data={
                "ids": ["AAPL-US"],
                "periodicity": "ANN",
                "fiscal_period": {
                    "start": "2012-01-01",
                    "end": "2014-01-01",
                },
                "metrics": "SALES",
                "segment_type": "BUS",
                "batch": "Y",
            },
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        response = await async_client.segments.with_raw_response.create(
            data={
                "ids": ["AAPL-US"],
                "metrics": "SALES",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        segment = await response.parse()
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        async with async_client.segments.with_streaming_response.create(
            data={
                "ids": ["AAPL-US"],
                "metrics": "SALES",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            segment = await response.parse()
            assert_matches_type(SegmentsResponse, segment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        segment = await async_client.segments.list(
            ids=["string", "string", "string"],
            metrics="SALES",
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        segment = await async_client.segments.list(
            ids=["string", "string", "string"],
            metrics="SALES",
            batch="Y",
            fiscal_period_end="2018-03-01",
            fiscal_period_start="2017-09-01",
            periodicity="ANN",
            segment_type="BUS",
        )
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        response = await async_client.segments.with_raw_response.list(
            ids=["string", "string", "string"],
            metrics="SALES",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        segment = await response.parse()
        assert_matches_type(SegmentsResponse, segment, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        async with async_client.segments.with_streaming_response.list(
            ids=["string", "string", "string"],
            metrics="SALES",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            segment = await response.parse()
            assert_matches_type(SegmentsResponse, segment, path=["response"])

        assert cast(Any, response.is_closed) is True
