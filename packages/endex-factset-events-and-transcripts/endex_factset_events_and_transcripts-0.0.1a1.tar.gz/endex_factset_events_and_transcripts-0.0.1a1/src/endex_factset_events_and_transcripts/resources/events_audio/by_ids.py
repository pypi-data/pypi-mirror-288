# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.events_audio import by_id_retrieve_params
from ...types.events_audio.events_audio_daily_ids import EventsAudioDailyIDs

__all__ = ["ByIDsResource", "AsyncByIDsResource"]


class ByIDsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ByIDsResourceWithRawResponse:
        return ByIDsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ByIDsResourceWithStreamingResponse:
        return ByIDsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        audio_source_id: int | NotGiven = NOT_GIVEN,
        report_id: int | NotGiven = NOT_GIVEN,
        trimmed: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDailyIDs:
        """
        Retrieves the latest audio recordings based on the provided report ID and audio
        source ID.

        Args:
          audio_source_id: Unique ID for an Internal recording specific to reportID. For example, ReportID
              X would have multiple recordings from different source (phone or webcast or
              vendor or replay). One ReportID can have multiple AudioSourceIDs.

          report_id: Unique identifier for fetching the audio file for an event. The same ID is used
              for the transcript of the same event.

          trimmed: This parameters helps to search trimmed audio files.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/audio/by-ids",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "audio_source_id": audio_source_id,
                        "report_id": report_id,
                        "trimmed": trimmed,
                    },
                    by_id_retrieve_params.ByIDRetrieveParams,
                ),
            ),
            cast_to=EventsAudioDailyIDs,
        )


class AsyncByIDsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncByIDsResourceWithRawResponse:
        return AsyncByIDsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncByIDsResourceWithStreamingResponse:
        return AsyncByIDsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        audio_source_id: int | NotGiven = NOT_GIVEN,
        report_id: int | NotGiven = NOT_GIVEN,
        trimmed: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDailyIDs:
        """
        Retrieves the latest audio recordings based on the provided report ID and audio
        source ID.

        Args:
          audio_source_id: Unique ID for an Internal recording specific to reportID. For example, ReportID
              X would have multiple recordings from different source (phone or webcast or
              vendor or replay). One ReportID can have multiple AudioSourceIDs.

          report_id: Unique identifier for fetching the audio file for an event. The same ID is used
              for the transcript of the same event.

          trimmed: This parameters helps to search trimmed audio files.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/audio/by-ids",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "audio_source_id": audio_source_id,
                        "report_id": report_id,
                        "trimmed": trimmed,
                    },
                    by_id_retrieve_params.ByIDRetrieveParams,
                ),
            ),
            cast_to=EventsAudioDailyIDs,
        )


class ByIDsResourceWithRawResponse:
    def __init__(self, by_ids: ByIDsResource) -> None:
        self._by_ids = by_ids

        self.retrieve = to_raw_response_wrapper(
            by_ids.retrieve,
        )


class AsyncByIDsResourceWithRawResponse:
    def __init__(self, by_ids: AsyncByIDsResource) -> None:
        self._by_ids = by_ids

        self.retrieve = async_to_raw_response_wrapper(
            by_ids.retrieve,
        )


class ByIDsResourceWithStreamingResponse:
    def __init__(self, by_ids: ByIDsResource) -> None:
        self._by_ids = by_ids

        self.retrieve = to_streamed_response_wrapper(
            by_ids.retrieve,
        )


class AsyncByIDsResourceWithStreamingResponse:
    def __init__(self, by_ids: AsyncByIDsResource) -> None:
        self._by_ids = by_ids

        self.retrieve = async_to_streamed_response_wrapper(
            by_ids.retrieve,
        )
