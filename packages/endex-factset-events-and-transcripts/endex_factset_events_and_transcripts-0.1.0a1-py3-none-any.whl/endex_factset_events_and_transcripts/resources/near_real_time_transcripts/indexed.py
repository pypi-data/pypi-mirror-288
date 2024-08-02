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
from ...types.near_real_time_transcripts import indexed_retrieve_params
from ...types.near_real_time_transcripts.indexed_nrt import IndexedNrt

__all__ = ["IndexedResource", "AsyncIndexedResource"]


class IndexedResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IndexedResourceWithRawResponse:
        return IndexedResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IndexedResourceWithStreamingResponse:
        return IndexedResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        audio_source_id: int,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexedNrt:
        """
        Returns the indexed transcript data in small increments throughout the duration
        of an active call.

        Args:
          audio_source_id: Unique ID for an Internal recording specific to reportID. For example, ReportID
              X would have multiple recordings from different source (dial-in or webcast). One
              ReportID can have multiple AudioSourceIDs.

          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/nrt/indexed",
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
                    },
                    indexed_retrieve_params.IndexedRetrieveParams,
                ),
            ),
            cast_to=IndexedNrt,
        )


class AsyncIndexedResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIndexedResourceWithRawResponse:
        return AsyncIndexedResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIndexedResourceWithStreamingResponse:
        return AsyncIndexedResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        audio_source_id: int,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IndexedNrt:
        """
        Returns the indexed transcript data in small increments throughout the duration
        of an active call.

        Args:
          audio_source_id: Unique ID for an Internal recording specific to reportID. For example, ReportID
              X would have multiple recordings from different source (dial-in or webcast). One
              ReportID can have multiple AudioSourceIDs.

          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/nrt/indexed",
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
                    },
                    indexed_retrieve_params.IndexedRetrieveParams,
                ),
            ),
            cast_to=IndexedNrt,
        )


class IndexedResourceWithRawResponse:
    def __init__(self, indexed: IndexedResource) -> None:
        self._indexed = indexed

        self.retrieve = to_raw_response_wrapper(
            indexed.retrieve,
        )


class AsyncIndexedResourceWithRawResponse:
    def __init__(self, indexed: AsyncIndexedResource) -> None:
        self._indexed = indexed

        self.retrieve = async_to_raw_response_wrapper(
            indexed.retrieve,
        )


class IndexedResourceWithStreamingResponse:
    def __init__(self, indexed: IndexedResource) -> None:
        self._indexed = indexed

        self.retrieve = to_streamed_response_wrapper(
            indexed.retrieve,
        )


class AsyncIndexedResourceWithStreamingResponse:
    def __init__(self, indexed: AsyncIndexedResource) -> None:
        self._indexed = indexed

        self.retrieve = async_to_streamed_response_wrapper(
            indexed.retrieve,
        )
