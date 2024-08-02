# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import date
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["DateListParams"]


class DateListParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["storyDateTime", "-storyDateTime"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDate.
    """

    end_date: Annotated[Union[str, date], PropertyInfo(alias="endDate", format="iso8601")]
    """End Date. Format is YYYY-MM-DD."""

    end_date_relative: Annotated[int, PropertyInfo(alias="endDateRelative")]
    """
    The latest date of the feed file the API should fetch for based on the file
    timestamp.

    - Format: Specify the date using a relative term as an integer: '0' for today,
      '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
      used to represent past dates.

    - _Either `endDate` or `endDateRelative` should be used, but not both._
    - _If both `endDate` and `endDateRelative` are provided in the same request, the
      API will return an error._
    - _If users provide future dates in requests for `endDate` or `endDateRelative`,
      the API will not return any data._
    """

    start_date: Annotated[Union[str, date], PropertyInfo(alias="startDate", format="iso8601")]
    """Start Date. Format is YYYY-MM-DD

    **The API supports data from 1999 onwards. Ensure that the provided Date falls
    within this range for accurate results.**
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

    time_zone: Annotated[str, PropertyInfo(alias="timeZone")]
    """
    timeZone to return story dates and times.Time zones, represented in POSIX
    format, are automatically adjusted for daylight savings. timeZone names are
    sourced from the IANA timezone registry. The time fields in the response will
    adhere to this specified timezone.
    """
