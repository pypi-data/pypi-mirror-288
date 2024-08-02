# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import TYPE_CHECKING, List, Union, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "BatchResultResponse",
    "Data",
    "DataPrice",
    "DataReturns",
    "DataCorporateAction",
    "DataAnnualizedDividendsObject",
    "DataSharesOutstandingResponseObject",
]


class DataPrice(BaseModel):
    currency: Optional[str] = None
    """Currency ISO code.

    For more details, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    date: Optional[datetime.date] = None
    """Ending date for the period expressed in YYYY-MM-DD format."""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Permanent Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R) or
    a -L Suffix (XXXXXX-L).
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object:
            ...


class DataReturns(BaseModel):
    currency: Optional[str] = None
    """Currency ISO code.

    For more details, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    date: Optional[datetime.date] = None
    """End date of the return.

    Date in YYYY-MM-DD format. Depending on Frequency and Calendar settings, this
    could represent the entire return period requested.
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Permanent Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R) or
    a -L Suffix (XXXXXX-L).
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    total_return: Optional[float] = FieldInfo(alias="totalReturn", default=None)
    """Returns the data for the given input parameters."""


class DataCorporateAction(BaseModel):
    announcement_date: Optional[str] = FieldInfo(alias="announcementDate", default=None)
    """Date Event was announced in YYYY-MM-DD format."""

    div_type_code: Optional[str] = FieldInfo(alias="divTypeCode", default=None)
    """Dividend Type Code.

    For code descriptions, visit [Online Assistant Page #8764]
    (https://oa.apps.factset.com/pages/8764).
    """

    effective_date: Optional[str] = FieldInfo(alias="effectiveDate", default=None)
    """Effective Date or Ex-Date of distribution in YYYY-MM-DD format."""

    event_id: Optional[str] = FieldInfo(alias="eventId", default=None)
    """FactSet identifier that uniquely identifies the Event."""

    event_type_code: Optional[str] = FieldInfo(alias="eventTypeCode", default=None)
    """
    Corporate Actions Event type code, possible values: [ DVC, DVCD, DRP, DVS, DVSS,
    BNS, BNSS, SPO, DSR, FSP, RSP, SPL ]
    """

    event_type_desc: Optional[str] = FieldInfo(alias="eventTypeDesc", default=None)
    """Corporate Actions Event type description."""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """Factset Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security's best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    pay_date: Optional[str] = FieldInfo(alias="payDate", default=None)
    """Date of Payment for distribution in YYYY-MM-DD format."""

    record_date: Optional[str] = FieldInfo(alias="recordDate", default=None)
    """Date of Record for distribution in YYYY-MM-DD format."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object:
            ...


class DataAnnualizedDividendsObject(BaseModel):
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


class DataSharesOutstandingResponseObject(BaseModel):
    adr_description: Optional[str] = FieldInfo(alias="adrDescription", default=None)
    """
    Different stock types based on the rights and benefits from ownership for the
    ADR.
    """

    adr_fsym_id: Optional[str] = FieldInfo(alias="adrFsymId", default=None)
    """
    Unique FactSet generated identifier assigned to a security, representing the ADR
    security.
    """

    adr_ratio: Optional[float] = FieldInfo(alias="adrRatio", default=None)
    """
    Number of common or ordinary shares that are equivalent to one American
    Depositary Receipt (ADR).
    """

    adr_total_outstanding: Optional[float] = FieldInfo(alias="adrTotalOutstanding", default=None)
    """Number of shares outstanding for the ADR as of `date`."""

    date: Optional[datetime.date] = None
    """Date of the record in YYYY-MM-DD format."""

    description: Optional[str] = None
    """Different stock types based on the rights and benefits from ownership."""

    document_id: Optional[str] = FieldInfo(alias="documentId", default=None)
    """
    Unique Identifier for each document or filing which contains the outstanding
    shares position.
    """

    fiscal_year: Optional[int] = FieldInfo(alias="fiscalYear", default=None)
    """The company's fiscal year corresponding to the report."""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """Security-level FactSet Permanent Identifier associated with the identifier."""

    publication_date: Optional[datetime.date] = FieldInfo(alias="publicationDate", default=None)
    """Exact date that results have been communicated to the market."""

    report_date: Optional[datetime.date] = FieldInfo(alias="reportDate", default=None)
    """Reporting date of the position."""

    reporting_period: Optional[int] = FieldInfo(alias="reportingPeriod", default=None)
    """Code representing the unique reporting period. Options are as follows:

    - 1 - 1st Quarter
    - 2 - 2nd Quarter
    - 3 - 3rd Quarter
    - 4 - 4th Quarter
    - 6 - Mid-Year
    """

    reporting_period_description: Optional[str] = FieldInfo(alias="reportingPeriodDescription", default=None)
    """Textual description of the reporting period."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """FactSet Security Permanent Identifier that was used for the request."""

    total_outstanding: Optional[float] = FieldInfo(alias="totalOutstanding", default=None)
    """Number of shares outstanding as of `date`."""


Data = Union[
    DataPrice, DataReturns, DataCorporateAction, DataAnnualizedDividendsObject, DataSharesOutstandingResponseObject
]


class BatchResultResponse(BaseModel):
    data: List[Data]
