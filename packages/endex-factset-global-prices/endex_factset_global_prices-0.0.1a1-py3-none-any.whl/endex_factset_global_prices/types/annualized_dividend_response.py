# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["AnnualizedDividendResponse", "Data"]


class Data(BaseModel):
    currency: Optional[str] = None
    """
    Currency ISO code associated with the annualized dividends.For more details,
    visit [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    effective_date: Optional[str] = FieldInfo(alias="effectiveDate", default=None)
    """Effective Date or Ex-Date of Annualized Dividend in YYYY-MM-DD format."""

    event_id: Optional[str] = FieldInfo(alias="eventId", default=None)
    """FactSet identifier that uniquely identifies the Event."""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """Factset Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security's best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    iad_def_trading_adj: Optional[float] = FieldInfo(alias="iadDefTradingAdj", default=None)
    """Annualized Dividend value in the trading currency.

    The value is adjusted for splits
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""


class AnnualizedDividendResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Annualized Dividends Objects"""
