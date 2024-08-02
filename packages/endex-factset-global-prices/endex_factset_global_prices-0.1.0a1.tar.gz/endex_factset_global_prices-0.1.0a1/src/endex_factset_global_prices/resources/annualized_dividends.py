# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import annualized_dividend_list_params, annualized_dividend_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.annualized_dividend_response import AnnualizedDividendResponse

__all__ = ["AnnualizedDividendsResource", "AsyncAnnualizedDividendsResource"]


class AnnualizedDividendsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnnualizedDividendsResourceWithRawResponse:
        return AnnualizedDividendsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnnualizedDividendsResourceWithStreamingResponse:
        return AnnualizedDividendsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnnualizedDividendResponse:
        """Gets the Annualized dividend of the latest reported dividend.

        The annualized
        dividend calculations does not involve cancelled dividends.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. Requests are limited to
              50 IDs.

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond back with an HTTP Status Code of 202. Once a batch request is
              submitted, use batch status to see if the job has been completed. Once
              completed, retrieve the results of the request via batch-result. When using
              Batch, ids limit is increased to 10000 ids per request, though limits on query
              string via GET method still apply. It's advised to submit large lists of ids via
              POST method. Please note that the number of unique currencies present in the
              requested ids is limited to 50 per request.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-global-prices/v1/annualized-dividends",
            body=maybe_transform(
                {
                    "ids": ids,
                    "batch": batch,
                    "currency": currency,
                },
                annualized_dividend_create_params.AnnualizedDividendCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnnualizedDividendResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnnualizedDividendResponse:
        """Gets the Annualized dividend of the latest reported dividend.

        The annualized
        dividend calculations does not involve cancelled dividends.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** = 50
              per both non-batch request and batch request*</p> *<p>Make note, GET Method URL
              request lines are also limited to a total length of 8192 bytes (8KB). In cases
              where the service allows for thousands of ids, which may lead to exceeding this
              request line limit of 8KB, it's advised for any requests with large request
              lines to be requested through the respective "POST" method.</p>\\**

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond with an HTTP Status Code of 202. Once a batch request is submitted,
              use batch status to see if the job has been completed. Once completed, retrieve
              the results of the request via batch-result. When using Batch, ids limit is
              increased to 10000 ids per request, though limits on query string via GET method
              still apply. It's advised to submit large lists of ids via POST method.
              <B>Please note that the number of unique currencies present in the requested ids
              is limited to 50 per request.</B>

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-global-prices/v1/annualized-dividends",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "batch": batch,
                        "currency": currency,
                    },
                    annualized_dividend_list_params.AnnualizedDividendListParams,
                ),
            ),
            cast_to=AnnualizedDividendResponse,
        )


class AsyncAnnualizedDividendsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnnualizedDividendsResourceWithRawResponse:
        return AsyncAnnualizedDividendsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnnualizedDividendsResourceWithStreamingResponse:
        return AsyncAnnualizedDividendsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnnualizedDividendResponse:
        """Gets the Annualized dividend of the latest reported dividend.

        The annualized
        dividend calculations does not involve cancelled dividends.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. Requests are limited to
              50 IDs.

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond back with an HTTP Status Code of 202. Once a batch request is
              submitted, use batch status to see if the job has been completed. Once
              completed, retrieve the results of the request via batch-result. When using
              Batch, ids limit is increased to 10000 ids per request, though limits on query
              string via GET method still apply. It's advised to submit large lists of ids via
              POST method. Please note that the number of unique currencies present in the
              requested ids is limited to 50 per request.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-global-prices/v1/annualized-dividends",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "batch": batch,
                    "currency": currency,
                },
                annualized_dividend_create_params.AnnualizedDividendCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnnualizedDividendResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnnualizedDividendResponse:
        """Gets the Annualized dividend of the latest reported dividend.

        The annualized
        dividend calculations does not involve cancelled dividends.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** = 50
              per both non-batch request and batch request*</p> *<p>Make note, GET Method URL
              request lines are also limited to a total length of 8192 bytes (8KB). In cases
              where the service allows for thousands of ids, which may lead to exceeding this
              request line limit of 8KB, it's advised for any requests with large request
              lines to be requested through the respective "POST" method.</p>\\**

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond with an HTTP Status Code of 202. Once a batch request is submitted,
              use batch status to see if the job has been completed. Once completed, retrieve
              the results of the request via batch-result. When using Batch, ids limit is
              increased to 10000 ids per request, though limits on query string via GET method
              still apply. It's advised to submit large lists of ids via POST method.
              <B>Please note that the number of unique currencies present in the requested ids
              is limited to 50 per request.</B>

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-global-prices/v1/annualized-dividends",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "batch": batch,
                        "currency": currency,
                    },
                    annualized_dividend_list_params.AnnualizedDividendListParams,
                ),
            ),
            cast_to=AnnualizedDividendResponse,
        )


class AnnualizedDividendsResourceWithRawResponse:
    def __init__(self, annualized_dividends: AnnualizedDividendsResource) -> None:
        self._annualized_dividends = annualized_dividends

        self.create = to_raw_response_wrapper(
            annualized_dividends.create,
        )
        self.list = to_raw_response_wrapper(
            annualized_dividends.list,
        )


class AsyncAnnualizedDividendsResourceWithRawResponse:
    def __init__(self, annualized_dividends: AsyncAnnualizedDividendsResource) -> None:
        self._annualized_dividends = annualized_dividends

        self.create = async_to_raw_response_wrapper(
            annualized_dividends.create,
        )
        self.list = async_to_raw_response_wrapper(
            annualized_dividends.list,
        )


class AnnualizedDividendsResourceWithStreamingResponse:
    def __init__(self, annualized_dividends: AnnualizedDividendsResource) -> None:
        self._annualized_dividends = annualized_dividends

        self.create = to_streamed_response_wrapper(
            annualized_dividends.create,
        )
        self.list = to_streamed_response_wrapper(
            annualized_dividends.list,
        )


class AsyncAnnualizedDividendsResourceWithStreamingResponse:
    def __init__(self, annualized_dividends: AsyncAnnualizedDividendsResource) -> None:
        self._annualized_dividends = annualized_dividends

        self.create = async_to_streamed_response_wrapper(
            annualized_dividends.create,
        )
        self.list = async_to_streamed_response_wrapper(
            annualized_dividends.list,
        )
