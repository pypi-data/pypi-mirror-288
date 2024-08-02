# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_prices import EndexFactsetGlobalPrices, AsyncEndexFactsetGlobalPrices
from endex_factset_global_prices.types import ReturnsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReturns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetGlobalPrices) -> None:
        return_ = client.returns.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        return_ = client.returns.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
            batch="Y",
            currency="USD",
            dividend_adjust="EXDATE_C",
            end_date="2021-06-30",
            frequency="M",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.returns.with_raw_response.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        return_ = response.parse()
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        with client.returns.with_streaming_response.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            return_ = response.parse()
            assert_matches_type(ReturnsResponse, return_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetGlobalPrices) -> None:
        return_ = client.returns.list(
            ids=["string", "string", "string"],
            start_date="startDate",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        return_ = client.returns.list(
            ids=["string", "string", "string"],
            start_date="startDate",
            batch="Y",
            currency="currency",
            dividend_adjust="PRICE",
            end_date="endDate",
            frequency="D",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.returns.with_raw_response.list(
            ids=["string", "string", "string"],
            start_date="startDate",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        return_ = response.parse()
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        with client.returns.with_streaming_response.list(
            ids=["string", "string", "string"],
            start_date="startDate",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            return_ = response.parse()
            assert_matches_type(ReturnsResponse, return_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncReturns:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        return_ = await async_client.returns.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        return_ = await async_client.returns.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
            batch="Y",
            currency="USD",
            dividend_adjust="EXDATE_C",
            end_date="2021-06-30",
            frequency="M",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.returns.with_raw_response.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        return_ = await response.parse()
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.returns.with_streaming_response.create(
            ids=["AAPL-US"],
            start_date="2020-06-30",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            return_ = await response.parse()
            assert_matches_type(ReturnsResponse, return_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        return_ = await async_client.returns.list(
            ids=["string", "string", "string"],
            start_date="startDate",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        return_ = await async_client.returns.list(
            ids=["string", "string", "string"],
            start_date="startDate",
            batch="Y",
            currency="currency",
            dividend_adjust="PRICE",
            end_date="endDate",
            frequency="D",
        )
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.returns.with_raw_response.list(
            ids=["string", "string", "string"],
            start_date="startDate",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        return_ = await response.parse()
        assert_matches_type(ReturnsResponse, return_, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.returns.with_streaming_response.list(
            ids=["string", "string", "string"],
            start_date="startDate",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            return_ = await response.parse()
            assert_matches_type(ReturnsResponse, return_, path=["response"])

        assert cast(Any, response.is_closed) is True
