# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["SearchListParams"]


class SearchListParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["storyDateTime", "-storyDateTime"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDate.
    """

    search_text: Annotated[str, PropertyInfo(alias="searchText")]
    """
    Restricts the search to include only document stories which include the text
    searched.
    """
