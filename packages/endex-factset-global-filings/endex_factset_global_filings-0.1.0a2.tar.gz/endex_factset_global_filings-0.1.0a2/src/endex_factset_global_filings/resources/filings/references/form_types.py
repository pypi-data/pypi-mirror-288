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
from ....types.filings.references.form_type_list_response import FormTypeListResponse

__all__ = ["FormTypesResource", "AsyncFormTypesResource"]


class FormTypesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FormTypesResourceWithRawResponse:
        return FormTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FormTypesResourceWithStreamingResponse:
        return FormTypesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormTypeListResponse:
        """Retrieves and delivers a comprehensive list of all available `formTypes`."""
        return self._get(
            "/reference/form-types",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormTypeListResponse,
        )


class AsyncFormTypesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFormTypesResourceWithRawResponse:
        return AsyncFormTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFormTypesResourceWithStreamingResponse:
        return AsyncFormTypesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormTypeListResponse:
        """Retrieves and delivers a comprehensive list of all available `formTypes`."""
        return await self._get(
            "/reference/form-types",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormTypeListResponse,
        )


class FormTypesResourceWithRawResponse:
    def __init__(self, form_types: FormTypesResource) -> None:
        self._form_types = form_types

        self.list = to_raw_response_wrapper(
            form_types.list,
        )


class AsyncFormTypesResourceWithRawResponse:
    def __init__(self, form_types: AsyncFormTypesResource) -> None:
        self._form_types = form_types

        self.list = async_to_raw_response_wrapper(
            form_types.list,
        )


class FormTypesResourceWithStreamingResponse:
    def __init__(self, form_types: FormTypesResource) -> None:
        self._form_types = form_types

        self.list = to_streamed_response_wrapper(
            form_types.list,
        )


class AsyncFormTypesResourceWithStreamingResponse:
    def __init__(self, form_types: AsyncFormTypesResource) -> None:
        self._form_types = form_types

        self.list = async_to_streamed_response_wrapper(
            form_types.list,
        )
