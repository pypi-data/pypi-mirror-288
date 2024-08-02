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
from ...types.near_real_time_transcripts import speakerid_retrieve_params
from ...types.near_real_time_transcripts.nrt_speaker_ids import NrtSpeakerIDs

__all__ = ["SpeakeridsResource", "AsyncSpeakeridsResource"]


class SpeakeridsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpeakeridsResourceWithRawResponse:
        return SpeakeridsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpeakeridsResourceWithStreamingResponse:
        return SpeakeridsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        audio_source_id: int,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["speakerStartOffset", "-speakerStartOffset"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NrtSpeakerIDs:
        """
        Returns the latest speakerIds with the confidence scores generated for an active
        call.

        Args:
          audio_source_id: Unique ID for an Internal recording specific to reportID. For example, ReportID
              X would have multiple recordings from different source (dial-in or webcast). One
              ReportID can have multiple AudioSourceIDs.

          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on the
              start offset of the speaker.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/nrt/speakerids",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "audio_source_id": audio_source_id,
                        "_pagination_limit": _pagination_limit,
                        "_pagination_offset": _pagination_offset,
                        "_sort": _sort,
                    },
                    speakerid_retrieve_params.SpeakeridRetrieveParams,
                ),
            ),
            cast_to=NrtSpeakerIDs,
        )


class AsyncSpeakeridsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpeakeridsResourceWithRawResponse:
        return AsyncSpeakeridsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpeakeridsResourceWithStreamingResponse:
        return AsyncSpeakeridsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        audio_source_id: int,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["speakerStartOffset", "-speakerStartOffset"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NrtSpeakerIDs:
        """
        Returns the latest speakerIds with the confidence scores generated for an active
        call.

        Args:
          audio_source_id: Unique ID for an Internal recording specific to reportID. For example, ReportID
              X would have multiple recordings from different source (dial-in or webcast). One
              ReportID can have multiple AudioSourceIDs.

          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on the
              start offset of the speaker.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/nrt/speakerids",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "audio_source_id": audio_source_id,
                        "_pagination_limit": _pagination_limit,
                        "_pagination_offset": _pagination_offset,
                        "_sort": _sort,
                    },
                    speakerid_retrieve_params.SpeakeridRetrieveParams,
                ),
            ),
            cast_to=NrtSpeakerIDs,
        )


class SpeakeridsResourceWithRawResponse:
    def __init__(self, speakerids: SpeakeridsResource) -> None:
        self._speakerids = speakerids

        self.retrieve = to_raw_response_wrapper(
            speakerids.retrieve,
        )


class AsyncSpeakeridsResourceWithRawResponse:
    def __init__(self, speakerids: AsyncSpeakeridsResource) -> None:
        self._speakerids = speakerids

        self.retrieve = async_to_raw_response_wrapper(
            speakerids.retrieve,
        )


class SpeakeridsResourceWithStreamingResponse:
    def __init__(self, speakerids: SpeakeridsResource) -> None:
        self._speakerids = speakerids

        self.retrieve = to_streamed_response_wrapper(
            speakerids.retrieve,
        )


class AsyncSpeakeridsResourceWithStreamingResponse:
    def __init__(self, speakerids: AsyncSpeakeridsResource) -> None:
        self._speakerids = speakerids

        self.retrieve = async_to_streamed_response_wrapper(
            speakerids.retrieve,
        )
