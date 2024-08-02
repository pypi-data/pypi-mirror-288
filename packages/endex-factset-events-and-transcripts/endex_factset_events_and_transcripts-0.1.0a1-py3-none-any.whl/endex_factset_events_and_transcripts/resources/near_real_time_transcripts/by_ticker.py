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
from ...types.shared.nrt_calls import NrtCalls
from ...types.near_real_time_transcripts import by_ticker_retrieve_params

__all__ = ["ByTickerResource", "AsyncByTickerResource"]


class ByTickerResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ByTickerResourceWithRawResponse:
        return ByTickerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ByTickerResourceWithStreamingResponse:
        return ByTickerResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["eventDatetimeUtc", "-eventDatetimeUtc"]] | NotGiven = NOT_GIVEN,
        call_status: Literal["InProgress", "Ended", "EWN", "IssueAtSource"] | NotGiven = NOT_GIVEN,
        entity_id: str | NotGiven = NOT_GIVEN,
        ticker: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NrtCalls:
        """
        Returns the active calls happening at the moment

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDatetimeUtc.

          call_status: Status of the call, i.e., Ended, InProgress, EndedWithoutNotification, or
              IssueAtSource.

          entity_id: Factset entity level identifier for the company hosting the event.

          ticker: Ticker-region identifier for the company hosting the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/nrt/by-ticker",
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
                        "call_status": call_status,
                        "entity_id": entity_id,
                        "ticker": ticker,
                    },
                    by_ticker_retrieve_params.ByTickerRetrieveParams,
                ),
            ),
            cast_to=NrtCalls,
        )


class AsyncByTickerResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncByTickerResourceWithRawResponse:
        return AsyncByTickerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncByTickerResourceWithStreamingResponse:
        return AsyncByTickerResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["eventDatetimeUtc", "-eventDatetimeUtc"]] | NotGiven = NOT_GIVEN,
        call_status: Literal["InProgress", "Ended", "EWN", "IssueAtSource"] | NotGiven = NOT_GIVEN,
        entity_id: str | NotGiven = NOT_GIVEN,
        ticker: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NrtCalls:
        """
        Returns the active calls happening at the moment

        Args:
          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              eventDatetimeUtc.

          call_status: Status of the call, i.e., Ended, InProgress, EndedWithoutNotification, or
              IssueAtSource.

          entity_id: Factset entity level identifier for the company hosting the event.

          ticker: Ticker-region identifier for the company hosting the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/nrt/by-ticker",
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
                        "call_status": call_status,
                        "entity_id": entity_id,
                        "ticker": ticker,
                    },
                    by_ticker_retrieve_params.ByTickerRetrieveParams,
                ),
            ),
            cast_to=NrtCalls,
        )


class ByTickerResourceWithRawResponse:
    def __init__(self, by_ticker: ByTickerResource) -> None:
        self._by_ticker = by_ticker

        self.retrieve = to_raw_response_wrapper(
            by_ticker.retrieve,
        )


class AsyncByTickerResourceWithRawResponse:
    def __init__(self, by_ticker: AsyncByTickerResource) -> None:
        self._by_ticker = by_ticker

        self.retrieve = async_to_raw_response_wrapper(
            by_ticker.retrieve,
        )


class ByTickerResourceWithStreamingResponse:
    def __init__(self, by_ticker: ByTickerResource) -> None:
        self._by_ticker = by_ticker

        self.retrieve = to_streamed_response_wrapper(
            by_ticker.retrieve,
        )


class AsyncByTickerResourceWithStreamingResponse:
    def __init__(self, by_ticker: AsyncByTickerResource) -> None:
        self._by_ticker = by_ticker

        self.retrieve = async_to_streamed_response_wrapper(
            by_ticker.retrieve,
        )
