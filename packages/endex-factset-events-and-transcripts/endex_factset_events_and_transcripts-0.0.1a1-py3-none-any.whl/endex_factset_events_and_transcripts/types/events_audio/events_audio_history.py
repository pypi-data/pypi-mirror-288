# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["EventsAudioHistory", "Data"]


class Data(BaseModel):
    file_count: Optional[int] = FieldInfo(alias="fileCount", default=None)
    """The count of the files."""

    file_name: Optional[str] = FieldInfo(alias="fileName", default=None)
    """The name of the file."""

    file_size: Optional[int] = FieldInfo(alias="fileSize", default=None)
    """The size of the file, in bytes."""

    trimmed: Optional[bool] = None
    """
    True it signifies that the pre-signed URL for downloading includes trimmed
    historical audio recordings along with their metadata for a specific year.

    False it signifies that the pre-signed URL for downloading contains the
    untrimmed historical audio recordings along with their relevant metadata for a
    specific year.
    """

    url: Optional[str] = None
    """
    A pre-signed URL for downloading historical audio recordings and related
    metadata of a specific year. The URL provided in the response will expire after
    3 hours.
    """

    year: Optional[int] = None
    """
    The year corresponding to the file containing historical audio recordings that
    can be downloaded via presigned URL.
    """


class EventsAudioHistory(BaseModel):
    data: Optional[List[Data]] = None
