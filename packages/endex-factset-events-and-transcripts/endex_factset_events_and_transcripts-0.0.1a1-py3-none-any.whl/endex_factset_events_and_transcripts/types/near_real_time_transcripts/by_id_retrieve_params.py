# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ByIDRetrieveParams"]


class ByIDRetrieveParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["eventDatetimeUtc", "-eventDatetimeUtc"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDatetimeUtc.
    """

    audio_source_id: Annotated[int, PropertyInfo(alias="audioSourceId")]
    """Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from different source
    (dial-in or webcast). One ReportID can have multiple AudioSourceIDs.
    """

    report_id: Annotated[int, PropertyInfo(alias="reportId")]
    """Unique identifier for an event."""
