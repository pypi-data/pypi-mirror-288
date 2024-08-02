# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import date
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
from ...types.events_audio import by_date_retrieve_params
from ...types.shared.events_audio_daily import EventsAudioDaily

__all__ = ["ByDateResource", "AsyncByDateResource"]


class ByDateResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ByDateResourceWithRawResponse:
        return ByDateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ByDateResourceWithStreamingResponse:
        return ByDateResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["startDate", "-startDate"]] | NotGiven = NOT_GIVEN,
        end_date: Union[str, date] | NotGiven = NOT_GIVEN,
        end_date_relative: int | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        source_code: Literal["Phone", "Webcast", "Vendor", "WebcastReplay", "Flash", "Replay"] | NotGiven = NOT_GIVEN,
        start_date: Union[str, date] | NotGiven = NOT_GIVEN,
        start_date_relative: int | NotGiven = NOT_GIVEN,
        trimmed: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDaily:
        """
        Retrieves the most recent audio recordings based on specified dates and allows
        filtering through both source code and Ids.

        Args:
          _pagination_limit: Specifies the number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              startDate.

          end_date: The latest date of the audio file the API should fetch for.

              - Format: Should be absolute (YYYY-MM-DD).

          end_date_relative: The latest date of the feed file the API should fetch based on the file
              timestamp.

              Format: Specify the date using a relative term as an integer: '0' for today,
              '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
              used to represent past dates.

              - Either `endDate` or `endDateRelative` should be used, but not both.
              - If both `endDate` and `endDateRelative` are provided in the same request, the
                API will return an error.
              - If users provide future dates in requests for `endDate` or `endDateRelative`,
                the API will not return any data.

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

          start_date: The earliest date of the audio file the API should fetch for.

              - Format: Should be absolute (YYYY-MM-DD).

          start_date_relative: The earliest date of the feed file the API should fetch based on the file
              timestamp.

              - Format: Specify the date using a relative term as an integer: '0' for today,
                '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
                used to represent past dates.

              - _Either `startDate` or `startDateRelative` should be used, but not both._
              - _If both `startDate` and `startDateRelative` are provided in the same request,
                the API will return an error._
              - _If users provide future dates in requests for `startDate` or
                `startDateRelative`, the API will not return any data._

          trimmed: This parameter helps to search for trimmed audio files, with the non-speaking
              portions removed, and related metadata. The data ranges from May 10, 2011 to Dec
              31, 2022.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/audio/by-date",
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
                        "end_date": end_date,
                        "end_date_relative": end_date_relative,
                        "ids": ids,
                        "source_code": source_code,
                        "start_date": start_date,
                        "start_date_relative": start_date_relative,
                        "trimmed": trimmed,
                    },
                    by_date_retrieve_params.ByDateRetrieveParams,
                ),
            ),
            cast_to=EventsAudioDaily,
        )


class AsyncByDateResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncByDateResourceWithRawResponse:
        return AsyncByDateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncByDateResourceWithStreamingResponse:
        return AsyncByDateResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["startDate", "-startDate"]] | NotGiven = NOT_GIVEN,
        end_date: Union[str, date] | NotGiven = NOT_GIVEN,
        end_date_relative: int | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        source_code: Literal["Phone", "Webcast", "Vendor", "WebcastReplay", "Flash", "Replay"] | NotGiven = NOT_GIVEN,
        start_date: Union[str, date] | NotGiven = NOT_GIVEN,
        start_date_relative: int | NotGiven = NOT_GIVEN,
        trimmed: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventsAudioDaily:
        """
        Retrieves the most recent audio recordings based on specified dates and allows
        filtering through both source code and Ids.

        Args:
          _pagination_limit: Specifies the number of results to return per page.

          _pagination_offset: Page number of the results to return.

          _sort: Enables sorting data in ascending or descending chronological order based on
              startDate.

          end_date: The latest date of the audio file the API should fetch for.

              - Format: Should be absolute (YYYY-MM-DD).

          end_date_relative: The latest date of the feed file the API should fetch based on the file
              timestamp.

              Format: Specify the date using a relative term as an integer: '0' for today,
              '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
              used to represent past dates.

              - Either `endDate` or `endDateRelative` should be used, but not both.
              - If both `endDate` and `endDateRelative` are provided in the same request, the
                API will return an error.
              - If users provide future dates in requests for `endDate` or `endDateRelative`,
                the API will not return any data.

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

          start_date: The earliest date of the audio file the API should fetch for.

              - Format: Should be absolute (YYYY-MM-DD).

          start_date_relative: The earliest date of the feed file the API should fetch based on the file
              timestamp.

              - Format: Specify the date using a relative term as an integer: '0' for today,
                '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
                used to represent past dates.

              - _Either `startDate` or `startDateRelative` should be used, but not both._
              - _If both `startDate` and `startDateRelative` are provided in the same request,
                the API will return an error._
              - _If users provide future dates in requests for `startDate` or
                `startDateRelative`, the API will not return any data._

          trimmed: This parameter helps to search for trimmed audio files, with the non-speaking
              portions removed, and related metadata. The data ranges from May 10, 2011 to Dec
              31, 2022.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/audio/by-date",
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
                        "end_date": end_date,
                        "end_date_relative": end_date_relative,
                        "ids": ids,
                        "source_code": source_code,
                        "start_date": start_date,
                        "start_date_relative": start_date_relative,
                        "trimmed": trimmed,
                    },
                    by_date_retrieve_params.ByDateRetrieveParams,
                ),
            ),
            cast_to=EventsAudioDaily,
        )


class ByDateResourceWithRawResponse:
    def __init__(self, by_date: ByDateResource) -> None:
        self._by_date = by_date

        self.retrieve = to_raw_response_wrapper(
            by_date.retrieve,
        )


class AsyncByDateResourceWithRawResponse:
    def __init__(self, by_date: AsyncByDateResource) -> None:
        self._by_date = by_date

        self.retrieve = async_to_raw_response_wrapper(
            by_date.retrieve,
        )


class ByDateResourceWithStreamingResponse:
    def __init__(self, by_date: ByDateResource) -> None:
        self._by_date = by_date

        self.retrieve = to_streamed_response_wrapper(
            by_date.retrieve,
        )


class AsyncByDateResourceWithStreamingResponse:
    def __init__(self, by_date: AsyncByDateResource) -> None:
        self._by_date = by_date

        self.retrieve = async_to_streamed_response_wrapper(
            by_date.retrieve,
        )
