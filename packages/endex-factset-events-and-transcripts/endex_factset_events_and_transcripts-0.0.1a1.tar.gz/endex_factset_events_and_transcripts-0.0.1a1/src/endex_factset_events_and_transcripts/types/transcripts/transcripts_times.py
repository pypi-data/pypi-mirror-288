# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date, datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["TranscriptsTimes", "Data", "Meta", "MetaPagination"]


class Data(BaseModel):
    all_ids: Optional[List[str]] = FieldInfo(alias="allIds", default=None)
    """Refers to all companies mentioned in the document."""

    categories: Optional[List[str]] = None
    """Categories are country, industry, and subject codes.

    This is a comma-separated list.
    """

    event_date: Optional[date] = FieldInfo(alias="eventDate", default=None)
    """The date when the event took place. Formatted as 'YYYY-MM-DD'."""

    event_id: Optional[str] = FieldInfo(alias="eventId", default=None)
    """ID of the conference call."""

    event_type: Optional[
        Literal[
            "Earnings",
            "Guidance",
            "AnalystsShareholdersMeeting",
            "ConferencePresentation",
            "SalesRevenue",
            "SpecialSituation",
        ]
    ] = FieldInfo(alias="eventType", default=None)
    """Specifies the type of event. Choose from the available options."""

    headline: Optional[str] = None
    """Headline of the story."""

    primary_ids: Optional[List[str]] = FieldInfo(alias="primaryIds", default=None)
    """Refers to the main companies a particular document pertains to."""

    report_id: Optional[str] = FieldInfo(alias="reportId", default=None)
    """
    This is a unique identifier for a specific transcript (audio or video) returned.
    """

    story_date_time: Optional[datetime] = FieldInfo(alias="storyDateTime", default=None)
    """Refers to either the date and time of the story, which is in UTC"""

    transcripts_link: Optional[str] = FieldInfo(alias="transcriptsLink", default=None)
    """
    This is a link for downloading the document with an expiration duration of 24
    hours.
    """

    transcript_type: Optional[Literal["Raw", "Corrected"]] = FieldInfo(alias="transcriptType", default=None)
    """Specifies the type of transcript."""

    upload_date_time: Optional[datetime] = FieldInfo(alias="uploadDateTime", default=None)
    """It is the time when transcript is created, which is in UTC."""

    version_id: Optional[str] = FieldInfo(alias="versionId", default=None)
    """Used to distinguish the corrected reports.

    As such, one `reportId` can have many `versionIds`.
    """


class MetaPagination(BaseModel):
    is_estimated_total: Optional[bool] = FieldInfo(alias="isEstimatedTotal", default=None)
    """
    This field acts as a flag for the exact count of results and is defaulted to
    false as the API should always return the exact count of results.
    """

    total: Optional[int] = None
    """Total number of files the API returns for a particular query."""


class Meta(BaseModel):
    pagination: Optional[MetaPagination] = None
    """Pagination Object"""


class TranscriptsTimes(BaseModel):
    data: Optional[List[Data]] = None
    """Collection of data elements."""

    meta: Optional[Meta] = None
    """Meta Object"""
