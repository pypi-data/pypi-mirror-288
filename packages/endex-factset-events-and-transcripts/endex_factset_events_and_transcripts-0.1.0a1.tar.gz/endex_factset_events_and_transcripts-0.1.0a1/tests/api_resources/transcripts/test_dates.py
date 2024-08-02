# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts._utils import parse_date
from endex_factset_events_and_transcripts.types.shared import Transcripts

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        date = client.transcripts.dates.list()
        assert_matches_type(Transcripts, date, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetEventsAndTranscripts) -> None:
        date = client.transcripts.dates.list(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["storyDateTime", "-storyDateTime"],
            end_date=parse_date("2019-12-27"),
            end_date_relative=0,
            start_date=parse_date("2019-12-27"),
            start_date_relative=0,
            time_zone="timeZone",
        )
        assert_matches_type(Transcripts, date, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.transcripts.dates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        date = response.parse()
        assert_matches_type(Transcripts, date, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.transcripts.dates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            date = response.parse()
            assert_matches_type(Transcripts, date, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDates:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        date = await async_client.transcripts.dates.list()
        assert_matches_type(Transcripts, date, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        date = await async_client.transcripts.dates.list(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["storyDateTime", "-storyDateTime"],
            end_date=parse_date("2019-12-27"),
            end_date_relative=0,
            start_date=parse_date("2019-12-27"),
            start_date_relative=0,
            time_zone="timeZone",
        )
        assert_matches_type(Transcripts, date, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.transcripts.dates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        date = await response.parse()
        assert_matches_type(Transcripts, date, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.transcripts.dates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            date = await response.parse()
            assert_matches_type(Transcripts, date, path=["response"])

        assert cast(Any, response.is_closed) is True
