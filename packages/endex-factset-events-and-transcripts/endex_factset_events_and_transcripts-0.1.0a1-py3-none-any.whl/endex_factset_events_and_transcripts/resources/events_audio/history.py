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
from ...types.events_audio import history_retrieve_params
from ...types.events_audio.events_audio_history import EventsAudioHistory

__all__ = ["HistoryResource", "AsyncHistoryResource"]


class HistoryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        year: int,
        trimmed: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioHistory:
        """
        This endpoint retrieves an object containing a pre-signed URL from which an
        archive of all audio data for a specified year can be downloaded.

        - Returns **untrimmed** historical audio recordings, which include complete
          audio files such as intro music & non-speaking portions, and related metadata
          dating back from May 10, 2011 to Sep 30, 2022.

        - Returns **trimmed** historical audio recordings, which are audio files with
          the non-speaking portions removed, and related metadata dating back from May
          10, 2011 to Dec 31, 2022.

        Args:
          year: Specifies the year for which the historical audio recordings and related
              metadata are to be retrieved.

          trimmed: Specifies if trimmed/untrimmed historical audio recordings should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/audio/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "year": year,
                        "trimmed": trimmed,
                    },
                    history_retrieve_params.HistoryRetrieveParams,
                ),
            ),
            cast_to=EventsAudioHistory,
        )


class AsyncHistoryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        year: int,
        trimmed: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioHistory:
        """
        This endpoint retrieves an object containing a pre-signed URL from which an
        archive of all audio data for a specified year can be downloaded.

        - Returns **untrimmed** historical audio recordings, which include complete
          audio files such as intro music & non-speaking portions, and related metadata
          dating back from May 10, 2011 to Sep 30, 2022.

        - Returns **trimmed** historical audio recordings, which are audio files with
          the non-speaking portions removed, and related metadata dating back from May
          10, 2011 to Dec 31, 2022.

        Args:
          year: Specifies the year for which the historical audio recordings and related
              metadata are to be retrieved.

          trimmed: Specifies if trimmed/untrimmed historical audio recordings should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/audio/history",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "year": year,
                        "trimmed": trimmed,
                    },
                    history_retrieve_params.HistoryRetrieveParams,
                ),
            ),
            cast_to=EventsAudioHistory,
        )


class HistoryResourceWithRawResponse:
    def __init__(self, history: HistoryResource) -> None:
        self._history = history

        self.retrieve = to_raw_response_wrapper(
            history.retrieve,
        )


class AsyncHistoryResourceWithRawResponse:
    def __init__(self, history: AsyncHistoryResource) -> None:
        self._history = history

        self.retrieve = async_to_raw_response_wrapper(
            history.retrieve,
        )


class HistoryResourceWithStreamingResponse:
    def __init__(self, history: HistoryResource) -> None:
        self._history = history

        self.retrieve = to_streamed_response_wrapper(
            history.retrieve,
        )


class AsyncHistoryResourceWithStreamingResponse:
    def __init__(self, history: AsyncHistoryResource) -> None:
        self._history = history

        self.retrieve = async_to_streamed_response_wrapper(
            history.retrieve,
        )
