# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AnnualizedDividendListParams"]


class AnnualizedDividendListParams(TypedDict, total=False):
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
