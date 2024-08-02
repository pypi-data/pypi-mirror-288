# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
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
from ...types.transcripts import time_list_params
from ...types.transcripts.transcripts_times import TranscriptsTimes

__all__ = ["TimesResource", "AsyncTimesResource"]


class TimesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TimesResourceWithRawResponse:
        return TimesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TimesResourceWithStreamingResponse:
        return TimesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime", "uploadDateTime", "-uploadDateTime"]]
        | NotGiven = NOT_GIVEN,
        end_date_time: Union[str, datetime] | NotGiven = NOT_GIVEN,
        start_date_time: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TranscriptsTimes:
        """
        Returns the transcripts documents within FactSet coverage along with other
        response fields.

        All transcripts originate from Factset Callstreet Transcripts.

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDate.

          end_date_time: The date to which data is required

          start_date_time: **The API supports data from 1999 onwards. Ensure that the provided Date falls
              within this range for accurate results.**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/transcripts/times",
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
                        "end_date_time": end_date_time,
                        "start_date_time": start_date_time,
                    },
                    time_list_params.TimeListParams,
                ),
            ),
            cast_to=TranscriptsTimes,
        )


class AsyncTimesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTimesResourceWithRawResponse:
        return AsyncTimesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTimesResourceWithStreamingResponse:
        return AsyncTimesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime", "uploadDateTime", "-uploadDateTime"]]
        | NotGiven = NOT_GIVEN,
        end_date_time: Union[str, datetime] | NotGiven = NOT_GIVEN,
        start_date_time: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TranscriptsTimes:
        """
        Returns the transcripts documents within FactSet coverage along with other
        response fields.

        All transcripts originate from Factset Callstreet Transcripts.

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDate.

          end_date_time: The date to which data is required

          start_date_time: **The API supports data from 1999 onwards. Ensure that the provided Date falls
              within this range for accurate results.**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/transcripts/times",
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
                        "end_date_time": end_date_time,
                        "start_date_time": start_date_time,
                    },
                    time_list_params.TimeListParams,
                ),
            ),
            cast_to=TranscriptsTimes,
        )


class TimesResourceWithRawResponse:
    def __init__(self, times: TimesResource) -> None:
        self._times = times

        self.list = to_raw_response_wrapper(
            times.list,
        )


class AsyncTimesResourceWithRawResponse:
    def __init__(self, times: AsyncTimesResource) -> None:
        self._times = times

        self.list = async_to_raw_response_wrapper(
            times.list,
        )


class TimesResourceWithStreamingResponse:
    def __init__(self, times: TimesResource) -> None:
        self._times = times

        self.list = to_streamed_response_wrapper(
            times.list,
        )


class AsyncTimesResourceWithStreamingResponse:
    def __init__(self, times: AsyncTimesResource) -> None:
        self._times = times

        self.list = async_to_streamed_response_wrapper(
            times.list,
        )
