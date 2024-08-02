# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_events_and_transcripts import EndexFactsetEventsAndTranscripts, AsyncEndexFactsetEventsAndTranscripts
from endex_factset_events_and_transcripts.types.reference import ResponseCategories

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCategories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        category = client.reference.categories.list()
        assert_matches_type(ResponseCategories, category, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        response = client.reference.categories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(ResponseCategories, category, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetEventsAndTranscripts) -> None:
        with client.reference.categories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = response.parse()
            assert_matches_type(ResponseCategories, category, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCategories:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        category = await async_client.reference.categories.list()
        assert_matches_type(ResponseCategories, category, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        response = await async_client.reference.categories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(ResponseCategories, category, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        async with async_client.reference.categories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = await response.parse()
            assert_matches_type(ResponseCategories, category, path=["response"])

        assert cast(Any, response.is_closed) is True
