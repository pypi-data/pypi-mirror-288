# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_prices import EndexFactsetGlobalPrices, AsyncEndexFactsetGlobalPrices
from endex_factset_global_prices.types import (
    CorporateActionsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCorporateActions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetGlobalPrices) -> None:
        corporate_action = client.corporate_actions.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        corporate_action = client.corporate_actions.create(
            ids=["AAPL-US"],
            batch="Y",
            cancelled_dividend="exclude",
            currency="USD",
            end_date="2021-06-30",
            event_category="CASH_DIVS",
            fields=["eventId", "eventTypeDesc", "recordDate", "payDate", "currency"],
            start_date="2020-06-30",
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.corporate_actions.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        corporate_action = response.parse()
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetGlobalPrices) -> None:
        with client.corporate_actions.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            corporate_action = response.parse()
            assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetGlobalPrices) -> None:
        corporate_action = client.corporate_actions.list(
            ids=["string", "string", "string"],
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetGlobalPrices) -> None:
        corporate_action = client.corporate_actions.list(
            ids=["string", "string", "string"],
            batch="Y",
            cancelled_dividend="include",
            currency="currency",
            end_date="endDate",
            event_category="CASH_DIVS",
            fields=["string", "string", "string"],
            start_date="startDate",
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.corporate_actions.with_raw_response.list(
            ids=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        corporate_action = response.parse()
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetGlobalPrices) -> None:
        with client.corporate_actions.with_streaming_response.list(
            ids=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            corporate_action = response.parse()
            assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCorporateActions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        corporate_action = await async_client.corporate_actions.create(
            ids=["AAPL-US"],
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        corporate_action = await async_client.corporate_actions.create(
            ids=["AAPL-US"],
            batch="Y",
            cancelled_dividend="exclude",
            currency="USD",
            end_date="2021-06-30",
            event_category="CASH_DIVS",
            fields=["eventId", "eventTypeDesc", "recordDate", "payDate", "currency"],
            start_date="2020-06-30",
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.corporate_actions.with_raw_response.create(
            ids=["AAPL-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        corporate_action = await response.parse()
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.corporate_actions.with_streaming_response.create(
            ids=["AAPL-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            corporate_action = await response.parse()
            assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        corporate_action = await async_client.corporate_actions.list(
            ids=["string", "string", "string"],
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        corporate_action = await async_client.corporate_actions.list(
            ids=["string", "string", "string"],
            batch="Y",
            cancelled_dividend="include",
            currency="currency",
            end_date="endDate",
            event_category="CASH_DIVS",
            fields=["string", "string", "string"],
            start_date="startDate",
        )
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.corporate_actions.with_raw_response.list(
            ids=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        corporate_action = await response.parse()
        assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.corporate_actions.with_streaming_response.list(
            ids=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            corporate_action = await response.parse()
            assert_matches_type(CorporateActionsResponse, corporate_action, path=["response"])

        assert cast(Any, response.is_closed) is True
