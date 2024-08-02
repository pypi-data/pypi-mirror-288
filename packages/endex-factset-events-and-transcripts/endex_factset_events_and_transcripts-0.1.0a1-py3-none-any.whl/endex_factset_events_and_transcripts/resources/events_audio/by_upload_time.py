# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

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
from ...types.events_audio import by_upload_time_retrieve_params
from ...types.shared.events_audio_daily import EventsAudioDaily

__all__ = ["ByUploadTimeResource", "AsyncByUploadTimeResource"]


class ByUploadTimeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ByUploadTimeResourceWithRawResponse:
        return ByUploadTimeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ByUploadTimeResourceWithStreamingResponse:
        return ByUploadTimeResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["uploadTime", "-uploadTime"]] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        source_code: Literal["Phone", "Webcast", "Vendor", "WebcastReplay", "Flash", "Replay"] | NotGiven = NOT_GIVEN,
        trimmed: bool | NotGiven = NOT_GIVEN,
        upload_time: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDaily:
        """
        Returns the latest audio recordings based on upload time and allows filtering
        through both source code and Ids.

        Args:
          _pagination_limit: Specifies the number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              uploadTime.

          ids: This parameter filters the results based on ticker-region or Entity ID or the
              combination of both. A comma is used to separate each identifier.

          source_code: This parameter filters the results based on Source of the Audio file. Below are
              the descriptions for each Source Code -

              - Phone = Originated from phone call
              - Webcast = Originated from a webcast
              - Vendor = Received from vendor
              - WebcastReplay = Replay of a webcast
              - Flash = Identical to webcast; can merge with "Webcast" in the future
              - Replay = Phone replay

          trimmed: This parameter helps to search for trimmed audio files, with the non-speaking
              portions removed, and related metadata. The data ranges from May 10, 2011 to Dec
              31, 2022.

          upload_time: This parameter filters data based on uploadTime relative to the current time, in
              hours. For example:- uploadTime = -15 (fetches audio files between 15 hours ago
              and now)

              Minimum is 1 hour i.e., uploadTime= -1

              Maximum is 1 week/168 hours i.e., uploadTime=-168

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/audio/by-upload-time",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "_pagination_limit": _pagination_limit,
                        "_pagination_offset": _pagination_offset,
                        "_sort": _sort,
                        "ids": ids,
                        "source_code": source_code,
                        "trimmed": trimmed,
                        "upload_time": upload_time,
                    },
                    by_upload_time_retrieve_params.ByUploadTimeRetrieveParams,
                ),
            ),
            cast_to=EventsAudioDaily,
        )


class AsyncByUploadTimeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncByUploadTimeResourceWithRawResponse:
        return AsyncByUploadTimeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncByUploadTimeResourceWithStreamingResponse:
        return AsyncByUploadTimeResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["uploadTime", "-uploadTime"]] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        source_code: Literal["Phone", "Webcast", "Vendor", "WebcastReplay", "Flash", "Replay"] | NotGiven = NOT_GIVEN,
        trimmed: bool | NotGiven = NOT_GIVEN,
        upload_time: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDaily:
        """
        Returns the latest audio recordings based on upload time and allows filtering
        through both source code and Ids.

        Args:
          _pagination_limit: Specifies the number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              uploadTime.

          ids: This parameter filters the results based on ticker-region or Entity ID or the
              combination of both. A comma is used to separate each identifier.

          source_code: This parameter filters the results based on Source of the Audio file. Below are
              the descriptions for each Source Code -

              - Phone = Originated from phone call
              - Webcast = Originated from a webcast
              - Vendor = Received from vendor
              - WebcastReplay = Replay of a webcast
              - Flash = Identical to webcast; can merge with "Webcast" in the future
              - Replay = Phone replay

          trimmed: This parameter helps to search for trimmed audio files, with the non-speaking
              portions removed, and related metadata. The data ranges from May 10, 2011 to Dec
              31, 2022.

          upload_time: This parameter filters data based on uploadTime relative to the current time, in
              hours. For example:- uploadTime = -15 (fetches audio files between 15 hours ago
              and now)

              Minimum is 1 hour i.e., uploadTime= -1

              Maximum is 1 week/168 hours i.e., uploadTime=-168

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/audio/by-upload-time",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "_pagination_limit": _pagination_limit,
                        "_pagination_offset": _pagination_offset,
                        "_sort": _sort,
                        "ids": ids,
                        "source_code": source_code,
                        "trimmed": trimmed,
                        "upload_time": upload_time,
                    },
                    by_upload_time_retrieve_params.ByUploadTimeRetrieveParams,
                ),
            ),
            cast_to=EventsAudioDaily,
        )


class ByUploadTimeResourceWithRawResponse:
    def __init__(self, by_upload_time: ByUploadTimeResource) -> None:
        self._by_upload_time = by_upload_time

        self.retrieve = to_raw_response_wrapper(
            by_upload_time.retrieve,
        )


class AsyncByUploadTimeResourceWithRawResponse:
    def __init__(self, by_upload_time: AsyncByUploadTimeResource) -> None:
        self._by_upload_time = by_upload_time

        self.retrieve = async_to_raw_response_wrapper(
            by_upload_time.retrieve,
        )


class ByUploadTimeResourceWithStreamingResponse:
    def __init__(self, by_upload_time: ByUploadTimeResource) -> None:
        self._by_upload_time = by_upload_time

        self.retrieve = to_streamed_response_wrapper(
            by_upload_time.retrieve,
        )


class AsyncByUploadTimeResourceWithStreamingResponse:
    def __init__(self, by_upload_time: AsyncByUploadTimeResource) -> None:
        self._by_upload_time = by_upload_time

        self.retrieve = async_to_streamed_response_wrapper(
            by_upload_time.retrieve,
        )
