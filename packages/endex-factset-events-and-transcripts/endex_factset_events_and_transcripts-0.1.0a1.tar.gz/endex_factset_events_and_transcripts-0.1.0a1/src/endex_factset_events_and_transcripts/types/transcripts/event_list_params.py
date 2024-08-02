# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    _sort: List[Literal["storyDateTime", "-storyDateTime"]]
    """
    Enables sorting data in ascending or descending chronological order based on
    eventDate.
    """

    event_ids: Annotated[List[str], PropertyInfo(alias="eventIds")]
    """Requests Event IDs.

    This is a comma-separated list with a maximum limit of 1000.
    """

    event_type: Annotated[
        Literal[
            "Earnings",
            "Guidance",
            "AnalystsShareholdersMeeting",
            "ConferencePresentation",
            "SalesRevenue",
            "SpecialSituation",
        ],
        PropertyInfo(alias="eventType"),
    ]
    """
    Specifies the type of event you want to retrieve. Earnings - Denotes an Earnings
    event. Guidance - Denotes a Guidance event. AnalystsShareholdersMeeting -
    Denotes an Analysts and Shareholders Meeting event. ConferencePresentation -
    Denotes a Conference Presentation event. SalesRevenue - Denotes a Sales/Revenue
    event. SpecialSituation - Denotes a Special Situation event (i.e.
    Merger/Acquisition).
    """
