# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "IndexedNrt",
    "Data",
    "DataTranscriptData",
    "DataTranscriptDataIndexedData",
    "DataTranscriptDataIndexedDataIndex",
    "DataTranscriptDataSnippetData",
]


class DataTranscriptDataIndexedDataIndex(BaseModel):
    confidence: Optional[float] = None
    """
    Represents the confidence with which the speech to text recognition engine
    predicts. 1 represents 100% confidence about the content.
    """

    content: Optional[str] = None
    """It denotes the spoken content."""

    language: Optional[str] = None
    """It denotes the spoken language. Its always english."""


class DataTranscriptDataIndexedData(BaseModel):
    end_time: Optional[float] = FieldInfo(alias="endTime", default=None)
    """The number of seconds into the call, when the content ends."""

    index: Optional[List[DataTranscriptDataIndexedDataIndex]] = None

    is_end_of_sentence: Optional[bool] = FieldInfo(alias="isEndOfSentence", default=None)
    """This parameter indicates if the current content signifies the end of a sentence.

    It returns true when the type is punctuation and the content is a period '.'. It
    does not return true if a sentence ends with a question mark or an exclamation
    mark.
    """

    start_time: Optional[float] = FieldInfo(alias="startTime", default=None)
    """The number of seconds into the call, when the content begins."""

    type: Optional[Literal["Punctuation", "Word", "SpeakerChange"]] = None
    """It denotes the type of content. Values- Punctuation, Word, SpeakerChange"""


class DataTranscriptDataSnippetData(BaseModel):
    end_time: Optional[float] = FieldInfo(alias="endTime", default=None)
    """The number of seconds into the call,when the transcript snippet ended."""

    start_time: Optional[float] = FieldInfo(alias="startTime", default=None)
    """The number of seconds into the call,when the transcript snippet started."""

    transcript: Optional[str] = None
    """The actual transcript snippet."""


class DataTranscriptData(BaseModel):
    indexed_data: Optional[List[DataTranscriptDataIndexedData]] = FieldInfo(alias="indexedData", default=None)

    snippet_data: Optional[DataTranscriptDataSnippetData] = FieldInfo(alias="snippetData", default=None)


class Data(BaseModel):
    audio_source_id: Optional[int] = FieldInfo(alias="audioSourceId", default=None)
    """The Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from a different source
    (dial-in or webcast). One ReportID can have multiple audioSourceIDs.
    """

    snippet_end_timestamp: Optional[datetime] = FieldInfo(alias="snippetEndTimestamp", default=None)
    """
    The snippet end time is calculated based off the endTime in the snippetData
    section and the recordingStartTime from the calls endpoint.
    """

    snippet_sequence: Optional[int] = FieldInfo(alias="snippetSequence", default=None)
    """The sequence number of the snippet from the start of the current call."""

    transcript_data: Optional[List[DataTranscriptData]] = FieldInfo(alias="transcriptData", default=None)


class IndexedNrt(BaseModel):
    data: Optional[List[Data]] = None
