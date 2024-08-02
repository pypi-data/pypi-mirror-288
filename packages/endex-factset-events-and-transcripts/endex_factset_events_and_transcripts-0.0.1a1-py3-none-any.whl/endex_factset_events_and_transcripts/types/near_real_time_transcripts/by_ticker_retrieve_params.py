# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ByTickerRetrieveParams"]


class ByTickerRetrieveParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["eventDatetimeUtc", "-eventDatetimeUtc"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDatetimeUtc.
    """

    call_status: Annotated[Literal["InProgress", "Ended", "EWN", "IssueAtSource"], PropertyInfo(alias="callStatus")]
    """
    Status of the call, i.e., Ended, InProgress, EndedWithoutNotification, or
    IssueAtSource.
    """

    entity_id: Annotated[str, PropertyInfo(alias="entityId")]
    """Factset entity level identifier for the company hosting the event."""

    ticker: str
    """Ticker-region identifier for the company hosting the event."""
