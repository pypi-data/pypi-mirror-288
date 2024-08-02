# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_fundamentals import EndexFactsetFundamentals, AsyncEndexFactsetFundamentals
from endex_factset_fundamentals.types.company_reports import ProfileResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProfile:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetFundamentals) -> None:
        profile = client.company_reports.profile.retrieve(
            ids=["string"],
        )
        assert_matches_type(ProfileResponse, profile, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetFundamentals) -> None:
        response = client.company_reports.profile.with_raw_response.retrieve(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(ProfileResponse, profile, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetFundamentals) -> None:
        with client.company_reports.profile.with_streaming_response.retrieve(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(ProfileResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncProfile:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        profile = await async_client.company_reports.profile.retrieve(
            ids=["string"],
        )
        assert_matches_type(ProfileResponse, profile, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        response = await async_client.company_reports.profile.with_raw_response.retrieve(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(ProfileResponse, profile, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetFundamentals) -> None:
        async with async_client.company_reports.profile.with_streaming_response.retrieve(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(ProfileResponse, profile, path=["response"])

        assert cast(Any, response.is_closed) is True
