# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts.types.shared import NrtCalls

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestByIDs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        by_id = client.near_real_time_transcripts.by_ids.retrieve()
        assert_matches_type(NrtCalls, by_id, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetEventsAndTranscripts) -> None:
        by_id = client.near_real_time_transcripts.by_ids.retrieve(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["eventDatetimeUtc", "-eventDatetimeUtc"],
            audio_source_id=0,
            report_id=0,
        )
        assert_matches_type(NrtCalls, by_id, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.near_real_time_transcripts.by_ids.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        by_id = response.parse()
        assert_matches_type(NrtCalls, by_id, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.near_real_time_transcripts.by_ids.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            by_id = response.parse()
            assert_matches_type(NrtCalls, by_id, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncByIDs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        by_id = await async_client.near_real_time_transcripts.by_ids.retrieve()
        assert_matches_type(NrtCalls, by_id, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        by_id = await async_client.near_real_time_transcripts.by_ids.retrieve(
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["eventDatetimeUtc", "-eventDatetimeUtc"],
            audio_source_id=0,
            report_id=0,
        )
        assert_matches_type(NrtCalls, by_id, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.near_real_time_transcripts.by_ids.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        by_id = await response.parse()
        assert_matches_type(NrtCalls, by_id, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.near_real_time_transcripts.by_ids.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            by_id = await response.parse()
            assert_matches_type(NrtCalls, by_id, path=["response"])

        assert cast(Any, response.is_closed) is True
