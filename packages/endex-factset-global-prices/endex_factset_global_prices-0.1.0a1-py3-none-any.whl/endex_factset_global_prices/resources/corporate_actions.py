# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import corporate_action_list_params, corporate_action_create_params
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
from ..types.corporate_actions_response import CorporateActionsResponse

__all__ = ["CorporateActionsResource", "AsyncCorporateActionsResource"]


class CorporateActionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CorporateActionsResourceWithRawResponse:
        return CorporateActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CorporateActionsResourceWithStreamingResponse:
        return CorporateActionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        cancelled_dividend: Literal["include", "exclude"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        event_category: Literal["CASH_DIVS", "STOCK_DIST", "RIGHTS", "SPINOFFS", "SPLITS", "ALL"]
        | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CorporateActionsResponse:
        """
        Gets the Corporate Actions amounts, dates, types, and flags over a specified
        date range. You may request future dates to receive information for declared
        events. <p>**_startDate and endDate are required parameters. The input startDate
        must come before the input endDate._**

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

          cancelled_dividend: The cancelled dividend returns the dividend details whether they are cancelled
              or active.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          event_category: Selects the Event Category to include in the response.

              - **CASH_DIVS** = Cash Dividends
              - **STOCK_DIST** = Stock Distributions
              - **SPINOFFS** = Spin Offs
              - **RIGHTS** = Rights Issue
              - **SPLITS** = Splits
              - **ALL** = Returns all Event Types. If left blank the service will default to
                ALL.

          fields: Request available Corporate Actions data fields to be included in the response.
              Default is all fields. _fsymId_, _effectiveDate_, _eventTypeCode_ and
              _requestId_ are always included.

              | field         | description                                   |
              | ------------- | --------------------------------------------- |
              | fsymId        | Factset Regional Security Identifier          |
              | eventTypeCode | Character code that denotes the type of event |
              | effectiveDate | The date when security is traded ex-dividend  |
              | requestId     | Identifier that was used for the request.     |

              <h3>Common Fields</h3>
                |field|description|
                |---|---|
                |eventId|Uniquely Identifies the event|
                |eventTypeDesc|Description of the type of event|
                |divTypeCode|Dividend type code. [OA#8764](https://my.apps.factset.com/oa/pages/8764)|
                |announcementDate|Date the event was publicly announced|
                |recordDate|Record date of the event|
                |payDate|Payment date of the event|
              <h3>Dividend Fields</h3>
                |field|description|
                |---|---|
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |amtDefNetGrossIndicator|Indicates whether the default amount is net or gross. G=Gross; N=Net.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |amtNetTradingAdj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date.  The value is adjusted for splits.|
                |amtNetTradingUnadj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |amtGrossTradingAdj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtGrossTradingUnadj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |declaredCurrency|Currency ISO code associated with the declared amount. |
                |amtDefDecAdj|Cash distribution amount (net or gross) in the currency it was declared in. The value is adjusted for splits.|
                |amtDefDecUnadj|Cash distribution amount (net or gross) in the currency it was declared in. The value is not adjusted for splits.|
                |amtNetDecAdj|Net cash distribution amount in the currency it was declared in. The value is adjusted for splits. |
                |amtNetDecUnadj|Net cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |amtGrossDecAdj|Gross cash distribution amount in the currency it was declared in. N/A is returned if the gross amount is not available. The value is adjusted for splits.|
                |amtGrossDecUnadj|Gross cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |dividendStatus|Identifies the cancelled dividents and helps to evaluate their price and portfolio performance.|
                |dividendActiveFlag|Identifies whether the dividend record is currently active(1) or inactive(0).Its applicable to Dividend(DVC) and Dividend with DRP option(DVCD)|
                |dividendsSpecFlag|Indicates a special price implications exists, which may or may not include special dividends. Indicates whether an adjustment should be made to historical pricing.|
                |dividendFrequencyDesc|Dividend Frequency for different event types in the form of a text as per the descriptions found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |dividendFrequencyCode|Dividend Frequency for different event types in the form of a code as per the details found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |frankDefTradingAdj|Split amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankDefTradingUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankDefDecAdj|Split amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.**Only applicable for Australian Securities**.|
                |frankDefDecUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.**Only applicable for Australian Securities**.|
                |frankPct|Percent of total dividend that is franked (subject to tax credit). **Only applicable for Australian Securities**.|
                |taxRate|Domestic Withholding Tax Rate for a Resident Individual|
              <h3>Distribution Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Factor applied to adjust historical prices. Calculation formulas are available on [OA#12619](https://my.apps.factset.com/oa/pages/12619)|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |distPct|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |rightsIssuePrice|Price of the rights issue. |
                |rightsIssueCurrency|Currency the rights issue price was declared in.|
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|
              <h3>Splits Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |distInstFsymId|Helps to identify an instrument representing the distributed company or security associated with ca event identifier. Its applicable for types like Bonus issue(BNS),Stock dividend(DVS),Rights issue (DSR), and spin off(SPO). |
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-global-prices/v1/corporate-actions",
            body=maybe_transform(
                {
                    "ids": ids,
                    "batch": batch,
                    "cancelled_dividend": cancelled_dividend,
                    "currency": currency,
                    "end_date": end_date,
                    "event_category": event_category,
                    "fields": fields,
                    "start_date": start_date,
                },
                corporate_action_create_params.CorporateActionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CorporateActionsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        cancelled_dividend: Literal["include", "exclude"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        event_category: Literal["CASH_DIVS", "STOCK_DIST", "RIGHTS", "SPINOFFS", "SPLITS", "ALL"]
        | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CorporateActionsResponse:
        """
        Gets the Corporate Actions amounts, dates, types, and flags over a specified
        date range. You may request future dates to receive information for declared
        events.

        Event Categories:

        - **Cash Dividends** (CASH_DIVS)
          - **DVC** - Dividend
          - **DVCD** - Dividend with DRP Option
          - **DRP** - Dividend Reinvestment
        - **Stock Distributions** (STOCK_DIST)
          - **DVS** - Stock Dividend
          - **DVSS** - Stock Dividend, Special
          - **BNS** - Bonus Issue
          - **BNSS** - Bonus Issue, Special
        - **Spin Offs** (SPINOFFS)
          - **SPO** - Spin Off
        - **Rights Issue** (RIGHTS)
          - **DSR** - Rights Issue
        - **Splits** (SPLITS)
          - **FSP** - Forward Split
          - **RSP** - Reverse Split
          - **SPL** - Split
          - **EXOS** - Exchange of Securities

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

          cancelled_dividend: The cancelled dividend returns the dividend details whether they are cancelled
              or active.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          event_category: Selects the Event Category to include in the response.

              - **CASH_DIVS** = Cash Dividends
              - **STOCK_DIST** = Stock Distributions
              - **SPINOFFS** = Spin Offs
              - **RIGHTS** = Rights Issue
              - **SPLITS** = Splits
              - **ALL** = Returns all Event Types. If left blank the service will default to
                ALL.

          fields: Request available Corporate Actions data fields to be included in the response.
              Default is all fields. _fsymId_, _effectiveDate_, _eventTypeCode_ and
              _requestId_ are always included.

              | field         | description                                   |
              | ------------- | --------------------------------------------- |
              | fsymId        | Factset Regional Security Identifier          |
              | eventTypeCode | Character code that denotes the type of event |
              | effectiveDate | The date when security is traded ex-dividend  |
              | requestId     | Identifier that was used for the request.     |

              <h3>Common Fields</h3>
                |field|description|
                |---|---|
                |eventId|Uniquely Identifies the event|
                |eventTypeDesc|Description of the type of event|
                |divTypeCode|Dividend type code. [OA#8764](https://my.apps.factset.com/oa/pages/8764)|
                |announcementDate|Date the event was publicly announced|
                |recordDate|Record date of the event|
                |payDate|Payment date of the event|
              <h3>Dividend Fields</h3>
                |field|description|
                |---|---|
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |amtDefNetGrossIndicator|Indicates whether the default amount is net or gross. G=Gross; N=Net.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |amtNetTradingAdj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date.  The value is adjusted for splits.|
                |amtNetTradingUnadj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |amtGrossTradingAdj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtGrossTradingUnadj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |declaredCurrency|Currency ISO code associated with the declared amount. |
                |amtDefDecAdj|Cash distribution amount (net or gross) in the currency it was declared in. The value is adjusted for splits.|
                |amtDefDecUnadj|Cash distribution amount (net or gross) in the currency it was declared in. The value is not adjusted for splits.|
                |amtNetDecAdj|Net cash distribution amount in the currency it was declared in. The value is adjusted for splits. |
                |amtNetDecUnadj|Net cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |amtGrossDecAdj|Gross cash distribution amount in the currency it was declared in. N/A is returned if the gross amount is not available. The value is adjusted for splits.|
                |amtGrossDecUnadj|Gross cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |dividendStatus|Identifies the cancelled dividends status( Active, Cancelled, Postponed, Partial Information) and helps to evaluate their price and portfolio performance.Its applicable to Dividend(DVC) and Dividend with DRP option(DVCD)|
                |dividendActiveFlag|Identifies whether the dividend record is currently active(1) or inactive(0).Its applicable to Dividend(DVC) and Dividend with DRP option(DVCD)|
                |dividendsSpecFlag|Indicates a special price implications exists, which may or may not include special dividends. Indicates whether an adjustment should be made to historical pricing.|
                |dividendFrequencyDesc|Dividend Frequency for different event types in the form of a text as per the descriptions found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |dividendFrequencyCode|Dividend Frequency for different event types in the form of a code as per the details found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |frankDefTradingAdj|Split amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID. Amount is translated to the trading currency based on the exchange rate as of the effective date.**Only applicable for Australian Securities**.|
                |frankDefTradingUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID. Amount is translated to the trading currency based on the exchange rate as of the effective date.**Only applicable for Australian Securities**.|
                |frankDefDecAdj|Split amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankDefDecUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankPct|Percent of total dividend that is franked (subject to tax credit). **Only applicable for Australian Securities**.|
                |taxRate|Domestic Withholding Tax Rate for a Resident Individual|
              <h3>Distribution Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Factor applied to adjust historical prices. Calculation formulas are available on [OA#12619](https://my.apps.factset.com/oa/pages/12619)|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |distPct|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |rightsIssuePrice|Price of the rights issue. |
                |rightsIssueCurrency|Currency the rights issue price was declared in.|
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|
              <h3>Splits Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |distInstFsymId|Helps to identify an instrument representing the distributed company or security associated with ca event identifier. Its applicable for types like Bonus issue(BNS),Stock dividend(DVS),Rights issue (DSR), and spin off(SPO).|
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-global-prices/v1/corporate-actions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "batch": batch,
                        "cancelled_dividend": cancelled_dividend,
                        "currency": currency,
                        "end_date": end_date,
                        "event_category": event_category,
                        "fields": fields,
                        "start_date": start_date,
                    },
                    corporate_action_list_params.CorporateActionListParams,
                ),
            ),
            cast_to=CorporateActionsResponse,
        )


class AsyncCorporateActionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCorporateActionsResourceWithRawResponse:
        return AsyncCorporateActionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCorporateActionsResourceWithStreamingResponse:
        return AsyncCorporateActionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        cancelled_dividend: Literal["include", "exclude"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        event_category: Literal["CASH_DIVS", "STOCK_DIST", "RIGHTS", "SPINOFFS", "SPLITS", "ALL"]
        | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CorporateActionsResponse:
        """
        Gets the Corporate Actions amounts, dates, types, and flags over a specified
        date range. You may request future dates to receive information for declared
        events. <p>**_startDate and endDate are required parameters. The input startDate
        must come before the input endDate._**

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

          cancelled_dividend: The cancelled dividend returns the dividend details whether they are cancelled
              or active.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          event_category: Selects the Event Category to include in the response.

              - **CASH_DIVS** = Cash Dividends
              - **STOCK_DIST** = Stock Distributions
              - **SPINOFFS** = Spin Offs
              - **RIGHTS** = Rights Issue
              - **SPLITS** = Splits
              - **ALL** = Returns all Event Types. If left blank the service will default to
                ALL.

          fields: Request available Corporate Actions data fields to be included in the response.
              Default is all fields. _fsymId_, _effectiveDate_, _eventTypeCode_ and
              _requestId_ are always included.

              | field         | description                                   |
              | ------------- | --------------------------------------------- |
              | fsymId        | Factset Regional Security Identifier          |
              | eventTypeCode | Character code that denotes the type of event |
              | effectiveDate | The date when security is traded ex-dividend  |
              | requestId     | Identifier that was used for the request.     |

              <h3>Common Fields</h3>
                |field|description|
                |---|---|
                |eventId|Uniquely Identifies the event|
                |eventTypeDesc|Description of the type of event|
                |divTypeCode|Dividend type code. [OA#8764](https://my.apps.factset.com/oa/pages/8764)|
                |announcementDate|Date the event was publicly announced|
                |recordDate|Record date of the event|
                |payDate|Payment date of the event|
              <h3>Dividend Fields</h3>
                |field|description|
                |---|---|
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |amtDefNetGrossIndicator|Indicates whether the default amount is net or gross. G=Gross; N=Net.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |amtNetTradingAdj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date.  The value is adjusted for splits.|
                |amtNetTradingUnadj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |amtGrossTradingAdj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtGrossTradingUnadj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |declaredCurrency|Currency ISO code associated with the declared amount. |
                |amtDefDecAdj|Cash distribution amount (net or gross) in the currency it was declared in. The value is adjusted for splits.|
                |amtDefDecUnadj|Cash distribution amount (net or gross) in the currency it was declared in. The value is not adjusted for splits.|
                |amtNetDecAdj|Net cash distribution amount in the currency it was declared in. The value is adjusted for splits. |
                |amtNetDecUnadj|Net cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |amtGrossDecAdj|Gross cash distribution amount in the currency it was declared in. N/A is returned if the gross amount is not available. The value is adjusted for splits.|
                |amtGrossDecUnadj|Gross cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |dividendStatus|Identifies the cancelled dividents and helps to evaluate their price and portfolio performance.|
                |dividendActiveFlag|Identifies whether the dividend record is currently active(1) or inactive(0).Its applicable to Dividend(DVC) and Dividend with DRP option(DVCD)|
                |dividendsSpecFlag|Indicates a special price implications exists, which may or may not include special dividends. Indicates whether an adjustment should be made to historical pricing.|
                |dividendFrequencyDesc|Dividend Frequency for different event types in the form of a text as per the descriptions found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |dividendFrequencyCode|Dividend Frequency for different event types in the form of a code as per the details found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |frankDefTradingAdj|Split amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankDefTradingUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankDefDecAdj|Split amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.**Only applicable for Australian Securities**.|
                |frankDefDecUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.**Only applicable for Australian Securities**.|
                |frankPct|Percent of total dividend that is franked (subject to tax credit). **Only applicable for Australian Securities**.|
                |taxRate|Domestic Withholding Tax Rate for a Resident Individual|
              <h3>Distribution Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Factor applied to adjust historical prices. Calculation formulas are available on [OA#12619](https://my.apps.factset.com/oa/pages/12619)|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |distPct|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |rightsIssuePrice|Price of the rights issue. |
                |rightsIssueCurrency|Currency the rights issue price was declared in.|
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|
              <h3>Splits Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |distInstFsymId|Helps to identify an instrument representing the distributed company or security associated with ca event identifier. Its applicable for types like Bonus issue(BNS),Stock dividend(DVS),Rights issue (DSR), and spin off(SPO). |
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-global-prices/v1/corporate-actions",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "batch": batch,
                    "cancelled_dividend": cancelled_dividend,
                    "currency": currency,
                    "end_date": end_date,
                    "event_category": event_category,
                    "fields": fields,
                    "start_date": start_date,
                },
                corporate_action_create_params.CorporateActionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CorporateActionsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        batch: Literal["Y", "N"] | NotGiven = NOT_GIVEN,
        cancelled_dividend: Literal["include", "exclude"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        event_category: Literal["CASH_DIVS", "STOCK_DIST", "RIGHTS", "SPINOFFS", "SPLITS", "ALL"]
        | NotGiven = NOT_GIVEN,
        fields: List[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CorporateActionsResponse:
        """
        Gets the Corporate Actions amounts, dates, types, and flags over a specified
        date range. You may request future dates to receive information for declared
        events.

        Event Categories:

        - **Cash Dividends** (CASH_DIVS)
          - **DVC** - Dividend
          - **DVCD** - Dividend with DRP Option
          - **DRP** - Dividend Reinvestment
        - **Stock Distributions** (STOCK_DIST)
          - **DVS** - Stock Dividend
          - **DVSS** - Stock Dividend, Special
          - **BNS** - Bonus Issue
          - **BNSS** - Bonus Issue, Special
        - **Spin Offs** (SPINOFFS)
          - **SPO** - Spin Off
        - **Rights Issue** (RIGHTS)
          - **DSR** - Rights Issue
        - **Splits** (SPLITS)
          - **FSP** - Forward Split
          - **RSP** - Reverse Split
          - **SPL** - Split
          - **EXOS** - Exchange of Securities

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

          cancelled_dividend: The cancelled dividend returns the dividend details whether they are cancelled
              or active.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          event_category: Selects the Event Category to include in the response.

              - **CASH_DIVS** = Cash Dividends
              - **STOCK_DIST** = Stock Distributions
              - **SPINOFFS** = Spin Offs
              - **RIGHTS** = Rights Issue
              - **SPLITS** = Splits
              - **ALL** = Returns all Event Types. If left blank the service will default to
                ALL.

          fields: Request available Corporate Actions data fields to be included in the response.
              Default is all fields. _fsymId_, _effectiveDate_, _eventTypeCode_ and
              _requestId_ are always included.

              | field         | description                                   |
              | ------------- | --------------------------------------------- |
              | fsymId        | Factset Regional Security Identifier          |
              | eventTypeCode | Character code that denotes the type of event |
              | effectiveDate | The date when security is traded ex-dividend  |
              | requestId     | Identifier that was used for the request.     |

              <h3>Common Fields</h3>
                |field|description|
                |---|---|
                |eventId|Uniquely Identifies the event|
                |eventTypeDesc|Description of the type of event|
                |divTypeCode|Dividend type code. [OA#8764](https://my.apps.factset.com/oa/pages/8764)|
                |announcementDate|Date the event was publicly announced|
                |recordDate|Record date of the event|
                |payDate|Payment date of the event|
              <h3>Dividend Fields</h3>
                |field|description|
                |---|---|
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |amtDefNetGrossIndicator|Indicates whether the default amount is net or gross. G=Gross; N=Net.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |amtNetTradingAdj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date.  The value is adjusted for splits.|
                |amtNetTradingUnadj|Net distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |amtGrossTradingAdj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtGrossTradingUnadj|Gross distribution amount in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits.|
                |declaredCurrency|Currency ISO code associated with the declared amount. |
                |amtDefDecAdj|Cash distribution amount (net or gross) in the currency it was declared in. The value is adjusted for splits.|
                |amtDefDecUnadj|Cash distribution amount (net or gross) in the currency it was declared in. The value is not adjusted for splits.|
                |amtNetDecAdj|Net cash distribution amount in the currency it was declared in. The value is adjusted for splits. |
                |amtNetDecUnadj|Net cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |amtGrossDecAdj|Gross cash distribution amount in the currency it was declared in. N/A is returned if the gross amount is not available. The value is adjusted for splits.|
                |amtGrossDecUnadj|Gross cash distribution amount in the currency it was declared in. The value is not adjusted for splits.|
                |dividendStatus|Identifies the cancelled dividends status( Active, Cancelled, Postponed, Partial Information) and helps to evaluate their price and portfolio performance.Its applicable to Dividend(DVC) and Dividend with DRP option(DVCD)|
                |dividendActiveFlag|Identifies whether the dividend record is currently active(1) or inactive(0).Its applicable to Dividend(DVC) and Dividend with DRP option(DVCD)|
                |dividendsSpecFlag|Indicates a special price implications exists, which may or may not include special dividends. Indicates whether an adjustment should be made to historical pricing.|
                |dividendFrequencyDesc|Dividend Frequency for different event types in the form of a text as per the descriptions found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |dividendFrequencyCode|Dividend Frequency for different event types in the form of a code as per the details found here [OA#8764](https://my.apps.factset.com/oa/pages/8764#Frequency)|
                |frankDefTradingAdj|Split amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID. Amount is translated to the trading currency based on the exchange rate as of the effective date.**Only applicable for Australian Securities**.|
                |frankDefTradingUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the trading currency of the input ID. Amount is translated to the trading currency based on the exchange rate as of the effective date.**Only applicable for Australian Securities**.|
                |frankDefDecAdj|Split amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankDefDecUnadj|Unsplit amount of dividend that is franked (subject to tax credit). Published in the currency the dividend was declared in.Amount is translated to the trading currency based on the exchange rate as of the effective date. **Only applicable for Australian Securities**.|
                |frankPct|Percent of total dividend that is franked (subject to tax credit). **Only applicable for Australian Securities**.|
                |taxRate|Domestic Withholding Tax Rate for a Resident Individual|
              <h3>Distribution Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Factor applied to adjust historical prices. Calculation formulas are available on [OA#12619](https://my.apps.factset.com/oa/pages/12619)|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |amtDefTradingAdj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is adjusted for splits.|
                |amtDefTradingUnadj|Cash distribution amount (net or gross) in the trading currency of the record. Amount is translated to the trading currency based on the exchange rate as of the effective date. The value is not adjusted for splits. |
                |currency|Currency ISO code associated with distribution amount converted into trading currency of the record.|
                |distPct|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |rightsIssuePrice|Price of the rights issue. |
                |rightsIssueCurrency|Currency the rights issue price was declared in.|
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|
              <h3>Splits Fields</h3>
                |field|description|
                |---|---|
                |adjFactor|Distribution percentage of the event  (i.e. 10%). Typical for stock distributions.|
                |adjFactorCombined|Combined adjustment factor for all distribution events on that day.|
                |distOldTerm|Component of distribution ratio- Number of shares held.|
                |distNewTerm|Component of distribution ratio - Number of shares received.|
                |distInstFsymId|Helps to identify an instrument representing the distributed company or security associated with ca event identifier. Its applicable for types like Bonus issue(BNS),Stock dividend(DVS),Rights issue (DSR), and spin off(SPO).|
                |shortDesc|Textual description identifying the event. Example- Split (Mandatory): 3 for 1.|

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. In the
              context of corporate actions, this filters the response to only include events
              within the date range. The frequency between the startDate and endDate is always
              set to the "event" frequency- meaning the service will return only events within
              those inclusive boundaries. Leaving both startDate and endDate blank will pull
              "all" events for each requested ids.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-global-prices/v1/corporate-actions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "batch": batch,
                        "cancelled_dividend": cancelled_dividend,
                        "currency": currency,
                        "end_date": end_date,
                        "event_category": event_category,
                        "fields": fields,
                        "start_date": start_date,
                    },
                    corporate_action_list_params.CorporateActionListParams,
                ),
            ),
            cast_to=CorporateActionsResponse,
        )


class CorporateActionsResourceWithRawResponse:
    def __init__(self, corporate_actions: CorporateActionsResource) -> None:
        self._corporate_actions = corporate_actions

        self.create = to_raw_response_wrapper(
            corporate_actions.create,
        )
        self.list = to_raw_response_wrapper(
            corporate_actions.list,
        )


class AsyncCorporateActionsResourceWithRawResponse:
    def __init__(self, corporate_actions: AsyncCorporateActionsResource) -> None:
        self._corporate_actions = corporate_actions

        self.create = async_to_raw_response_wrapper(
            corporate_actions.create,
        )
        self.list = async_to_raw_response_wrapper(
            corporate_actions.list,
        )


class CorporateActionsResourceWithStreamingResponse:
    def __init__(self, corporate_actions: CorporateActionsResource) -> None:
        self._corporate_actions = corporate_actions

        self.create = to_streamed_response_wrapper(
            corporate_actions.create,
        )
        self.list = to_streamed_response_wrapper(
            corporate_actions.list,
        )


class AsyncCorporateActionsResourceWithStreamingResponse:
    def __init__(self, corporate_actions: AsyncCorporateActionsResource) -> None:
        self._corporate_actions = corporate_actions

        self.create = async_to_streamed_response_wrapper(
            corporate_actions.create,
        )
        self.list = async_to_streamed_response_wrapper(
            corporate_actions.list,
        )
