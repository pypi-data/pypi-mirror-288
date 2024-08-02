# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SharesOutstandingResponse", "Data"]


class Data(BaseModel):
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


class SharesOutstandingResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Shares Outstanding Objects"""
