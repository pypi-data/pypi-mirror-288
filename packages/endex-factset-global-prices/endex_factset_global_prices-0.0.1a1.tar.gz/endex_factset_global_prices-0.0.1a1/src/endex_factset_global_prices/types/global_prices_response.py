# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["GlobalPricesResponse", "Data"]


class Data(BaseModel):
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


class GlobalPricesResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Price Objects"""
