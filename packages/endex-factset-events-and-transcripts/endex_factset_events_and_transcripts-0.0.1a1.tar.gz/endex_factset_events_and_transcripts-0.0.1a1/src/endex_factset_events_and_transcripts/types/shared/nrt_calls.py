# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["NrtCalls", "Data", "Meta", "MetaPagination"]


class Data(BaseModel):
    audio_source_id: Optional[int] = FieldInfo(alias="audioSourceId", default=None)
    """Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from different source
    (dial-in - P or webcast - W). One reportId can have multiple audiosourceIDs.
    """

    call_status: Optional[Literal["InProgress", "Ended", "EndedWithoutNotification", "IssueAtSource"]] = FieldInfo(
        alias="callStatus", default=None
    )
    """Status of the call i.e.

    Ended, InProgress, EndedWithoutNotification, or IssueAtSource.

    - InProgress - the call is in progress.
    - Ended - the call has ended.
    - EndedWithoutNotification - the call has technically ended and can be
      considered as ended but is missing a notification from the upstream systems.
    - IssueAtSource - the call has ended with no snippet data due to a possible
      issue at the source.
    """

    entity_id: Optional[str] = FieldInfo(alias="entityId", default=None)
    """Factset entity level identifier for the company hosting the event."""

    event_datetime_utc: Optional[datetime] = FieldInfo(alias="eventDatetimeUtc", default=None)
    """The official UTC timestamp of the start of the event."""

    event_title: Optional[str] = FieldInfo(alias="eventTitle", default=None)
    """Title of the Event."""

    event_type: Optional[
        Literal[
            "AnalystsInvestorsShareholdersMeeting",
            "EarningsCall",
            "EarningsRelease",
            "Guidance",
            "SalesRevenueCall",
            "SalesRevenueRelease",
            "SpecialSituation",
        ]
    ] = FieldInfo(alias="eventType", default=None)
    """Refers to the various event types covered by FactSet CallStreet."""

    recording_start_time: Optional[datetime] = FieldInfo(alias="recordingStartTime", default=None)

    report_id: Optional[int] = FieldInfo(alias="reportId", default=None)
    """The unique ID for an event."""

    source_code: Optional[Literal["PhoneReplay", "Webcast"]] = FieldInfo(alias="sourceCode", default=None)
    """
    Identifier for the source of how the event is recorded. PhoneReplay: Event is
    recorded through a phone replay Webcast: Event is recorded through a webcast.
    """

    ticker: Optional[str] = None
    """Ticker-region identifier for the company hosting the event."""


class MetaPagination(BaseModel):
    is_estimated_total: Optional[bool] = FieldInfo(alias="isEstimatedTotal", default=None)
    """
    This field acts as a flag for the exact count of results and is defaulted to
    false as the API should always return the exact count of results.
    """

    total: Optional[int] = None
    """Total number for results returned for a specific query."""


class Meta(BaseModel):
    pagination: Optional[MetaPagination] = None


class NrtCalls(BaseModel):
    data: Optional[List[Data]] = None

    meta: Optional[Meta] = None
