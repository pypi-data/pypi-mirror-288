# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from .categories import (
    CategoriesResource,
    AsyncCategoriesResource,
    CategoriesResourceWithRawResponse,
    AsyncCategoriesResourceWithRawResponse,
    CategoriesResourceWithStreamingResponse,
    AsyncCategoriesResourceWithStreamingResponse,
)
from .time_zones import (
    TimeZonesResource,
    AsyncTimeZonesResource,
    TimeZonesResourceWithRawResponse,
    AsyncTimeZonesResourceWithRawResponse,
    TimeZonesResourceWithStreamingResponse,
    AsyncTimeZonesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ReferenceResource", "AsyncReferenceResource"]


class ReferenceResource(SyncAPIResource):
    @cached_property
    def time_zones(self) -> TimeZonesResource:
        return TimeZonesResource(self._client)

    @cached_property
    def categories(self) -> CategoriesResource:
        return CategoriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ReferenceResourceWithRawResponse:
        return ReferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReferenceResourceWithStreamingResponse:
        return ReferenceResourceWithStreamingResponse(self)


class AsyncReferenceResource(AsyncAPIResource):
    @cached_property
    def time_zones(self) -> AsyncTimeZonesResource:
        return AsyncTimeZonesResource(self._client)

    @cached_property
    def categories(self) -> AsyncCategoriesResource:
        return AsyncCategoriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncReferenceResourceWithRawResponse:
        return AsyncReferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReferenceResourceWithStreamingResponse:
        return AsyncReferenceResourceWithStreamingResponse(self)


class ReferenceResourceWithRawResponse:
    def __init__(self, reference: ReferenceResource) -> None:
        self._reference = reference

    @cached_property
    def time_zones(self) -> TimeZonesResourceWithRawResponse:
        return TimeZonesResourceWithRawResponse(self._reference.time_zones)

    @cached_property
    def categories(self) -> CategoriesResourceWithRawResponse:
        return CategoriesResourceWithRawResponse(self._reference.categories)


class AsyncReferenceResourceWithRawResponse:
    def __init__(self, reference: AsyncReferenceResource) -> None:
        self._reference = reference

    @cached_property
    def time_zones(self) -> AsyncTimeZonesResourceWithRawResponse:
        return AsyncTimeZonesResourceWithRawResponse(self._reference.time_zones)

    @cached_property
    def categories(self) -> AsyncCategoriesResourceWithRawResponse:
        return AsyncCategoriesResourceWithRawResponse(self._reference.categories)


class ReferenceResourceWithStreamingResponse:
    def __init__(self, reference: ReferenceResource) -> None:
        self._reference = reference

    @cached_property
    def time_zones(self) -> TimeZonesResourceWithStreamingResponse:
        return TimeZonesResourceWithStreamingResponse(self._reference.time_zones)

    @cached_property
    def categories(self) -> CategoriesResourceWithStreamingResponse:
        return CategoriesResourceWithStreamingResponse(self._reference.categories)


class AsyncReferenceResourceWithStreamingResponse:
    def __init__(self, reference: AsyncReferenceResource) -> None:
        self._reference = reference

    @cached_property
    def time_zones(self) -> AsyncTimeZonesResourceWithStreamingResponse:
        return AsyncTimeZonesResourceWithStreamingResponse(self._reference.time_zones)

    @cached_property
    def categories(self) -> AsyncCategoriesResourceWithStreamingResponse:
        return AsyncCategoriesResourceWithStreamingResponse(self._reference.categories)
