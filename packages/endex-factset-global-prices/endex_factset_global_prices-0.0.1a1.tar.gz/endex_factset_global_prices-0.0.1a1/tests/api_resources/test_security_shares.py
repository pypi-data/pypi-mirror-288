# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_prices import EndexFactsetGlobalPrices, AsyncEndexFactsetGlobalPrices
from endex_factset_global_prices.types import (
    SharesOutstandingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSecurityShares:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetGlobalPrices) -> None:
        security_share = client.security_shares.create(
            data={"ids": ["FDS-US"]},
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        security_share = client.security_shares.create(
            data={
                "ids": ["FDS-US"],
                "start_date": "2020-06-30",
                "end_date": "2021-06-30",
                "frequency": "M",
                "calendar": "FIVEDAY",
                "batch": "N",
            },
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.security_shares.with_raw_response.create(
            data={"ids": ["FDS-US"]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        security_share = response.parse()
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        with client.security_shares.with_streaming_response.create(
            data={"ids": ["FDS-US"]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            security_share = response.parse()
            assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetGlobalPrices) -> None:
        security_share = client.security_shares.list(
            ids=["string", "string", "string"],
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        security_share = client.security_shares.list(
            ids=["string", "string", "string"],
            batch="Y",
            calendar="FIVEDAY",
            end_date="endDate",
            frequency="D",
            start_date="startDate",
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.security_shares.with_raw_response.list(
            ids=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        security_share = response.parse()
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        with client.security_shares.with_streaming_response.list(
            ids=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            security_share = response.parse()
            assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSecurityShares:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        security_share = await async_client.security_shares.create(
            data={"ids": ["FDS-US"]},
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        security_share = await async_client.security_shares.create(
            data={
                "ids": ["FDS-US"],
                "start_date": "2020-06-30",
                "end_date": "2021-06-30",
                "frequency": "M",
                "calendar": "FIVEDAY",
                "batch": "N",
            },
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.security_shares.with_raw_response.create(
            data={"ids": ["FDS-US"]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        security_share = await response.parse()
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.security_shares.with_streaming_response.create(
            data={"ids": ["FDS-US"]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            security_share = await response.parse()
            assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        security_share = await async_client.security_shares.list(
            ids=["string", "string", "string"],
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        security_share = await async_client.security_shares.list(
            ids=["string", "string", "string"],
            batch="Y",
            calendar="FIVEDAY",
            end_date="endDate",
            frequency="D",
            start_date="startDate",
        )
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.security_shares.with_raw_response.list(
            ids=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        security_share = await response.parse()
        assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.security_shares.with_streaming_response.list(
            ids=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            security_share = await response.parse()
            assert_matches_type(SharesOutstandingResponse, security_share, path=["response"])

        assert cast(Any, response.is_closed) is True
