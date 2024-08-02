# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts._utils import parse_date
from endex_factset_events_and_transcripts.types.shared import EventsAudioDaily

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestByDate:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        by_date = client.events_audio.by_date.retrieve()
        assert_matches_type(EventsAudioDaily, by_date, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetEventsAndTranscripts) -> None:
        by_date = client.events_audio.by_date.retrieve(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["startDate"],
            end_date=parse_date("2019-12-27"),
            end_date_relative=0,
            ids=["string", "string", "string"],
            source_code="Phone",
            start_date=parse_date("2019-12-27"),
            start_date_relative=0,
            trimmed=True,
        )
        assert_matches_type(EventsAudioDaily, by_date, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.events_audio.by_date.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        by_date = response.parse()
        assert_matches_type(EventsAudioDaily, by_date, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.events_audio.by_date.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            by_date = response.parse()
            assert_matches_type(EventsAudioDaily, by_date, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncByDate:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        by_date = await async_client.events_audio.by_date.retrieve()
        assert_matches_type(EventsAudioDaily, by_date, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        by_date = await async_client.events_audio.by_date.retrieve(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["startDate"],
            end_date=parse_date("2019-12-27"),
            end_date_relative=0,
            ids=["string", "string", "string"],
            source_code="Phone",
            start_date=parse_date("2019-12-27"),
            start_date_relative=0,
            trimmed=True,
        )
        assert_matches_type(EventsAudioDaily, by_date, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.events_audio.by_date.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        by_date = await response.parse()
        assert_matches_type(EventsAudioDaily, by_date, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.events_audio.by_date.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            by_date = await response.parse()
            assert_matches_type(EventsAudioDaily, by_date, path=["response"])

        assert cast(Any, response.is_closed) is True
