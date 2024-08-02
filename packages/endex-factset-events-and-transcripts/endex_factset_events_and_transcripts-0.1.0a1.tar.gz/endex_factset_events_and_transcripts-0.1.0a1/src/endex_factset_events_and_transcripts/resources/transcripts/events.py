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
from ...types.transcripts import event_list_params
from ...types.shared.transcripts import Transcripts

__all__ = ["EventsResource", "AsyncEventsResource"]


class EventsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventsResourceWithRawResponse:
        return EventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsResourceWithStreamingResponse:
        return EventsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime"]] | NotGiven = NOT_GIVEN,
        event_ids: List[str] | NotGiven = NOT_GIVEN,
        event_type: Literal[
            "Earnings",
            "Guidance",
            "AnalystsShareholdersMeeting",
            "ConferencePresentation",
            "SalesRevenue",
            "SpecialSituation",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Transcripts:
        """
        Returns the transcripts documents within FactSet coverage along with other
        response fields.

        All transcripts originate from Factset Callstreet Transcripts.

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDate.

          event_ids: Requests Event IDs. This is a comma-separated list with a maximum limit of 1000.

          event_type: Specifies the type of event you want to retrieve. Earnings - Denotes an Earnings
              event. Guidance - Denotes a Guidance event. AnalystsShareholdersMeeting -
              Denotes an Analysts and Shareholders Meeting event. ConferencePresentation -
              Denotes a Conference Presentation event. SalesRevenue - Denotes a Sales/Revenue
              event. SpecialSituation - Denotes a Special Situation event (i.e.
              Merger/Acquisition).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/transcripts/events",
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
                        "event_ids": event_ids,
                        "event_type": event_type,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=Transcripts,
        )


class AsyncEventsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventsResourceWithRawResponse:
        return AsyncEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsResourceWithStreamingResponse:
        return AsyncEventsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime"]] | NotGiven = NOT_GIVEN,
        event_ids: List[str] | NotGiven = NOT_GIVEN,
        event_type: Literal[
            "Earnings",
            "Guidance",
            "AnalystsShareholdersMeeting",
            "ConferencePresentation",
            "SalesRevenue",
            "SpecialSituation",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Transcripts:
        """
        Returns the transcripts documents within FactSet coverage along with other
        response fields.

        All transcripts originate from Factset Callstreet Transcripts.

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDate.

          event_ids: Requests Event IDs. This is a comma-separated list with a maximum limit of 1000.

          event_type: Specifies the type of event you want to retrieve. Earnings - Denotes an Earnings
              event. Guidance - Denotes a Guidance event. AnalystsShareholdersMeeting -
              Denotes an Analysts and Shareholders Meeting event. ConferencePresentation -
              Denotes a Conference Presentation event. SalesRevenue - Denotes a Sales/Revenue
              event. SpecialSituation - Denotes a Special Situation event (i.e.
              Merger/Acquisition).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/transcripts/events",
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
                        "event_ids": event_ids,
                        "event_type": event_type,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=Transcripts,
        )


class EventsResourceWithRawResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.list = to_raw_response_wrapper(
            events.list,
        )


class AsyncEventsResourceWithRawResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.list = async_to_raw_response_wrapper(
            events.list,
        )


class EventsResourceWithStreamingResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.list = to_streamed_response_wrapper(
            events.list,
        )


class AsyncEventsResourceWithStreamingResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.list = async_to_streamed_response_wrapper(
            events.list,
        )
