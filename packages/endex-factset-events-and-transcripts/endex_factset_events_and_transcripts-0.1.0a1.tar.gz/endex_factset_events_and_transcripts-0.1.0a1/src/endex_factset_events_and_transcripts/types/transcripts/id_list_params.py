# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["IDListParams"]


class IDListParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["storyDateTime", "-storyDateTime"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDate.
    """

    categories: List[str]
    """Code for categories to include.

    This is a comma-separated list.which represent country, industry, and subject
    codes. Use the `/reference/categories` endpoint to get the list of available
    categories.

    Default = All categories.
    """

    ids: List[str]
    """Requested symbols or securities.

    This is a comma-separated list with a maximum limit of 1000. Each symbol can be
    a FactSet exchange symbol, CUSIP, or SEDOL.
    """

    primary_id: Annotated[Literal[True, False], PropertyInfo(alias="primaryId")]
    """Type of identifier search

    - true - Returns headlines of stories that have the searched identifier(s) as
      the primary identifier.
    - false - Returns headlines of stories that mentioned or referred to the
      identifier.
    """

    report_ids: Annotated[List[str], PropertyInfo(alias="reportIds")]
    """Requests Report IDs.

    This is a comma-separated list with a maximum limit of 1000
    """
