# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts.types.near_real_time_transcripts import (
    NrtSpeakerIDs,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpeakerids:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        speakerid = client.near_real_time_transcripts.speakerids.retrieve(
            audio_source_id=0,
        )
        assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetEventsAndTranscripts) -> None:
        speakerid = client.near_real_time_transcripts.speakerids.retrieve(
            audio_source_id=0,
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["speakerStartOffset", "-speakerStartOffset"],
        )
        assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.near_real_time_transcripts.speakerids.with_raw_response.retrieve(
            audio_source_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        speakerid = response.parse()
        assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.near_real_time_transcripts.speakerids.with_streaming_response.retrieve(
            audio_source_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            speakerid = response.parse()
            assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSpeakerids:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        speakerid = await async_client.near_real_time_transcripts.speakerids.retrieve(
            audio_source_id=0,
        )
        assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        speakerid = await async_client.near_real_time_transcripts.speakerids.retrieve(
            audio_source_id=0,
            _pagination_limit=0,
            _pagination_offset=0,
            _sort=["speakerStartOffset", "-speakerStartOffset"],
        )
        assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.near_real_time_transcripts.speakerids.with_raw_response.retrieve(
            audio_source_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        speakerid = await response.parse()
        assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.near_real_time_transcripts.speakerids.with_streaming_response.retrieve(
            audio_source_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            speakerid = await response.parse()
            assert_matches_type(NrtSpeakerIDs, speakerid, path=["response"])

        assert cast(Any, response.is_closed) is True
