# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import return_list_params, return_create_params
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
from ..types.returns_response import ReturnsResponse

__all__ = ["ReturnsResource", "AsyncReturnsResource"]


class ReturnsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ReturnsResourceWithRawResponse:
        return ReturnsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReturnsResourceWithStreamingResponse:
        return ReturnsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        start_date: str,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        dividend_adjust: Literal["PRICE", "EXDATE", "PAYDATE", "EXDATE_C", "PAYDATE_C"] | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReturnsResponse:
        """Returns for the requested ids and currency for the given dates.

        Depending on the
        input parameters the return data is provided.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. Requests are limited to
              50 IDs.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

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

          dividend_adjust: Controls the dividend reinvestment for the returns calculation.

              - **PRICE** = Price Change - Dividends Excluded.
              - **EXDATE** = Simple Return - Dividends Received on exdate but not reinvested.
              - **PAYDATE** = Simple Return - Dividends Received on paydate but not
                reinvested.
              - **EXDATE_C** = Compound Return - Dividends reinvested on exdate.
              - **PAYDATE_C** = Compound Return - Dividends reinvested on paydate.

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **AD** = Actual Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **M** = Monthly, based on the last trading day of the month.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Actual Quarterly
              - **CQ** = Quarterly based on the last trading day of the calendar quarter
                (March, June, September, or December).
              - **ASA** = Actual Semi-annual
              - **CSA** = Calendar Semi-annual
              - **AY** = Actual Annual, based on the start date.
              - **CY** = Calendar Annual, based on the last trading day of the calendar year.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-global-prices/v1/returns",
            body=maybe_transform(
                {
                    "ids": ids,
                    "start_date": start_date,
                    "batch": batch,
                    "currency": currency,
                    "dividend_adjust": dividend_adjust,
                    "end_date": end_date,
                    "frequency": frequency,
                },
                return_create_params.ReturnCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReturnsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        start_date: str,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        dividend_adjust: Literal["PRICE", "EXDATE", "PAYDATE", "EXDATE_C", "PAYDATE_C"] | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReturnsResponse:
        """Returns for the requested ids and currency for the given dates.

        Depending on the
        input parameters the return data is provided.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** = 50
              per both non-batch request and batch request*</p> *<p>Make note, GET Method URL
              request lines are also limited to a total length of 8192 bytes (8KB). In cases
              where the service allows for thousands of ids, which may lead to exceeding this
              request line limit of 8KB, it's advised for any requests with large request
              lines to be requested through the respective "POST" method.</p>\\**

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. The
              input start date must be before the input end date. Future dates (T+1) are not
              accepted in this endpoint.

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

          dividend_adjust: Controls the dividend reinvestment for the returns calculation.

              - **PRICE** = Price Change - Dividends Excluded.
              - **EXDATE** = Simple Return - Dividends Received on exdate but not reinvested.
              - **PAYDATE** = Simple Return - Dividends Received on paydate but not
                reinvested.
              - **EXDATE_C** = Compound Return - Dividends reinvested on exdate.
              - **PAYDATE_C** = Compound Return - Dividends reinvested on paydate.

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. The
              input end date must be after the input start date. Future dates (T+1) are not
              accepted in this endpoint.

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **AD** = Actual Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **M** = Monthly, based on the last trading day of the month.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Actual Quarterly
              - **CQ** = Quarterly based on the last trading day of the calendar quarter
                (March, June, September, or December).
              - **ASA** = Actual Semi-annual
              - **CSA** = Calendar Semi-annual
              - **AY** = Actual Annual, based on the start date.
              - **CY** = Calendar Annual, based on the last trading day of the calendar year.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-global-prices/v1/returns",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "start_date": start_date,
                        "batch": batch,
                        "currency": currency,
                        "dividend_adjust": dividend_adjust,
                        "end_date": end_date,
                        "frequency": frequency,
                    },
                    return_list_params.ReturnListParams,
                ),
            ),
            cast_to=ReturnsResponse,
        )


class AsyncReturnsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncReturnsResourceWithRawResponse:
        return AsyncReturnsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReturnsResourceWithStreamingResponse:
        return AsyncReturnsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        start_date: str,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        dividend_adjust: Literal["PRICE", "EXDATE", "PAYDATE", "EXDATE_C", "PAYDATE_C"] | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReturnsResponse:
        """Returns for the requested ids and currency for the given dates.

        Depending on the
        input parameters the return data is provided.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. Requests are limited to
              50 IDs.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

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

          dividend_adjust: Controls the dividend reinvestment for the returns calculation.

              - **PRICE** = Price Change - Dividends Excluded.
              - **EXDATE** = Simple Return - Dividends Received on exdate but not reinvested.
              - **PAYDATE** = Simple Return - Dividends Received on paydate but not
                reinvested.
              - **EXDATE_C** = Compound Return - Dividends reinvested on exdate.
              - **PAYDATE_C** = Compound Return - Dividends reinvested on paydate.

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **AD** = Actual Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **M** = Monthly, based on the last trading day of the month.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Actual Quarterly
              - **CQ** = Quarterly based on the last trading day of the calendar quarter
                (March, June, September, or December).
              - **ASA** = Actual Semi-annual
              - **CSA** = Calendar Semi-annual
              - **AY** = Actual Annual, based on the start date.
              - **CY** = Calendar Annual, based on the last trading day of the calendar year.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-global-prices/v1/returns",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "start_date": start_date,
                    "batch": batch,
                    "currency": currency,
                    "dividend_adjust": dividend_adjust,
                    "end_date": end_date,
                    "frequency": frequency,
                },
                return_create_params.ReturnCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReturnsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        start_date: str,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        dividend_adjust: Literal["PRICE", "EXDATE", "PAYDATE", "EXDATE_C", "PAYDATE_C"] | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReturnsResponse:
        """Returns for the requested ids and currency for the given dates.

        Depending on the
        input parameters the return data is provided.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** = 50
              per both non-batch request and batch request*</p> *<p>Make note, GET Method URL
              request lines are also limited to a total length of 8192 bytes (8KB). In cases
              where the service allows for thousands of ids, which may lead to exceeding this
              request line limit of 8KB, it's advised for any requests with large request
              lines to be requested through the respective "POST" method.</p>\\**

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. The
              input start date must be before the input end date. Future dates (T+1) are not
              accepted in this endpoint.

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

          dividend_adjust: Controls the dividend reinvestment for the returns calculation.

              - **PRICE** = Price Change - Dividends Excluded.
              - **EXDATE** = Simple Return - Dividends Received on exdate but not reinvested.
              - **PAYDATE** = Simple Return - Dividends Received on paydate but not
                reinvested.
              - **EXDATE_C** = Compound Return - Dividends reinvested on exdate.
              - **PAYDATE_C** = Compound Return - Dividends reinvested on paydate.

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. The
              input end date must be after the input start date. Future dates (T+1) are not
              accepted in this endpoint.

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **AD** = Actual Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **M** = Monthly, based on the last trading day of the month.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Actual Quarterly
              - **CQ** = Quarterly based on the last trading day of the calendar quarter
                (March, June, September, or December).
              - **ASA** = Actual Semi-annual
              - **CSA** = Calendar Semi-annual
              - **AY** = Actual Annual, based on the start date.
              - **CY** = Calendar Annual, based on the last trading day of the calendar year.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-global-prices/v1/returns",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "start_date": start_date,
                        "batch": batch,
                        "currency": currency,
                        "dividend_adjust": dividend_adjust,
                        "end_date": end_date,
                        "frequency": frequency,
                    },
                    return_list_params.ReturnListParams,
                ),
            ),
            cast_to=ReturnsResponse,
        )


class ReturnsResourceWithRawResponse:
    def __init__(self, returns: ReturnsResource) -> None:
        self._returns = returns

        self.create = to_raw_response_wrapper(
            returns.create,
        )
        self.list = to_raw_response_wrapper(
            returns.list,
        )


class AsyncReturnsResourceWithRawResponse:
    def __init__(self, returns: AsyncReturnsResource) -> None:
        self._returns = returns

        self.create = async_to_raw_response_wrapper(
            returns.create,
        )
        self.list = async_to_raw_response_wrapper(
            returns.list,
        )


class ReturnsResourceWithStreamingResponse:
    def __init__(self, returns: ReturnsResource) -> None:
        self._returns = returns

        self.create = to_streamed_response_wrapper(
            returns.create,
        )
        self.list = to_streamed_response_wrapper(
            returns.list,
        )


class AsyncReturnsResourceWithStreamingResponse:
    def __init__(self, returns: AsyncReturnsResource) -> None:
        self._returns = returns

        self.create = async_to_streamed_response_wrapper(
            returns.create,
        )
        self.list = async_to_streamed_response_wrapper(
            returns.list,
        )
