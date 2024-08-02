# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import price_list_params, price_create_params
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
from ..types.global_prices_response import GlobalPricesResponse

__all__ = ["PricesResource", "AsyncPricesResource"]


class PricesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PricesResourceWithRawResponse:
        return PricesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PricesResourceWithStreamingResponse:
        return PricesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        start_date: str,
        adjust: Literal["SPLIT", "SPLIT_SPINOFF", "UNSPLIT"] | NotGiven = NOT_GIVEN,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        calendar: Literal["FIVEDAY", "SEVENDAY", "US"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GlobalPricesResponse:
        """
        Gets security prices', Open, High, Low, Close, Volume, VWAP, Trade Count, and
        Turn Over for a specified list of securities, date range, currency, and
        adjustment factors.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.

              <p>ids limit =  500 per non-batch request / 2000 per batch request for a single day and 50 per multi-day request</p>

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

          adjust: Controls the split and spinoff adjustments for the prices.

              - **SPLIT** = Split ONLY Adjusted. This is used by default.
              - **SPLIT_SPINOFF** = Splits & Spinoff Adjusted.
              - **UNSPLIT** = No Adjustments.

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond back with an HTTP Status Code of 202. Once a batch request is
              submitted, use batch status to see if the job has been completed. Once
              completed, retrieve the results of the request via batch-result. When using
              Batch, ids limit is increased to 10000 ids per request, though limits on query
              string via GET method still apply. It's advised to submit large lists of ids via
              POST method. Please note that the number of unique currencies present in the
              requested ids is limited to 50 per request.

          calendar: Calendar of data returned. SEVENDAY includes weekends.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

          fields: Request available pricing data fields to be included in the response. Default is
              all fields. All responses will include the _fsymId_, _date_, and _currency_
              fields. |field|description| |---|---| |price|Closing Price| |priceOpen|Opening
              Price| |priceHigh|High Price| |priceLow|Low Price| |volume|Volume|
              |turnover|Total Trade Value for the Day| |tradeCount|Number of Trades|
              |vwap|Volume Weighted Average Price|

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
            "/factset-global-prices/v1/prices",
            body=maybe_transform(
                {
                    "ids": ids,
                    "start_date": start_date,
                    "adjust": adjust,
                    "batch": batch,
                    "calendar": calendar,
                    "currency": currency,
                    "end_date": end_date,
                    "fields": fields,
                    "frequency": frequency,
                },
                price_create_params.PriceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GlobalPricesResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        start_date: str,
        adjust: Literal["SPLIT", "SPLIT_SPINOFF", "UNSPLIT"] | NotGiven = NOT_GIVEN,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        calendar: Literal["FIVEDAY", "SEVENDAY", "US"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GlobalPricesResponse:
        """
        Gets security prices', Open, High, Low, Close, Volume, VWAP, Trade Count, and
        Turn Over for a specified list of securities, date range, currency, and
        adjustment factors.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** =
              1000 per non-batch request / 2000 per batch request for a single day and 50 per
              multi-day request. The number of unique currencies present in the requested ids
              is limited to 50 per request._</p> _<p>Make note, GET Method URL request lines
              are also limited to a total length of 8192 bytes (8KB). In cases where the
              service allows for thousands of ids, which may lead to exceeding this request
              line limit of 8KB, it's advised for any requests with large request lines to be
              requested through the respective "POST" method.</p>\\**

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. The
              input start date must be before the input end date. Future dates (T+1) are not
              accepted in this endpoint.

          adjust: Controls the split and spinoff adjustments for the prices.

              - **SPLIT** = Split ONLY Adjusted. This is used by default.
              - **SPLIT_SPINOFF** = Splits & Spinoff Adjusted.
              - **UNSPLIT** = No Adjustments.

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

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. The
              input end date must be after the input start date. Future dates (T+1) are not
              accepted in this endpoint.

          fields: Request available pricing data fields to be included in the response. Default is
              all fields. All responses will include the _fsymId_, _date_, and _currency_
              fields. |field|description| |---|---| |price|Closing Price| |priceOpen|Opening
              Price| |priceHigh|High Price| |priceLow|Low Price| |volume|Volume|
              |turnover|Total Trade Value for the Day| |tradeCount|Number of Trades|
              |vwap|Volume Weighted Average Price|

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
            "/factset-global-prices/v1/prices",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "start_date": start_date,
                        "adjust": adjust,
                        "batch": batch,
                        "calendar": calendar,
                        "currency": currency,
                        "end_date": end_date,
                        "fields": fields,
                        "frequency": frequency,
                    },
                    price_list_params.PriceListParams,
                ),
            ),
            cast_to=GlobalPricesResponse,
        )


class AsyncPricesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPricesResourceWithRawResponse:
        return AsyncPricesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPricesResourceWithStreamingResponse:
        return AsyncPricesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        start_date: str,
        adjust: Literal["SPLIT", "SPLIT_SPINOFF", "UNSPLIT"] | NotGiven = NOT_GIVEN,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        calendar: Literal["FIVEDAY", "SEVENDAY", "US"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GlobalPricesResponse:
        """
        Gets security prices', Open, High, Low, Close, Volume, VWAP, Trade Count, and
        Turn Over for a specified list of securities, date range, currency, and
        adjustment factors.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.

              <p>ids limit =  500 per non-batch request / 2000 per batch request for a single day and 50 per multi-day request</p>

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

          adjust: Controls the split and spinoff adjustments for the prices.

              - **SPLIT** = Split ONLY Adjusted. This is used by default.
              - **SPLIT_SPINOFF** = Splits & Spinoff Adjusted.
              - **UNSPLIT** = No Adjustments.

          batch: Enables the ability to asynchronously "batch" the request, supporting a
              long-running request for up to 20 minutes. Upon requesting batch=Y, the service
              will respond back with an HTTP Status Code of 202. Once a batch request is
              submitted, use batch status to see if the job has been completed. Once
              completed, retrieve the results of the request via batch-result. When using
              Batch, ids limit is increased to 10000 ids per request, though limits on query
              string via GET method still apply. It's advised to submit large lists of ids via
              POST method. Please note that the number of unique currencies present in the
              requested ids is limited to 50 per request.

          calendar: Calendar of data returned. SEVENDAY includes weekends.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. Future
              dates (T+1) are not accepted in this endpoint.

          fields: Request available pricing data fields to be included in the response. Default is
              all fields. All responses will include the _fsymId_, _date_, and _currency_
              fields. |field|description| |---|---| |price|Closing Price| |priceOpen|Opening
              Price| |priceHigh|High Price| |priceLow|Low Price| |volume|Volume|
              |turnover|Total Trade Value for the Day| |tradeCount|Number of Trades|
              |vwap|Volume Weighted Average Price|

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
            "/factset-global-prices/v1/prices",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "start_date": start_date,
                    "adjust": adjust,
                    "batch": batch,
                    "calendar": calendar,
                    "currency": currency,
                    "end_date": end_date,
                    "fields": fields,
                    "frequency": frequency,
                },
                price_create_params.PriceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GlobalPricesResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        start_date: str,
        adjust: Literal["SPLIT", "SPLIT_SPINOFF", "UNSPLIT"] | NotGiven = NOT_GIVEN,
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        calendar: Literal["FIVEDAY", "SEVENDAY", "US"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GlobalPricesResponse:
        """
        Gets security prices', Open, High, Low, Close, Volume, VWAP, Trade Count, and
        Turn Over for a specified list of securities, date range, currency, and
        adjustment factors.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids.<p>**\\**ids limit** =
              1000 per non-batch request / 2000 per batch request for a single day and 50 per
              multi-day request. The number of unique currencies present in the requested ids
              is limited to 50 per request._</p> _<p>Make note, GET Method URL request lines
              are also limited to a total length of 8192 bytes (8KB). In cases where the
              service allows for thousands of ids, which may lead to exceeding this request
              line limit of 8KB, it's advised for any requests with large request lines to be
              requested through the respective "POST" method.</p>\\**

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. The
              input start date must be before the input end date. Future dates (T+1) are not
              accepted in this endpoint.

          adjust: Controls the split and spinoff adjustments for the prices.

              - **SPLIT** = Split ONLY Adjusted. This is used by default.
              - **SPLIT_SPINOFF** = Splits & Spinoff Adjusted.
              - **UNSPLIT** = No Adjustments.

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

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. The
              input end date must be after the input start date. Future dates (T+1) are not
              accepted in this endpoint.

          fields: Request available pricing data fields to be included in the response. Default is
              all fields. All responses will include the _fsymId_, _date_, and _currency_
              fields. |field|description| |---|---| |price|Closing Price| |priceOpen|Opening
              Price| |priceHigh|High Price| |priceLow|Low Price| |volume|Volume|
              |turnover|Total Trade Value for the Day| |tradeCount|Number of Trades|
              |vwap|Volume Weighted Average Price|

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
            "/factset-global-prices/v1/prices",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "start_date": start_date,
                        "adjust": adjust,
                        "batch": batch,
                        "calendar": calendar,
                        "currency": currency,
                        "end_date": end_date,
                        "fields": fields,
                        "frequency": frequency,
                    },
                    price_list_params.PriceListParams,
                ),
            ),
            cast_to=GlobalPricesResponse,
        )


class PricesResourceWithRawResponse:
    def __init__(self, prices: PricesResource) -> None:
        self._prices = prices

        self.create = to_raw_response_wrapper(
            prices.create,
        )
        self.list = to_raw_response_wrapper(
            prices.list,
        )


class AsyncPricesResourceWithRawResponse:
    def __init__(self, prices: AsyncPricesResource) -> None:
        self._prices = prices

        self.create = async_to_raw_response_wrapper(
            prices.create,
        )
        self.list = async_to_raw_response_wrapper(
            prices.list,
        )


class PricesResourceWithStreamingResponse:
    def __init__(self, prices: PricesResource) -> None:
        self._prices = prices

        self.create = to_streamed_response_wrapper(
            prices.create,
        )
        self.list = to_streamed_response_wrapper(
            prices.list,
        )


class AsyncPricesResourceWithStreamingResponse:
    def __init__(self, prices: AsyncPricesResource) -> None:
        self._prices = prices

        self.create = async_to_streamed_response_wrapper(
            prices.create,
        )
        self.list = async_to_streamed_response_wrapper(
            prices.list,
        )
