# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PriceCreateParams"]


class PriceCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids.

    <p>ids limit =  500 per non-batch request / 2000 per batch request for a single day and 50 per multi-day request</p>
    """

    start_date: Required[Annotated[str, PropertyInfo(alias="startDate")]]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    Future dates (T+1) are not accepted in this endpoint.
    """

    adjust: Literal["SPLIT", "SPLIT_SPINOFF", "UNSPLIT"]
    """Controls the split and spinoff adjustments for the prices.

    - **SPLIT** = Split ONLY Adjusted. This is used by default.
    - **SPLIT_SPINOFF** = Splits & Spinoff Adjusted.
    - **UNSPLIT** = No Adjustments.
    """

    batch: Literal["Y", "N"]
    """
    Enables the ability to asynchronously "batch" the request, supporting a
    long-running request for up to 20 minutes. Upon requesting batch=Y, the service
    will respond back with an HTTP Status Code of 202. Once a batch request is
    submitted, use batch status to see if the job has been completed. Once
    completed, retrieve the results of the request via batch-result. When using
    Batch, ids limit is increased to 10000 ids per request, though limits on query
    string via GET method still apply. It's advised to submit large lists of ids via
    POST method. Please note that the number of unique currencies present in the
    requested ids is limited to 50 per request.
    """

    calendar: Literal["FIVEDAY", "SEVENDAY", "US"]
    """Calendar of data returned. SEVENDAY includes weekends."""

    currency: str
    """Currency code for adjusting prices.

    Default is Local. For a list of currency ISO codes, visit
    [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """The end date requested for a given date range in **YYYY-MM-DD** format.

    Future dates (T+1) are not accepted in this endpoint.
    """

    fields: List[str]
    """Request available pricing data fields to be included in the response.

    Default is all fields. All responses will include the _fsymId_, _date_, and
    _currency_ fields. |field|description| |---|---| |price|Closing Price|
    |priceOpen|Opening Price| |priceHigh|High Price| |priceLow|Low Price|
    |volume|Volume| |turnover|Total Trade Value for the Day| |tradeCount|Number of
    Trades| |vwap|Volume Weighted Average Price|
    """

    frequency: Literal["D", "AD", "W", "M", "AM", "AQ", "CQ", "ASA", "CSA", "AY", "CY"]
    """Controls the display frequency of the data returned.

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
    """
