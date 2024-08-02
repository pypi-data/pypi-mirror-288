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
from .indexed import (
    IndexedResource,
    AsyncIndexedResource,
    IndexedResourceWithRawResponse,
    AsyncIndexedResourceWithRawResponse,
    IndexedResourceWithStreamingResponse,
    AsyncIndexedResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .by_ticker import (
    ByTickerResource,
    AsyncByTickerResource,
    ByTickerResourceWithRawResponse,
    AsyncByTickerResourceWithRawResponse,
    ByTickerResourceWithStreamingResponse,
    AsyncByTickerResourceWithStreamingResponse,
)
from .speakerids import (
    SpeakeridsResource,
    AsyncSpeakeridsResource,
    SpeakeridsResourceWithRawResponse,
    AsyncSpeakeridsResourceWithRawResponse,
    SpeakeridsResourceWithStreamingResponse,
    AsyncSpeakeridsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["NearRealTimeTranscriptsResource", "AsyncNearRealTimeTranscriptsResource"]


class NearRealTimeTranscriptsResource(SyncAPIResource):
    @cached_property
    def by_ticker(self) -> ByTickerResource:
        return ByTickerResource(self._client)

    @cached_property
    def by_ids(self) -> ByIDsResource:
        return ByIDsResource(self._client)

    @cached_property
    def speakerids(self) -> SpeakeridsResource:
        return SpeakeridsResource(self._client)

    @cached_property
    def indexed(self) -> IndexedResource:
        return IndexedResource(self._client)

    @cached_property
    def with_raw_response(self) -> NearRealTimeTranscriptsResourceWithRawResponse:
        return NearRealTimeTranscriptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NearRealTimeTranscriptsResourceWithStreamingResponse:
        return NearRealTimeTranscriptsResourceWithStreamingResponse(self)


class AsyncNearRealTimeTranscriptsResource(AsyncAPIResource):
    @cached_property
    def by_ticker(self) -> AsyncByTickerResource:
        return AsyncByTickerResource(self._client)

    @cached_property
    def by_ids(self) -> AsyncByIDsResource:
        return AsyncByIDsResource(self._client)

    @cached_property
    def speakerids(self) -> AsyncSpeakeridsResource:
        return AsyncSpeakeridsResource(self._client)

    @cached_property
    def indexed(self) -> AsyncIndexedResource:
        return AsyncIndexedResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncNearRealTimeTranscriptsResourceWithRawResponse:
        return AsyncNearRealTimeTranscriptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNearRealTimeTranscriptsResourceWithStreamingResponse:
        return AsyncNearRealTimeTranscriptsResourceWithStreamingResponse(self)


class NearRealTimeTranscriptsResourceWithRawResponse:
    def __init__(self, near_real_time_transcripts: NearRealTimeTranscriptsResource) -> None:
        self._near_real_time_transcripts = near_real_time_transcripts

    @cached_property
    def by_ticker(self) -> ByTickerResourceWithRawResponse:
        return ByTickerResourceWithRawResponse(self._near_real_time_transcripts.by_ticker)

    @cached_property
    def by_ids(self) -> ByIDsResourceWithRawResponse:
        return ByIDsResourceWithRawResponse(self._near_real_time_transcripts.by_ids)

    @cached_property
    def speakerids(self) -> SpeakeridsResourceWithRawResponse:
        return SpeakeridsResourceWithRawResponse(self._near_real_time_transcripts.speakerids)

    @cached_property
    def indexed(self) -> IndexedResourceWithRawResponse:
        return IndexedResourceWithRawResponse(self._near_real_time_transcripts.indexed)


class AsyncNearRealTimeTranscriptsResourceWithRawResponse:
    def __init__(self, near_real_time_transcripts: AsyncNearRealTimeTranscriptsResource) -> None:
        self._near_real_time_transcripts = near_real_time_transcripts

    @cached_property
    def by_ticker(self) -> AsyncByTickerResourceWithRawResponse:
        return AsyncByTickerResourceWithRawResponse(self._near_real_time_transcripts.by_ticker)

    @cached_property
    def by_ids(self) -> AsyncByIDsResourceWithRawResponse:
        return AsyncByIDsResourceWithRawResponse(self._near_real_time_transcripts.by_ids)

    @cached_property
    def speakerids(self) -> AsyncSpeakeridsResourceWithRawResponse:
        return AsyncSpeakeridsResourceWithRawResponse(self._near_real_time_transcripts.speakerids)

    @cached_property
    def indexed(self) -> AsyncIndexedResourceWithRawResponse:
        return AsyncIndexedResourceWithRawResponse(self._near_real_time_transcripts.indexed)


class NearRealTimeTranscriptsResourceWithStreamingResponse:
    def __init__(self, near_real_time_transcripts: NearRealTimeTranscriptsResource) -> None:
        self._near_real_time_transcripts = near_real_time_transcripts

    @cached_property
    def by_ticker(self) -> ByTickerResourceWithStreamingResponse:
        return ByTickerResourceWithStreamingResponse(self._near_real_time_transcripts.by_ticker)

    @cached_property
    def by_ids(self) -> ByIDsResourceWithStreamingResponse:
        return ByIDsResourceWithStreamingResponse(self._near_real_time_transcripts.by_ids)

    @cached_property
    def speakerids(self) -> SpeakeridsResourceWithStreamingResponse:
        return SpeakeridsResourceWithStreamingResponse(self._near_real_time_transcripts.speakerids)

    @cached_property
    def indexed(self) -> IndexedResourceWithStreamingResponse:
        return IndexedResourceWithStreamingResponse(self._near_real_time_transcripts.indexed)


class AsyncNearRealTimeTranscriptsResourceWithStreamingResponse:
    def __init__(self, near_real_time_transcripts: AsyncNearRealTimeTranscriptsResource) -> None:
        self._near_real_time_transcripts = near_real_time_transcripts

    @cached_property
    def by_ticker(self) -> AsyncByTickerResourceWithStreamingResponse:
        return AsyncByTickerResourceWithStreamingResponse(self._near_real_time_transcripts.by_ticker)

    @cached_property
    def by_ids(self) -> AsyncByIDsResourceWithStreamingResponse:
        return AsyncByIDsResourceWithStreamingResponse(self._near_real_time_transcripts.by_ids)

    @cached_property
    def speakerids(self) -> AsyncSpeakeridsResourceWithStreamingResponse:
        return AsyncSpeakeridsResourceWithStreamingResponse(self._near_real_time_transcripts.speakerids)

    @cached_property
    def indexed(self) -> AsyncIndexedResourceWithStreamingResponse:
        return AsyncIndexedResourceWithStreamingResponse(self._near_real_time_transcripts.indexed)
