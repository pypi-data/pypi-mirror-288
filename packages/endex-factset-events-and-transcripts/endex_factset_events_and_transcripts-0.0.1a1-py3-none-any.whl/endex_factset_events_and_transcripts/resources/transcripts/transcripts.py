# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .ids import (
    IDsResource,
    AsyncIDsResource,
    IDsResourceWithRawResponse,
    AsyncIDsResourceWithRawResponse,
    IDsResourceWithStreamingResponse,
    AsyncIDsResourceWithStreamingResponse,
)
from .dates import (
    DatesResource,
    AsyncDatesResource,
    DatesResourceWithRawResponse,
    AsyncDatesResourceWithRawResponse,
    DatesResourceWithStreamingResponse,
    AsyncDatesResourceWithStreamingResponse,
)
from .times import (
    TimesResource,
    AsyncTimesResource,
    TimesResourceWithRawResponse,
    AsyncTimesResourceWithRawResponse,
    TimesResourceWithStreamingResponse,
    AsyncTimesResourceWithStreamingResponse,
)
from .events import (
    EventsResource,
    AsyncEventsResource,
    EventsResourceWithRawResponse,
    AsyncEventsResourceWithRawResponse,
    EventsResourceWithStreamingResponse,
    AsyncEventsResourceWithStreamingResponse,
)
from .search import (
    SearchResource,
    AsyncSearchResource,
    SearchResourceWithRawResponse,
    AsyncSearchResourceWithRawResponse,
    SearchResourceWithStreamingResponse,
    AsyncSearchResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["TranscriptsResource", "AsyncTranscriptsResource"]


class TranscriptsResource(SyncAPIResource):
    @cached_property
    def dates(self) -> DatesResource:
        return DatesResource(self._client)

    @cached_property
    def times(self) -> TimesResource:
        return TimesResource(self._client)

    @cached_property
    def search(self) -> SearchResource:
        return SearchResource(self._client)

    @cached_property
    def ids(self) -> IDsResource:
        return IDsResource(self._client)

    @cached_property
    def events(self) -> EventsResource:
        return EventsResource(self._client)

    @cached_property
    def with_raw_response(self) -> TranscriptsResourceWithRawResponse:
        return TranscriptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TranscriptsResourceWithStreamingResponse:
        return TranscriptsResourceWithStreamingResponse(self)


class AsyncTranscriptsResource(AsyncAPIResource):
    @cached_property
    def dates(self) -> AsyncDatesResource:
        return AsyncDatesResource(self._client)

    @cached_property
    def times(self) -> AsyncTimesResource:
        return AsyncTimesResource(self._client)

    @cached_property
    def search(self) -> AsyncSearchResource:
        return AsyncSearchResource(self._client)

    @cached_property
    def ids(self) -> AsyncIDsResource:
        return AsyncIDsResource(self._client)

    @cached_property
    def events(self) -> AsyncEventsResource:
        return AsyncEventsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTranscriptsResourceWithRawResponse:
        return AsyncTranscriptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTranscriptsResourceWithStreamingResponse:
        return AsyncTranscriptsResourceWithStreamingResponse(self)


class TranscriptsResourceWithRawResponse:
    def __init__(self, transcripts: TranscriptsResource) -> None:
        self._transcripts = transcripts

    @cached_property
    def dates(self) -> DatesResourceWithRawResponse:
        return DatesResourceWithRawResponse(self._transcripts.dates)

    @cached_property
    def times(self) -> TimesResourceWithRawResponse:
        return TimesResourceWithRawResponse(self._transcripts.times)

    @cached_property
    def search(self) -> SearchResourceWithRawResponse:
        return SearchResourceWithRawResponse(self._transcripts.search)

    @cached_property
    def ids(self) -> IDsResourceWithRawResponse:
        return IDsResourceWithRawResponse(self._transcripts.ids)

    @cached_property
    def events(self) -> EventsResourceWithRawResponse:
        return EventsResourceWithRawResponse(self._transcripts.events)


class AsyncTranscriptsResourceWithRawResponse:
    def __init__(self, transcripts: AsyncTranscriptsResource) -> None:
        self._transcripts = transcripts

    @cached_property
    def dates(self) -> AsyncDatesResourceWithRawResponse:
        return AsyncDatesResourceWithRawResponse(self._transcripts.dates)

    @cached_property
    def times(self) -> AsyncTimesResourceWithRawResponse:
        return AsyncTimesResourceWithRawResponse(self._transcripts.times)

    @cached_property
    def search(self) -> AsyncSearchResourceWithRawResponse:
        return AsyncSearchResourceWithRawResponse(self._transcripts.search)

    @cached_property
    def ids(self) -> AsyncIDsResourceWithRawResponse:
        return AsyncIDsResourceWithRawResponse(self._transcripts.ids)

    @cached_property
    def events(self) -> AsyncEventsResourceWithRawResponse:
        return AsyncEventsResourceWithRawResponse(self._transcripts.events)


class TranscriptsResourceWithStreamingResponse:
    def __init__(self, transcripts: TranscriptsResource) -> None:
        self._transcripts = transcripts

    @cached_property
    def dates(self) -> DatesResourceWithStreamingResponse:
        return DatesResourceWithStreamingResponse(self._transcripts.dates)

    @cached_property
    def times(self) -> TimesResourceWithStreamingResponse:
        return TimesResourceWithStreamingResponse(self._transcripts.times)

    @cached_property
    def search(self) -> SearchResourceWithStreamingResponse:
        return SearchResourceWithStreamingResponse(self._transcripts.search)

    @cached_property
    def ids(self) -> IDsResourceWithStreamingResponse:
        return IDsResourceWithStreamingResponse(self._transcripts.ids)

    @cached_property
    def events(self) -> EventsResourceWithStreamingResponse:
        return EventsResourceWithStreamingResponse(self._transcripts.events)


class AsyncTranscriptsResourceWithStreamingResponse:
    def __init__(self, transcripts: AsyncTranscriptsResource) -> None:
        self._transcripts = transcripts

    @cached_property
    def dates(self) -> AsyncDatesResourceWithStreamingResponse:
        return AsyncDatesResourceWithStreamingResponse(self._transcripts.dates)

    @cached_property
    def times(self) -> AsyncTimesResourceWithStreamingResponse:
        return AsyncTimesResourceWithStreamingResponse(self._transcripts.times)

    @cached_property
    def search(self) -> AsyncSearchResourceWithStreamingResponse:
        return AsyncSearchResourceWithStreamingResponse(self._transcripts.search)

    @cached_property
    def ids(self) -> AsyncIDsResourceWithStreamingResponse:
        return AsyncIDsResourceWithStreamingResponse(self._transcripts.ids)

    @cached_property
    def events(self) -> AsyncEventsResourceWithStreamingResponse:
        return AsyncEventsResourceWithStreamingResponse(self._transcripts.events)
