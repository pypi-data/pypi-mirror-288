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
from ...types.transcripts import date_list_params
from ...types.shared.transcripts import Transcripts

__all__ = ["DatesResource", "AsyncDatesResource"]


class DatesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DatesResourceWithRawResponse:
        return DatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DatesResourceWithStreamingResponse:
        return DatesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime"]] | NotGiven = NOT_GIVEN,
        end_date: Union[str, date] | NotGiven = NOT_GIVEN,
        end_date_relative: int | NotGiven = NOT_GIVEN,
        start_date: Union[str, date] | NotGiven = NOT_GIVEN,
        start_date_relative: int | NotGiven = NOT_GIVEN,
        time_zone: str | NotGiven = NOT_GIVEN,
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

          end_date: End Date. Format is YYYY-MM-DD.

          end_date_relative: The latest date of the feed file the API should fetch for based on the file
              timestamp.

              - Format: Specify the date using a relative term as an integer: '0' for today,
                '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
                used to represent past dates.

              - _Either `endDate` or `endDateRelative` should be used, but not both._
              - _If both `endDate` and `endDateRelative` are provided in the same request, the
                API will return an error._
              - _If users provide future dates in requests for `endDate` or `endDateRelative`,
                the API will not return any data._

          start_date: Start Date. Format is YYYY-MM-DD

              **The API supports data from 1999 onwards. Ensure that the provided Date falls
              within this range for accurate results.**

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

          time_zone: timeZone to return story dates and times.Time zones, represented in POSIX
              format, are automatically adjusted for daylight savings. timeZone names are
              sourced from the IANA timezone registry. The time fields in the response will
              adhere to this specified timezone.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/transcripts/dates",
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
                        "start_date": start_date,
                        "start_date_relative": start_date_relative,
                        "time_zone": time_zone,
                    },
                    date_list_params.DateListParams,
                ),
            ),
            cast_to=Transcripts,
        )


class AsyncDatesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDatesResourceWithRawResponse:
        return AsyncDatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDatesResourceWithStreamingResponse:
        return AsyncDatesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        _sort: List[Literal["storyDateTime", "-storyDateTime"]] | NotGiven = NOT_GIVEN,
        end_date: Union[str, date] | NotGiven = NOT_GIVEN,
        end_date_relative: int | NotGiven = NOT_GIVEN,
        start_date: Union[str, date] | NotGiven = NOT_GIVEN,
        start_date_relative: int | NotGiven = NOT_GIVEN,
        time_zone: str | NotGiven = NOT_GIVEN,
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

          end_date: End Date. Format is YYYY-MM-DD.

          end_date_relative: The latest date of the feed file the API should fetch for based on the file
              timestamp.

              - Format: Specify the date using a relative term as an integer: '0' for today,
                '-1' for yesterday, '-2' for two days ago, and so forth. Negative values are
                used to represent past dates.

              - _Either `endDate` or `endDateRelative` should be used, but not both._
              - _If both `endDate` and `endDateRelative` are provided in the same request, the
                API will return an error._
              - _If users provide future dates in requests for `endDate` or `endDateRelative`,
                the API will not return any data._

          start_date: Start Date. Format is YYYY-MM-DD

              **The API supports data from 1999 onwards. Ensure that the provided Date falls
              within this range for accurate results.**

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

          time_zone: timeZone to return story dates and times.Time zones, represented in POSIX
              format, are automatically adjusted for daylight savings. timeZone names are
              sourced from the IANA timezone registry. The time fields in the response will
              adhere to this specified timezone.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/transcripts/dates",
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
                        "start_date": start_date,
                        "start_date_relative": start_date_relative,
                        "time_zone": time_zone,
                    },
                    date_list_params.DateListParams,
                ),
            ),
            cast_to=Transcripts,
        )


class DatesResourceWithRawResponse:
    def __init__(self, dates: DatesResource) -> None:
        self._dates = dates

        self.list = to_raw_response_wrapper(
            dates.list,
        )


class AsyncDatesResourceWithRawResponse:
    def __init__(self, dates: AsyncDatesResource) -> None:
        self._dates = dates

        self.list = async_to_raw_response_wrapper(
            dates.list,
        )


class DatesResourceWithStreamingResponse:
    def __init__(self, dates: DatesResource) -> None:
        self._dates = dates

        self.list = to_streamed_response_wrapper(
            dates.list,
        )


class AsyncDatesResourceWithStreamingResponse:
    def __init__(self, dates: AsyncDatesResource) -> None:
        self._dates = dates

        self.list = async_to_streamed_response_wrapper(
            dates.list,
        )
