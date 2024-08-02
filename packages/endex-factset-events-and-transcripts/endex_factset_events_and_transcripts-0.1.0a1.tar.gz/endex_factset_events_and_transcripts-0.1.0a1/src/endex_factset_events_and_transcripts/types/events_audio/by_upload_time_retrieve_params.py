# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ByUploadTimeRetrieveParams"]


class ByUploadTimeRetrieveParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Specifies the number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["uploadTime", "-uploadTime"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    uploadTime.
    """

    ids: List[str]
    """
    This parameter filters the results based on ticker-region or Entity ID or the
    combination of both. A comma is used to separate each identifier.
    """

    source_code: Annotated[
        Literal["Phone", "Webcast", "Vendor", "WebcastReplay", "Flash", "Replay"], PropertyInfo(alias="sourceCode")
    ]
    """This parameter filters the results based on Source of the Audio file.

    Below are the descriptions for each Source Code -

    - Phone = Originated from phone call
    - Webcast = Originated from a webcast
    - Vendor = Received from vendor
    - WebcastReplay = Replay of a webcast
    - Flash = Identical to webcast; can merge with "Webcast" in the future
    - Replay = Phone replay
    """

    trimmed: bool
    """
    This parameter helps to search for trimmed audio files, with the non-speaking
    portions removed, and related metadata. The data ranges from May 10, 2011 to Dec
    31, 2022.
    """

    upload_time: Annotated[int, PropertyInfo(alias="uploadTime")]
    """
    This parameter filters data based on uploadTime relative to the current time, in
    hours. For example:- uploadTime = -15 (fetches audio files between 15 hours ago
    and now)

    Minimum is 1 hour i.e., uploadTime= -1

    Maximum is 1 week/168 hours i.e., uploadTime=-168
    """
