# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .by_ids import (
    ByIDsResource,
    AsyncByIDsResource,
    ByIDsResourceWithRawResponse,
    AsyncByIDsResourceWithRawResponse,
    ByIDsResourceWithStreamingResponse,
    AsyncByIDsResourceWithStreamingResponse,
)
from .by_date import (
    ByDateResource,
    AsyncByDateResource,
    ByDateResourceWithRawResponse,
    AsyncByDateResourceWithRawResponse,
    ByDateResourceWithStreamingResponse,
    AsyncByDateResourceWithStreamingResponse,
)
from .history import (
    HistoryResource,
    AsyncHistoryResource,
    HistoryResourceWithRawResponse,
    AsyncHistoryResourceWithRawResponse,
    HistoryResourceWithStreamingResponse,
    AsyncHistoryResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .by_file_name import (
    ByFileNameResource,
    AsyncByFileNameResource,
    ByFileNameResourceWithRawResponse,
    AsyncByFileNameResourceWithRawResponse,
    ByFileNameResourceWithStreamingResponse,
    AsyncByFileNameResourceWithStreamingResponse,
)
from .by_upload_time import (
    ByUploadTimeResource,
    AsyncByUploadTimeResource,
    ByUploadTimeResourceWithRawResponse,
    AsyncByUploadTimeResourceWithRawResponse,
    ByUploadTimeResourceWithStreamingResponse,
    AsyncByUploadTimeResourceWithStreamingResponse,
)

__all__ = ["EventsAudioResource", "AsyncEventsAudioResource"]


class EventsAudioResource(SyncAPIResource):
    @cached_property
    def history(self) -> HistoryResource:
        return HistoryResource(self._client)

    @cached_property
    def by_date(self) -> ByDateResource:
        return ByDateResource(self._client)

    @cached_property
    def by_upload_time(self) -> ByUploadTimeResource:
        return ByUploadTimeResource(self._client)

    @cached_property
    def by_file_name(self) -> ByFileNameResource:
        return ByFileNameResource(self._client)

    @cached_property
    def by_ids(self) -> ByIDsResource:
        return ByIDsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EventsAudioResourceWithRawResponse:
        return EventsAudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsAudioResourceWithStreamingResponse:
        return EventsAudioResourceWithStreamingResponse(self)


class AsyncEventsAudioResource(AsyncAPIResource):
    @cached_property
    def history(self) -> AsyncHistoryResource:
        return AsyncHistoryResource(self._client)

    @cached_property
    def by_date(self) -> AsyncByDateResource:
        return AsyncByDateResource(self._client)

    @cached_property
    def by_upload_time(self) -> AsyncByUploadTimeResource:
        return AsyncByUploadTimeResource(self._client)

    @cached_property
    def by_file_name(self) -> AsyncByFileNameResource:
        return AsyncByFileNameResource(self._client)

    @cached_property
    def by_ids(self) -> AsyncByIDsResource:
        return AsyncByIDsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEventsAudioResourceWithRawResponse:
        return AsyncEventsAudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsAudioResourceWithStreamingResponse:
        return AsyncEventsAudioResourceWithStreamingResponse(self)


class EventsAudioResourceWithRawResponse:
    def __init__(self, events_audio: EventsAudioResource) -> None:
        self._events_audio = events_audio

    @cached_property
    def history(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self._events_audio.history)

    @cached_property
    def by_date(self) -> ByDateResourceWithRawResponse:
        return ByDateResourceWithRawResponse(self._events_audio.by_date)

    @cached_property
    def by_upload_time(self) -> ByUploadTimeResourceWithRawResponse:
        return ByUploadTimeResourceWithRawResponse(self._events_audio.by_upload_time)

    @cached_property
    def by_file_name(self) -> ByFileNameResourceWithRawResponse:
        return ByFileNameResourceWithRawResponse(self._events_audio.by_file_name)

    @cached_property
    def by_ids(self) -> ByIDsResourceWithRawResponse:
        return ByIDsResourceWithRawResponse(self._events_audio.by_ids)


class AsyncEventsAudioResourceWithRawResponse:
    def __init__(self, events_audio: AsyncEventsAudioResource) -> None:
        self._events_audio = events_audio

    @cached_property
    def history(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self._events_audio.history)

    @cached_property
    def by_date(self) -> AsyncByDateResourceWithRawResponse:
        return AsyncByDateResourceWithRawResponse(self._events_audio.by_date)

    @cached_property
    def by_upload_time(self) -> AsyncByUploadTimeResourceWithRawResponse:
        return AsyncByUploadTimeResourceWithRawResponse(self._events_audio.by_upload_time)

    @cached_property
    def by_file_name(self) -> AsyncByFileNameResourceWithRawResponse:
        return AsyncByFileNameResourceWithRawResponse(self._events_audio.by_file_name)

    @cached_property
    def by_ids(self) -> AsyncByIDsResourceWithRawResponse:
        return AsyncByIDsResourceWithRawResponse(self._events_audio.by_ids)


class EventsAudioResourceWithStreamingResponse:
    def __init__(self, events_audio: EventsAudioResource) -> None:
        self._events_audio = events_audio

    @cached_property
    def history(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self._events_audio.history)

    @cached_property
    def by_date(self) -> ByDateResourceWithStreamingResponse:
        return ByDateResourceWithStreamingResponse(self._events_audio.by_date)

    @cached_property
    def by_upload_time(self) -> ByUploadTimeResourceWithStreamingResponse:
        return ByUploadTimeResourceWithStreamingResponse(self._events_audio.by_upload_time)

    @cached_property
    def by_file_name(self) -> ByFileNameResourceWithStreamingResponse:
        return ByFileNameResourceWithStreamingResponse(self._events_audio.by_file_name)

    @cached_property
    def by_ids(self) -> ByIDsResourceWithStreamingResponse:
        return ByIDsResourceWithStreamingResponse(self._events_audio.by_ids)


class AsyncEventsAudioResourceWithStreamingResponse:
    def __init__(self, events_audio: AsyncEventsAudioResource) -> None:
        self._events_audio = events_audio

    @cached_property
    def history(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self._events_audio.history)

    @cached_property
    def by_date(self) -> AsyncByDateResourceWithStreamingResponse:
        return AsyncByDateResourceWithStreamingResponse(self._events_audio.by_date)

    @cached_property
    def by_upload_time(self) -> AsyncByUploadTimeResourceWithStreamingResponse:
        return AsyncByUploadTimeResourceWithStreamingResponse(self._events_audio.by_upload_time)

    @cached_property
    def by_file_name(self) -> AsyncByFileNameResourceWithStreamingResponse:
        return AsyncByFileNameResourceWithStreamingResponse(self._events_audio.by_file_name)

    @cached_property
    def by_ids(self) -> AsyncByIDsResourceWithStreamingResponse:
        return AsyncByIDsResourceWithStreamingResponse(self._events_audio.by_ids)
