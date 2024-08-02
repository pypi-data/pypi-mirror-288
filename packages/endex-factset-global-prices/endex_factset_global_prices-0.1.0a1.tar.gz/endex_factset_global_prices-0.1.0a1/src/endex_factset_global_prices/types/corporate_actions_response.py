# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CorporateActionsResponse", "Data"]


class Data(BaseModel):
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


class CorporateActionsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Corporate Action Objects"""
