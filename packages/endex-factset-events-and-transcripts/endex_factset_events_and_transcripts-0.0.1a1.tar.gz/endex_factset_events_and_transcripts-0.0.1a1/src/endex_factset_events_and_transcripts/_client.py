# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "EndexFactsetEventsAndTranscripts",
    "AsyncEndexFactsetEventsAndTranscripts",
    "Client",
    "AsyncClient",
]


class EndexFactsetEventsAndTranscripts(SyncAPIClient):
    calendar_events: resources.CalendarEventsResource
    events_audio: resources.EventsAudioResource
    near_real_time_transcripts: resources.NearRealTimeTranscriptsResource
    transcripts: resources.TranscriptsResource
    reference: resources.ReferenceResource
    with_raw_response: EndexFactsetEventsAndTranscriptsWithRawResponse
    with_streaming_response: EndexFactsetEventsAndTranscriptsWithStreamedResponse

    # client options

    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """
        Construct a new synchronous endex-factset-events-and-transcripts client instance.
        """
        if base_url is None:
            base_url = os.environ.get("ENDEX_FACTSET_EVENTS_AND_TRANSCRIPTS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.factset.com/events/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.calendar_events = resources.CalendarEventsResource(self)
        self.events_audio = resources.EventsAudioResource(self)
        self.near_real_time_transcripts = resources.NearRealTimeTranscriptsResource(self)
        self.transcripts = resources.TranscriptsResource(self)
        self.reference = resources.ReferenceResource(self)
        self.with_raw_response = EndexFactsetEventsAndTranscriptsWithRawResponse(self)
        self.with_streaming_response = EndexFactsetEventsAndTranscriptsWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncEndexFactsetEventsAndTranscripts(AsyncAPIClient):
    calendar_events: resources.AsyncCalendarEventsResource
    events_audio: resources.AsyncEventsAudioResource
    near_real_time_transcripts: resources.AsyncNearRealTimeTranscriptsResource
    transcripts: resources.AsyncTranscriptsResource
    reference: resources.AsyncReferenceResource
    with_raw_response: AsyncEndexFactsetEventsAndTranscriptsWithRawResponse
    with_streaming_response: AsyncEndexFactsetEventsAndTranscriptsWithStreamedResponse

    # client options

    def __init__(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async endex-factset-events-and-transcripts client instance."""
        if base_url is None:
            base_url = os.environ.get("ENDEX_FACTSET_EVENTS_AND_TRANSCRIPTS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.factset.com/events/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.calendar_events = resources.AsyncCalendarEventsResource(self)
        self.events_audio = resources.AsyncEventsAudioResource(self)
        self.near_real_time_transcripts = resources.AsyncNearRealTimeTranscriptsResource(self)
        self.transcripts = resources.AsyncTranscriptsResource(self)
        self.reference = resources.AsyncReferenceResource(self)
        self.with_raw_response = AsyncEndexFactsetEventsAndTranscriptsWithRawResponse(self)
        self.with_streaming_response = AsyncEndexFactsetEventsAndTranscriptsWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class EndexFactsetEventsAndTranscriptsWithRawResponse:
    def __init__(self, client: EndexFactsetEventsAndTranscripts) -> None:
        self.calendar_events = resources.CalendarEventsResourceWithRawResponse(client.calendar_events)
        self.events_audio = resources.EventsAudioResourceWithRawResponse(client.events_audio)
        self.near_real_time_transcripts = resources.NearRealTimeTranscriptsResourceWithRawResponse(
            client.near_real_time_transcripts
        )
        self.transcripts = resources.TranscriptsResourceWithRawResponse(client.transcripts)
        self.reference = resources.ReferenceResourceWithRawResponse(client.reference)


class AsyncEndexFactsetEventsAndTranscriptsWithRawResponse:
    def __init__(self, client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        self.calendar_events = resources.AsyncCalendarEventsResourceWithRawResponse(client.calendar_events)
        self.events_audio = resources.AsyncEventsAudioResourceWithRawResponse(client.events_audio)
        self.near_real_time_transcripts = resources.AsyncNearRealTimeTranscriptsResourceWithRawResponse(
            client.near_real_time_transcripts
        )
        self.transcripts = resources.AsyncTranscriptsResourceWithRawResponse(client.transcripts)
        self.reference = resources.AsyncReferenceResourceWithRawResponse(client.reference)


class EndexFactsetEventsAndTranscriptsWithStreamedResponse:
    def __init__(self, client: EndexFactsetEventsAndTranscripts) -> None:
        self.calendar_events = resources.CalendarEventsResourceWithStreamingResponse(client.calendar_events)
        self.events_audio = resources.EventsAudioResourceWithStreamingResponse(client.events_audio)
        self.near_real_time_transcripts = resources.NearRealTimeTranscriptsResourceWithStreamingResponse(
            client.near_real_time_transcripts
        )
        self.transcripts = resources.TranscriptsResourceWithStreamingResponse(client.transcripts)
        self.reference = resources.ReferenceResourceWithStreamingResponse(client.reference)


class AsyncEndexFactsetEventsAndTranscriptsWithStreamedResponse:
    def __init__(self, client: AsyncEndexFactsetEventsAndTranscripts) -> None:
        self.calendar_events = resources.AsyncCalendarEventsResourceWithStreamingResponse(client.calendar_events)
        self.events_audio = resources.AsyncEventsAudioResourceWithStreamingResponse(client.events_audio)
        self.near_real_time_transcripts = resources.AsyncNearRealTimeTranscriptsResourceWithStreamingResponse(
            client.near_real_time_transcripts
        )
        self.transcripts = resources.AsyncTranscriptsResourceWithStreamingResponse(client.transcripts)
        self.reference = resources.AsyncReferenceResourceWithStreamingResponse(client.reference)


Client = EndexFactsetEventsAndTranscripts

AsyncClient = AsyncEndexFactsetEventsAndTranscripts
