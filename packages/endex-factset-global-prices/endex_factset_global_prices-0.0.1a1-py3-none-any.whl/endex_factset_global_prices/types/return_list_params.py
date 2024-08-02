# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ReturnListParams"]


class ReturnListParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids.<p>**\\**ids limit** = 50 per both non-batch request and batch
    request*</p> *<p>Make note, GET Method URL request lines are also limited to a
    total length of 8192 bytes (8KB). In cases where the service allows for
    thousands of ids, which may lead to exceeding this request line limit of 8KB,
    it's advised for any requests with large request lines to be requested through
    the respective "POST" method.</p>\\**
    """

    start_date: Required[Annotated[str, PropertyInfo(alias="startDate")]]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    The input start date must be before the input end date. Future dates (T+1) are
    not accepted in this endpoint.
    """

    batch: Literal["Y", "N"]
    """
    Enables the ability to asynchronously "batch" the request, supporting a
    long-running request for up to 20 minutes. Upon requesting batch=Y, the service
    will respond with an HTTP Status Code of 202. Once a batch request is submitted,
    use batch status to see if the job has been completed. Once completed, retrieve
    the results of the request via batch-result. When using Batch, ids limit is
    increased to 10000 ids per request, though limits on query string via GET method
    still apply. It's advised to submit large lists of ids via POST method.
    <B>Please note that the number of unique currencies present in the requested ids
    is limited to 50 per request.</B>
    """

    currency: str
    """Currency code for adjusting prices.

    Default is Local. For a list of currency ISO codes, visit
    [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).
    """

    dividend_adjust: Annotated[
        Literal["PRICE", "EXDATE", "PAYDATE", "EXDATE_C", "PAYDATE_C"], PropertyInfo(alias="dividendAdjust")
    ]
    """Controls the dividend reinvestment for the returns calculation.

    - **PRICE** = Price Change - Dividends Excluded.
    - **EXDATE** = Simple Return - Dividends Received on exdate but not reinvested.
    - **PAYDATE** = Simple Return - Dividends Received on paydate but not
      reinvested.
    - **EXDATE_C** = Compound Return - Dividends reinvested on exdate.
    - **PAYDATE_C** = Compound Return - Dividends reinvested on paydate.
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """The end date requested for a given date range in **YYYY-MM-DD** format.

    The input end date must be after the input start date. Future dates (T+1) are
    not accepted in this endpoint.
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
