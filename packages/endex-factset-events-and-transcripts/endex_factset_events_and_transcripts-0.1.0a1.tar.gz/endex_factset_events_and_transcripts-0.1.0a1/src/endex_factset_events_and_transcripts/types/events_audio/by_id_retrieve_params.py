# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ByIDRetrieveParams"]


class ByIDRetrieveParams(TypedDict, total=False):
    audio_source_id: Annotated[int, PropertyInfo(alias="audioSourceId")]
    """Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from different source
    (phone or webcast or vendor or replay). One ReportID can have multiple
    AudioSourceIDs.
    """

    report_id: Annotated[int, PropertyInfo(alias="reportId")]
    """Unique identifier for fetching the audio file for an event.

    The same ID is used for the transcript of the same event.
    """

    trimmed: bool
    """This parameters helps to search trimmed audio files."""
