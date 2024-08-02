# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.filings.references.source_list_response import SourceListResponse

__all__ = ["SourcesResource", "AsyncSourcesResource"]


class SourcesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SourcesResourceWithRawResponse:
        return SourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SourcesResourceWithStreamingResponse:
        return SourcesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SourceListResponse:
        """Retrieves and delivers a comprehensive list of all available `sources`."""
        return self._get(
            "/reference/sources",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SourceListResponse,
        )


class AsyncSourcesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSourcesResourceWithRawResponse:
        return AsyncSourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSourcesResourceWithStreamingResponse:
        return AsyncSourcesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SourceListResponse:
        """Retrieves and delivers a comprehensive list of all available `sources`."""
        return await self._get(
            "/reference/sources",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SourceListResponse,
        )


class SourcesResourceWithRawResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.list = to_raw_response_wrapper(
            sources.list,
        )


class AsyncSourcesResourceWithRawResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.list = async_to_raw_response_wrapper(
            sources.list,
        )


class SourcesResourceWithStreamingResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.list = to_streamed_response_wrapper(
            sources.list,
        )


class AsyncSourcesResourceWithStreamingResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.list = async_to_streamed_response_wrapper(
            sources.list,
        )
