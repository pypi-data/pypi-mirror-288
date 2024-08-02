# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import date
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ByDateRetrieveParams"]


class ByDateRetrieveParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Specifies the number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["startDate", "-startDate"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    startDate.
    """

    end_date: Annotated[Union[str, date], PropertyInfo(alias="endDate", format="iso8601")]
    """The latest date of the audio file the API should fetch for.

    - Format: Should be absolute (YYYY-MM-DD).
    """

    end_date_relative: Annotated[int, PropertyInfo(alias="endDateRelative")]
    """
    The latest date of the feed file the API should fetch based on the file
    timestamp.

    Format: Specify the date using a relative term as an integer: '0' for today,
    '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
    used to represent past dates.

    - Either `endDate` or `endDateRelative` should be used, but not both.
    - If both `endDate` and `endDateRelative` are provided in the same request, the
      API will return an error.
    - If users provide future dates in requests for `endDate` or `endDateRelative`,
      the API will not return any data.
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

    start_date: Annotated[Union[str, date], PropertyInfo(alias="startDate", format="iso8601")]
    """The earliest date of the audio file the API should fetch for.

    - Format: Should be absolute (YYYY-MM-DD).
    """

    start_date_relative: Annotated[int, PropertyInfo(alias="startDateRelative")]
    """
    The earliest date of the feed file the API should fetch based on the file
    timestamp.

    - Format: Specify the date using a relative term as an integer: '0' for today,
      '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
      used to represent past dates.

    - _Either `startDate` or `startDateRelative` should be used, but not both._
    - _If both `startDate` and `startDateRelative` are provided in the same request,
      the API will return an error._
    - _If users provide future dates in requests for `startDate` or
      `startDateRelative`, the API will not return any data._
    """

    trimmed: bool
    """
    This parameter helps to search for trimmed audio files, with the non-speaking
    portions removed, and related metadata. The data ranges from May 10, 2011 to Dec
    31, 2022.
    """
