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
from ...types.transcripts import id_list_params
from ...types.transcripts.transcripts_one import TranscriptsOne

__all__ = ["IDsResource", "AsyncIDsResource"]


class IDsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IDsResourceWithRawResponse:
        return IDsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IDsResourceWithStreamingResponse:
        return IDsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime"]] | NotGiven = NOT_GIVEN,
        categories: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        primary_id: Literal[True, False] | NotGiven = NOT_GIVEN,
        report_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TranscriptsOne:
        """
        Returns the transcripts documents within FactSet coverage along with other
        response fields.

        All transcripts originate from Factset Callstreet Transcripts.

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDate.

          categories: Code for categories to include. This is a comma-separated list.which represent
              country, industry, and subject codes. Use the `/reference/categories` endpoint
              to get the list of available categories.

              Default = All categories.

          ids: Requested symbols or securities. This is a comma-separated list with a maximum
              limit of 1000. Each symbol can be a FactSet exchange symbol, CUSIP, or SEDOL.

          primary_id: Type of identifier search

              - true - Returns headlines of stories that have the searched identifier(s) as
                the primary identifier.
              - false - Returns headlines of stories that mentioned or referred to the
                identifier.

          report_ids: Requests Report IDs. This is a comma-separated list with a maximum limit of 1000

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/transcripts/ids",
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
                        "categories": categories,
                        "ids": ids,
                        "primary_id": primary_id,
                        "report_ids": report_ids,
                    },
                    id_list_params.IDListParams,
                ),
            ),
            cast_to=TranscriptsOne,
        )


class AsyncIDsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIDsResourceWithRawResponse:
        return AsyncIDsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIDsResourceWithStreamingResponse:
        return AsyncIDsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime"]] | NotGiven = NOT_GIVEN,
        categories: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        primary_id: Literal[True, False] | NotGiven = NOT_GIVEN,
        report_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TranscriptsOne:
        """
        Returns the transcripts documents within FactSet coverage along with other
        response fields.

        All transcripts originate from Factset Callstreet Transcripts.

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDate.

          categories: Code for categories to include. This is a comma-separated list.which represent
              country, industry, and subject codes. Use the `/reference/categories` endpoint
              to get the list of available categories.

              Default = All categories.

          ids: Requested symbols or securities. This is a comma-separated list with a maximum
              limit of 1000. Each symbol can be a FactSet exchange symbol, CUSIP, or SEDOL.

          primary_id: Type of identifier search

              - true - Returns headlines of stories that have the searched identifier(s) as
                the primary identifier.
              - false - Returns headlines of stories that mentioned or referred to the
                identifier.

          report_ids: Requests Report IDs. This is a comma-separated list with a maximum limit of 1000

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/transcripts/ids",
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
                        "categories": categories,
                        "ids": ids,
                        "primary_id": primary_id,
                        "report_ids": report_ids,
                    },
                    id_list_params.IDListParams,
                ),
            ),
            cast_to=TranscriptsOne,
        )


class IDsResourceWithRawResponse:
    def __init__(self, ids: IDsResource) -> None:
        self._ids = ids

        self.list = to_raw_response_wrapper(
            ids.list,
        )


class AsyncIDsResourceWithRawResponse:
    def __init__(self, ids: AsyncIDsResource) -> None:
        self._ids = ids

        self.list = async_to_raw_response_wrapper(
            ids.list,
        )


class IDsResourceWithStreamingResponse:
    def __init__(self, ids: IDsResource) -> None:
        self._ids = ids

        self.list = to_streamed_response_wrapper(
            ids.list,
        )


class AsyncIDsResourceWithStreamingResponse:
    def __init__(self, ids: AsyncIDsResource) -> None:
        self._ids = ids

        self.list = async_to_streamed_response_wrapper(
            ids.list,
        )
