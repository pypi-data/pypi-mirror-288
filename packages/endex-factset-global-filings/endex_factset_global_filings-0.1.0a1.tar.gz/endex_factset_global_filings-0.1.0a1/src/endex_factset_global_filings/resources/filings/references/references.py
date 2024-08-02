# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .sources import (
    SourcesResource,
    AsyncSourcesResource,
    SourcesResourceWithRawResponse,
    AsyncSourcesResourceWithRawResponse,
    SourcesResourceWithStreamingResponse,
    AsyncSourcesResourceWithStreamingResponse,
)
from ...._compat import cached_property
from .categories import (
    CategoriesResource,
    AsyncCategoriesResource,
    CategoriesResourceWithRawResponse,
    AsyncCategoriesResourceWithRawResponse,
    CategoriesResourceWithStreamingResponse,
    AsyncCategoriesResourceWithStreamingResponse,
)
from .form_types import (
    FormTypesResource,
    AsyncFormTypesResource,
    FormTypesResourceWithRawResponse,
    AsyncFormTypesResourceWithRawResponse,
    FormTypesResourceWithStreamingResponse,
    AsyncFormTypesResourceWithStreamingResponse,
)
from .time_zones import (
    TimeZonesResource,
    AsyncTimeZonesResource,
    TimeZonesResourceWithRawResponse,
    AsyncTimeZonesResourceWithRawResponse,
    TimeZonesResourceWithStreamingResponse,
    AsyncTimeZonesResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["ReferencesResource", "AsyncReferencesResource"]


class ReferencesResource(SyncAPIResource):
    @cached_property
    def sources(self) -> SourcesResource:
        return SourcesResource(self._client)

    @cached_property
    def form_types(self) -> FormTypesResource:
        return FormTypesResource(self._client)

    @cached_property
    def time_zones(self) -> TimeZonesResource:
        return TimeZonesResource(self._client)

    @cached_property
    def categories(self) -> CategoriesResource:
        return CategoriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ReferencesResourceWithRawResponse:
        return ReferencesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReferencesResourceWithStreamingResponse:
        return ReferencesResourceWithStreamingResponse(self)


class AsyncReferencesResource(AsyncAPIResource):
    @cached_property
    def sources(self) -> AsyncSourcesResource:
        return AsyncSourcesResource(self._client)

    @cached_property
    def form_types(self) -> AsyncFormTypesResource:
        return AsyncFormTypesResource(self._client)

    @cached_property
    def time_zones(self) -> AsyncTimeZonesResource:
        return AsyncTimeZonesResource(self._client)

    @cached_property
    def categories(self) -> AsyncCategoriesResource:
        return AsyncCategoriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncReferencesResourceWithRawResponse:
        return AsyncReferencesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReferencesResourceWithStreamingResponse:
        return AsyncReferencesResourceWithStreamingResponse(self)


class ReferencesResourceWithRawResponse:
    def __init__(self, references: ReferencesResource) -> None:
        self._references = references

    @cached_property
    def sources(self) -> SourcesResourceWithRawResponse:
        return SourcesResourceWithRawResponse(self._references.sources)

    @cached_property
    def form_types(self) -> FormTypesResourceWithRawResponse:
        return FormTypesResourceWithRawResponse(self._references.form_types)

    @cached_property
    def time_zones(self) -> TimeZonesResourceWithRawResponse:
        return TimeZonesResourceWithRawResponse(self._references.time_zones)

    @cached_property
    def categories(self) -> CategoriesResourceWithRawResponse:
        return CategoriesResourceWithRawResponse(self._references.categories)


class AsyncReferencesResourceWithRawResponse:
    def __init__(self, references: AsyncReferencesResource) -> None:
        self._references = references

    @cached_property
    def sources(self) -> AsyncSourcesResourceWithRawResponse:
        return AsyncSourcesResourceWithRawResponse(self._references.sources)

    @cached_property
    def form_types(self) -> AsyncFormTypesResourceWithRawResponse:
        return AsyncFormTypesResourceWithRawResponse(self._references.form_types)

    @cached_property
    def time_zones(self) -> AsyncTimeZonesResourceWithRawResponse:
        return AsyncTimeZonesResourceWithRawResponse(self._references.time_zones)

    @cached_property
    def categories(self) -> AsyncCategoriesResourceWithRawResponse:
        return AsyncCategoriesResourceWithRawResponse(self._references.categories)


class ReferencesResourceWithStreamingResponse:
    def __init__(self, references: ReferencesResource) -> None:
        self._references = references

    @cached_property
    def sources(self) -> SourcesResourceWithStreamingResponse:
        return SourcesResourceWithStreamingResponse(self._references.sources)

    @cached_property
    def form_types(self) -> FormTypesResourceWithStreamingResponse:
        return FormTypesResourceWithStreamingResponse(self._references.form_types)

    @cached_property
    def time_zones(self) -> TimeZonesResourceWithStreamingResponse:
        return TimeZonesResourceWithStreamingResponse(self._references.time_zones)

    @cached_property
    def categories(self) -> CategoriesResourceWithStreamingResponse:
        return CategoriesResourceWithStreamingResponse(self._references.categories)


class AsyncReferencesResourceWithStreamingResponse:
    def __init__(self, references: AsyncReferencesResource) -> None:
        self._references = references

    @cached_property
    def sources(self) -> AsyncSourcesResourceWithStreamingResponse:
        return AsyncSourcesResourceWithStreamingResponse(self._references.sources)

    @cached_property
    def form_types(self) -> AsyncFormTypesResourceWithStreamingResponse:
        return AsyncFormTypesResourceWithStreamingResponse(self._references.form_types)

    @cached_property
    def time_zones(self) -> AsyncTimeZonesResourceWithStreamingResponse:
        return AsyncTimeZonesResourceWithStreamingResponse(self._references.time_zones)

    @cached_property
    def categories(self) -> AsyncCategoriesResourceWithStreamingResponse:
        return AsyncCategoriesResourceWithStreamingResponse(self._references.categories)
