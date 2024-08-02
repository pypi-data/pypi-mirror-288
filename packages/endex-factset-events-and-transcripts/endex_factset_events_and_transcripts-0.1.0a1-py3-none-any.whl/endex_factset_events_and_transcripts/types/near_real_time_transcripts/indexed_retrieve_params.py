# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["IndexedRetrieveParams"]


class IndexedRetrieveParams(TypedDict, total=False):
    audio_source_id: Required[Annotated[int, PropertyInfo(alias="audioSourceId")]]
    """Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from different source
    (dial-in or webcast). One ReportID can have multiple AudioSourceIDs.
    """

    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""
