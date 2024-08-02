# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["EventsAudioDailyIDs", "Data"]


class Data(BaseModel):
    audio_source_id: Optional[int] = FieldInfo(alias="audioSourceId", default=None)
    """Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from different source
    (Phone or Webcast or Vendor or Replay). One ReportID can have multiple
    AudioSourceIDs.

    The audioSourceId identifier is available for audio calls since November
    29, 2022. Only un-trimmed audio files contain an audioSourceId value. All the
    vendor and trimmed audio files will have an audioSourceId value of null.
    """

    bitrate: Optional[float] = None
    """The total number of bits of information stored per second of sound in Kbps."""

    duration_secs: Optional[float] = FieldInfo(alias="durationSecs", default=None)
    """
    Total duration of the recording in seconds based on startOffsetSeconds to
    endOffsetSeconds.
    """

    end_offset_seconds: Optional[float] = FieldInfo(alias="endOffsetSeconds", default=None)
    """
    The delta in seconds between startTime to when FactSet marks the end of the
    call.
    """

    end_time: Optional[str] = FieldInfo(alias="endTime", default=None)
    """The official timestamp when FactSet ends the recording."""

    entity_id: Optional[str] = FieldInfo(alias="entityId", default=None)
    """FactSet entity level identifier for the company hosting the event."""

    file_name: Optional[str] = FieldInfo(alias="fileName", default=None)
    """The filename of the audio file."""

    file_size: Optional[float] = FieldInfo(alias="fileSize", default=None)
    """Size of the Audio file, in bytes."""

    report_id: Optional[int] = FieldInfo(alias="reportId", default=None)
    """The unique ID of the audio file for an event.

    The same ID is used for the transcript of the same event. This report ID can
    also be used to map to the Event details in SDF tables.
    """

    sample_rate: Optional[float] = FieldInfo(alias="sampleRate", default=None)
    """The number of samples of audio carried per second in Kbps."""

    source_code: Optional[Literal["Webcast", "Vendor", "WebcastReplay", "Flash", "Replay", "Phone"]] = FieldInfo(
        alias="sourceCode", default=None
    )
    """This parameter filters the results based on Source of the Audio file.

    Below are the descriptions for each Source Code -

    - Phone = Originated from phone call
    - Webcast = Originated from a webcast
    - Vendor = Received from vendor
    - WebcastReplay = Replay of a webcast
    - Flash = Identical to webcast; can merge with "Webcast" in the future
    - Replay = Phone replay
    """

    start_offset_seconds: Optional[float] = FieldInfo(alias="startOffsetSeconds", default=None)
    """
    The delta in seconds between start of audio file to when FactSet marks the
    beginning of the call.
    """

    start_time: Optional[str] = FieldInfo(alias="startTime", default=None)
    """The official timestamp when FactSet begins the recording."""

    ticker: Optional[str] = None
    """Ticker-region identifier for the company hosting the event."""

    trimmed: Optional[bool] = None
    """The trimmed attribute indicates whether the audio is the trimmed version.

    If `sourceCode` is set to vendor, this attribute will always be true.
    """

    upload_time: Optional[str] = FieldInfo(alias="uploadTime", default=None)
    """The official timestamp when FactSet publishes the audio file externally."""

    url: Optional[str] = None
    """
    A pre-signed URL that allows downloading the audio file, expiring after 24
    hours.
    """


class EventsAudioDailyIDs(BaseModel):
    data: Optional[List[Data]] = None
