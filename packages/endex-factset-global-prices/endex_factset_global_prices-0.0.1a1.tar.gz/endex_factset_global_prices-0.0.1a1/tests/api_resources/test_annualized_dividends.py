# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_prices import EndexFactsetGlobalPrices, AsyncEndexFactsetGlobalPrices
from endex_factset_global_prices.types import (
    AnnualizedDividendResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAnnualizedDividends:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetGlobalPrices) -> None:
        annualized_dividend = client.annualized_dividends.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        annualized_dividend = client.annualized_dividends.create(
            ids=["AAPL-US"],
            batch="Y",
            currency="USD",
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.annualized_dividends.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        annualized_dividend = response.parse()
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        with client.annualized_dividends.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            annualized_dividend = response.parse()
            assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetGlobalPrices) -> None:
        annualized_dividend = client.annualized_dividends.list(
            ids=["string", "string", "string"],
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        annualized_dividend = client.annualized_dividends.list(
            ids=["string", "string", "string"],
            batch="Y",
            currency="currency",
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.annualized_dividends.with_raw_response.list(
            ids=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        annualized_dividend = response.parse()
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        with client.annualized_dividends.with_streaming_response.list(
            ids=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            annualized_dividend = response.parse()
            assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAnnualizedDividends:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        annualized_dividend = await async_client.annualized_dividends.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        annualized_dividend = await async_client.annualized_dividends.create(
            ids=["AAPL-US"],
            batch="Y",
            currency="USD",
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.annualized_dividends.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        annualized_dividend = await response.parse()
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.annualized_dividends.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            annualized_dividend = await response.parse()
            assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        annualized_dividend = await async_client.annualized_dividends.list(
            ids=["string", "string", "string"],
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        annualized_dividend = await async_client.annualized_dividends.list(
            ids=["string", "string", "string"],
            batch="Y",
            currency="currency",
        )
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.annualized_dividends.with_raw_response.list(
            ids=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        annualized_dividend = await response.parse()
        assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.annualized_dividends.with_streaming_response.list(
            ids=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            annualized_dividend = await response.parse()
            assert_matches_type(AnnualizedDividendResponse, annualized_dividend, path=["response"])

        assert cast(Any, response.is_closed) is True
