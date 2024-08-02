# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.reference.response_time import ResponseTime

__all__ = ["TimeZonesResource", "AsyncTimeZonesResource"]


class TimeZonesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TimeZonesResourceWithRawResponse:
        return TimeZonesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TimeZonesResourceWithStreamingResponse:
        return TimeZonesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResponseTime:
        """Retrieves and delivers a comprehensive list of all available `timeZones`."""
        return self._get(
            "/reference/time-zones",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseTime,
        )


class AsyncTimeZonesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTimeZonesResourceWithRawResponse:
        return AsyncTimeZonesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTimeZonesResourceWithStreamingResponse:
        return AsyncTimeZonesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResponseTime:
        """Retrieves and delivers a comprehensive list of all available `timeZones`."""
        return await self._get(
            "/reference/time-zones",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResponseTime,
        )


class TimeZonesResourceWithRawResponse:
    def __init__(self, time_zones: TimeZonesResource) -> None:
        self._time_zones = time_zones

        self.retrieve = to_raw_response_wrapper(
            time_zones.retrieve,
        )


class AsyncTimeZonesResourceWithRawResponse:
    def __init__(self, time_zones: AsyncTimeZonesResource) -> None:
        self._time_zones = time_zones

        self.retrieve = async_to_raw_response_wrapper(
            time_zones.retrieve,
        )


class TimeZonesResourceWithStreamingResponse:
    def __init__(self, time_zones: TimeZonesResource) -> None:
        self._time_zones = time_zones

        self.retrieve = to_streamed_response_wrapper(
            time_zones.retrieve,
        )


class AsyncTimeZonesResourceWithStreamingResponse:
    def __init__(self, time_zones: AsyncTimeZonesResource) -> None:
        self._time_zones = time_zones

        self.retrieve = async_to_streamed_response_wrapper(
            time_zones.retrieve,
        )
