# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import security_share_list_params, security_share_create_params
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
from ..types.shares_outstanding_response import SharesOutstandingResponse

__all__ = ["SecuritySharesResource", "AsyncSecuritySharesResource"]


class SecuritySharesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SecuritySharesResourceWithRawResponse:
        return SecuritySharesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SecuritySharesResourceWithStreamingResponse:
        return SecuritySharesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: security_share_create_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SharesOutstandingResponse:
        """Returns security level shares outstanding data for the given ids and dates.

        At
        this time, all values returned are split adjusted.

        Args:
          data: Shares Outstanding Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-global-prices/v1/security-shares",
            body=maybe_transform({"data": data}, security_share_create_params.SecurityShareCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SharesOutstandingResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        calendar: Literal["FIVEDAY", "SEVENDAY", "US"] | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SharesOutstandingResponse:
        """Returns security level shares outstanding data for the given ids and dates.

        At
        this time, all values returned are split adjusted.

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

          calendar: Calendar of data returned. SEVENDAY includes weekends.

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

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. The
              input start date must be before the input end date. Future dates (T+1) are not
              accepted in this endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-global-prices/v1/security-shares",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "batch": batch,
                        "calendar": calendar,
                        "end_date": end_date,
                        "frequency": frequency,
                        "start_date": start_date,
                    },
                    security_share_list_params.SecurityShareListParams,
                ),
            ),
            cast_to=SharesOutstandingResponse,
        )


class AsyncSecuritySharesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSecuritySharesResourceWithRawResponse:
        return AsyncSecuritySharesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSecuritySharesResourceWithStreamingResponse:
        return AsyncSecuritySharesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: security_share_create_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SharesOutstandingResponse:
        """Returns security level shares outstanding data for the given ids and dates.

        At
        this time, all values returned are split adjusted.

        Args:
          data: Shares Outstanding Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-global-prices/v1/security-shares",
            body=await async_maybe_transform({"data": data}, security_share_create_params.SecurityShareCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SharesOutstandingResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        calendar: Literal["FIVEDAY", "SEVENDAY", "US"] | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SharesOutstandingResponse:
        """Returns security level shares outstanding data for the given ids and dates.

        At
        this time, all values returned are split adjusted.

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

          calendar: Calendar of data returned. SEVENDAY includes weekends.

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

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. The
              input start date must be before the input end date. Future dates (T+1) are not
              accepted in this endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-global-prices/v1/security-shares",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "batch": batch,
                        "calendar": calendar,
                        "end_date": end_date,
                        "frequency": frequency,
                        "start_date": start_date,
                    },
                    security_share_list_params.SecurityShareListParams,
                ),
            ),
            cast_to=SharesOutstandingResponse,
        )


class SecuritySharesResourceWithRawResponse:
    def __init__(self, security_shares: SecuritySharesResource) -> None:
        self._security_shares = security_shares

        self.create = to_raw_response_wrapper(
            security_shares.create,
        )
        self.list = to_raw_response_wrapper(
            security_shares.list,
        )


class AsyncSecuritySharesResourceWithRawResponse:
    def __init__(self, security_shares: AsyncSecuritySharesResource) -> None:
        self._security_shares = security_shares

        self.create = async_to_raw_response_wrapper(
            security_shares.create,
        )
        self.list = async_to_raw_response_wrapper(
            security_shares.list,
        )


class SecuritySharesResourceWithStreamingResponse:
    def __init__(self, security_shares: SecuritySharesResource) -> None:
        self._security_shares = security_shares

        self.create = to_streamed_response_wrapper(
            security_shares.create,
        )
        self.list = to_streamed_response_wrapper(
            security_shares.list,
        )


class AsyncSecuritySharesResourceWithStreamingResponse:
    def __init__(self, security_shares: AsyncSecuritySharesResource) -> None:
        self._security_shares = security_shares

        self.create = async_to_streamed_response_wrapper(
            security_shares.create,
        )
        self.list = async_to_streamed_response_wrapper(
            security_shares.list,
        )
