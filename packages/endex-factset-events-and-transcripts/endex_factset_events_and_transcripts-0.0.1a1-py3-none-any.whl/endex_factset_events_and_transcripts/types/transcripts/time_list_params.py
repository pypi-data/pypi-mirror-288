# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TimeListParams"]


class TimeListParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["storyDateTime", "-storyDateTime", "uploadDateTime", "-uploadDateTime"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDate.
    """

    end_date_time: Annotated[Union[str, datetime], PropertyInfo(alias="endDateTime", format="iso8601")]
    """The date to which data is required"""

    start_date_time: Annotated[Union[str, datetime], PropertyInfo(alias="startDateTime", format="iso8601")]
    """\\**\\**The API supports data from 1999 onwards.

    Ensure that the provided Date falls within this range for accurate results.\\**\\**
    """
