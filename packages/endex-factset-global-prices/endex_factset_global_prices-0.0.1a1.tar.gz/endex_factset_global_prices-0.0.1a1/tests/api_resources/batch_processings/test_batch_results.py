# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_prices import EndexFactsetGlobalPrices, AsyncEndexFactsetGlobalPrices
from endex_factset_global_prices.types.batch_processings import BatchResultResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatchResults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetGlobalPrices) -> None:
        batch_result = client.batch_processings.batch_results.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchResultResponse, batch_result, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetGlobalPrices) -> None:
        response = client.batch_processings.batch_results.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_result = response.parse()
        assert_matches_type(BatchResultResponse, batch_result, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetGlobalPrices) -> None:
        with client.batch_processings.batch_results.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_result = response.parse()
            assert_matches_type(BatchResultResponse, batch_result, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBatchResults:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        batch_result = await async_client.batch_processings.batch_results.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BatchResultResponse, batch_result, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        response = await async_client.batch_processings.batch_results.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_result = await response.parse()
        assert_matches_type(BatchResultResponse, batch_result, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetGlobalPrices) -> None:
        async with async_client.batch_processings.batch_results.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_result = await response.parse()
            assert_matches_type(BatchResultResponse, batch_result, path=["response"])

        assert cast(Any, response.is_closed) is True
