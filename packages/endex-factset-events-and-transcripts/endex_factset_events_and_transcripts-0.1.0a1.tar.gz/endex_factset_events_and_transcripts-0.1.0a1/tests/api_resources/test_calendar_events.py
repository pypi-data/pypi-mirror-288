# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts.types import CompanyEventResponse
from endex_factset_events_and_transcripts._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCalendarEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetEventsAndTranscripts) -> None:
        calendar_event = client.calendar_events.create()
        assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetEventsAndTranscripts) -> None:
        calendar_event = client.calendar_events.create(
            data={
                "date_time": {
                    "start": parse_datetime("2022-12-01T00:00:00Z"),
                    "end": parse_datetime("2022-12-31T22:59:02Z"),
                },
                "universe": {
                    "symbols": ["FDS-US"],
                    "type": "Tickers",
                },
                "event_types": ["Earnings"],
            },
        )
        assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.calendar_events.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        calendar_event = response.parse()
        assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.calendar_events.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            calendar_event = response.parse()
            assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCalendarEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        calendar_event = await async_client.calendar_events.create()
        assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        calendar_event = await async_client.calendar_events.create(
            data={
                "date_time": {
                    "start": parse_datetime("2022-12-01T00:00:00Z"),
                    "end": parse_datetime("2022-12-31T22:59:02Z"),
                },
                "universe": {
                    "symbols": ["FDS-US"],
                    "type": "Tickers",
                },
                "event_types": ["Earnings"],
            },
        )
        assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.calendar_events.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        calendar_event = await response.parse()
        assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.calendar_events.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            calendar_event = await response.parse()
            assert_matches_type(CompanyEventResponse, calendar_event, path=["response"])

        assert cast(Any, response.is_closed) is True
