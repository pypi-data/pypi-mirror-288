# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts._utils import parse_datetime
from endex_factset_events_and_transcripts.types.transcripts import TranscriptsTimes

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTimes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        time = client.transcripts.times.list()
        assert_matches_type(TranscriptsTimes, time, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetEventsAndTranscripts) -> None:
        time = client.transcripts.times.list(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["storyDateTime", "-storyDateTime", "uploadDateTime"],
            end_date_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TranscriptsTimes, time, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.transcripts.times.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time = response.parse()
        assert_matches_type(TranscriptsTimes, time, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.transcripts.times.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time = response.parse()
            assert_matches_type(TranscriptsTimes, time, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTimes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        time = await async_client.transcripts.times.list()
        assert_matches_type(TranscriptsTimes, time, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        time = await async_client.transcripts.times.list(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["storyDateTime", "-storyDateTime", "uploadDateTime"],
            end_date_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(TranscriptsTimes, time, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.transcripts.times.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time = await response.parse()
        assert_matches_type(TranscriptsTimes, time, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.transcripts.times.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time = await response.parse()
            assert_matches_type(TranscriptsTimes, time, path=["response"])

        assert cast(Any, response.is_closed) is True
