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
from ...types.events_audio import by_file_name_retrieve_params
from ...types.events_audio.events_audio_daily_file_name import EventsAudioDailyFileName

__all__ = ["ByFileNameResource", "AsyncByFileNameResource"]


class ByFileNameResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ByFileNameResourceWithRawResponse:
        return ByFileNameResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ByFileNameResourceWithStreamingResponse:
        return ByFileNameResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        file_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDailyFileName:
        """
        Retrieves the latest audio recordings corresponding to the provided file name.

        Args:
          file_name: This parameter is used to filter the data on based on the file name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/audio/by-file-name",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"file_name": file_name}, by_file_name_retrieve_params.ByFileNameRetrieveParams),
            ),
            cast_to=EventsAudioDailyFileName,
        )


class AsyncByFileNameResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncByFileNameResourceWithRawResponse:
        return AsyncByFileNameResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncByFileNameResourceWithStreamingResponse:
        return AsyncByFileNameResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        file_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDailyFileName:
        """
        Retrieves the latest audio recordings corresponding to the provided file name.

        Args:
          file_name: This parameter is used to filter the data on based on the file name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/audio/by-file-name",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"file_name": file_name}, by_file_name_retrieve_params.ByFileNameRetrieveParams
                ),
            ),
            cast_to=EventsAudioDailyFileName,
        )


class ByFileNameResourceWithRawResponse:
    def __init__(self, by_file_name: ByFileNameResource) -> None:
        self._by_file_name = by_file_name

        self.retrieve = to_raw_response_wrapper(
            by_file_name.retrieve,
        )


class AsyncByFileNameResourceWithRawResponse:
    def __init__(self, by_file_name: AsyncByFileNameResource) -> None:
        self._by_file_name = by_file_name

        self.retrieve = async_to_raw_response_wrapper(
            by_file_name.retrieve,
        )


class ByFileNameResourceWithStreamingResponse:
    def __init__(self, by_file_name: ByFileNameResource) -> None:
        self._by_file_name = by_file_name

        self.retrieve = to_streamed_response_wrapper(
            by_file_name.retrieve,
        )


class AsyncByFileNameResourceWithStreamingResponse:
    def __init__(self, by_file_name: AsyncByFileNameResource) -> None:
        self._by_file_name = by_file_name

        self.retrieve = async_to_streamed_response_wrapper(
            by_file_name.retrieve,
        )
