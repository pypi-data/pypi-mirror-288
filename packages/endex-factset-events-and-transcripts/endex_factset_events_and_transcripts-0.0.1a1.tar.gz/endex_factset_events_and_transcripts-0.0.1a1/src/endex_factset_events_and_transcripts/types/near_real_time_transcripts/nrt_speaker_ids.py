# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["NrtSpeakerIDs", "Data", "Meta", "MetaPagination"]


class Data(BaseModel):
    affiliation_id: Optional[str] = FieldInfo(alias="affiliationId", default=None)
    """
    The affiliationId represents the entity ID associated with the organization or
    company to which the speaker is affiliated.
    """

    audio_source_id: Optional[int] = FieldInfo(alias="audioSourceId", default=None)
    """The Unique ID for an Internal recording specific to reportID.

    For example, ReportID X would have multiple recordings from a different source
    (dial-in or webcast). One ReportID can have multiple audioSourceIDs.
    """

    confidence_score: Optional[float] = FieldInfo(alias="confidenceScore", default=None)
    """The Confidence score similarity for a particular speaker.

    A score >= 0.49 while a speaker is speaking can be considered as a high
    confidence in the predicted speaker.

    Only the speakerIDs with confidenceScore >= 0.49 are rendered in the result set.
    """

    speaker_id: Optional[str] = FieldInfo(alias="speakerId", default=None)
    """A unique identifier for a speaker.

    You can find speakerIds within
    [FactSet People API](https://developer.factset.com/api-catalog/factset-people-api).
    """

    speaker_start_offset: Optional[float] = FieldInfo(alias="speakerStartOffset", default=None)
    """The number of seconds into the call when a speaker starts / is speaking."""


class MetaPagination(BaseModel):
    is_estimated_total: Optional[bool] = FieldInfo(alias="isEstimatedTotal", default=None)
    """
    Boolean value that represents whether the total count of results returned is
    exact or an estimate. This is defaulted to False as the API should always return
    the exact count.
    """

    total: Optional[int] = None
    """Total number of results the API returns for a particular query."""


class Meta(BaseModel):
    pagination: Optional[MetaPagination] = None


class NrtSpeakerIDs(BaseModel):
    data: Optional[List[Data]] = None

    meta: Optional[Meta] = None
