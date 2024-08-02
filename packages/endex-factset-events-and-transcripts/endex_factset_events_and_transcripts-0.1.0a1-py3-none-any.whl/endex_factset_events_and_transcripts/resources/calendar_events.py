# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import calendar_event_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.company_event_response import CompanyEventResponse

__all__ = ["CalendarEventsResource", "AsyncCalendarEventsResource"]


class CalendarEventsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CalendarEventsResourceWithRawResponse:
        return CalendarEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CalendarEventsResourceWithStreamingResponse:
        return CalendarEventsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: calendar_event_create_params.Data | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyEventResponse:
        """
        This endpoint returns all company events with filters from the request.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/calendar/events",
            body=maybe_transform({"data": data}, calendar_event_create_params.CalendarEventCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyEventResponse,
        )


class AsyncCalendarEventsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCalendarEventsResourceWithRawResponse:
        return AsyncCalendarEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCalendarEventsResourceWithStreamingResponse:
        return AsyncCalendarEventsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: calendar_event_create_params.Data | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyEventResponse:
        """
        This endpoint returns all company events with filters from the request.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/calendar/events",
            body=await async_maybe_transform({"data": data}, calendar_event_create_params.CalendarEventCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyEventResponse,
        )


class CalendarEventsResourceWithRawResponse:
    def __init__(self, calendar_events: CalendarEventsResource) -> None:
        self._calendar_events = calendar_events

        self.create = to_raw_response_wrapper(
            calendar_events.create,
        )


class AsyncCalendarEventsResourceWithRawResponse:
    def __init__(self, calendar_events: AsyncCalendarEventsResource) -> None:
        self._calendar_events = calendar_events

        self.create = async_to_raw_response_wrapper(
            calendar_events.create,
        )


class CalendarEventsResourceWithStreamingResponse:
    def __init__(self, calendar_events: CalendarEventsResource) -> None:
        self._calendar_events = calendar_events

        self.create = to_streamed_response_wrapper(
            calendar_events.create,
        )


class AsyncCalendarEventsResourceWithStreamingResponse:
    def __init__(self, calendar_events: AsyncCalendarEventsResource) -> None:
        self._calendar_events = calendar_events

        self.create = async_to_streamed_response_wrapper(
            calendar_events.create,
        )
