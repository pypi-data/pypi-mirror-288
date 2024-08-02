# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ...types import filing_count_params, filing_search_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .references import (
    ReferencesResource,
    AsyncReferencesResource,
    ReferencesResourceWithRawResponse,
    AsyncReferencesResourceWithRawResponse,
    ReferencesResourceWithStreamingResponse,
    AsyncReferencesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .references.references import ReferencesResource, AsyncReferencesResource
from ...types.investment_research import InvestmentResearch
from ...types.filing_count_response import FilingCountResponse

__all__ = ["FilingsResource", "AsyncFilingsResource"]


class FilingsResource(SyncAPIResource):
    @cached_property
    def references(self) -> ReferencesResource:
        return ReferencesResource(self._client)

    @cached_property
    def with_raw_response(self) -> FilingsResourceWithRawResponse:
        return FilingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilingsResourceWithStreamingResponse:
        return FilingsResourceWithStreamingResponse(self)

    def count(
        self,
        *,
        sources: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FilingCountResponse:
        """
        Returns the count of filings documents along with other response fields.

        Args:
          sources: Code for document source to include.This is a comma-separated list. Use the
              `/reference/sources` endpoint to get the list of available sources.

          end_date: End Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

          ids: Requested symbols or securities. This is a comma-separated list with a maximum
              limit of 1000. Each symbol can be a FactSet exchange symbol, CUSIP, or SEDOL.

          start_date: Start Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

              **Note:** **The API supports data from 1995 onwards. Ensure that the provided
              Date falls within this range for accurate results.**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/count",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "sources": sources,
                        "end_date": end_date,
                        "ids": ids,
                        "start_date": start_date,
                    },
                    filing_count_params.FilingCountParams,
                ),
            ),
            cast_to=FilingCountResponse,
        )

    def search(
        self,
        *,
        sources: List[str],
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        categories: List[str] | NotGiven = NOT_GIVEN,
        edgar_accession: str | NotGiven = NOT_GIVEN,
        edgar_form_type: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        primary_id: Literal[True, False] | NotGiven = NOT_GIVEN,
        search_text: str | NotGiven = NOT_GIVEN,
        sort: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        time_zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> InvestmentResearch:
        """
        Returns the filings documents within FactSet coverage along with other response
        fields.

        Args:
          sources: Code for document source to include. This is a comma-separated list. Use the
              `/reference/sources` endpoint to get the list of available sources.

          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          categories: Code for categories to include. This is a comma-separated list. Use the
              `/reference/categories` endpoint to get the list of available categories.

              Default = All categories.

          edgar_accession: A unique identifier given to each EDGAR filings document. e.g.
              accession=0001013237-21-000069&sources=EDG.

              **Note: When used in conjunction with the 'source' parameter set to 'EDGAR', the
              API considers this accession for data retrieval. For non-EDGAR sources, this
              parameter is ignored.**

          edgar_form_type: Restricts the search to include any form types of EDGAR.

              **Note:This parameter applies exclusively to EDGAR searches; it is ignored when
              used with non-EDGAR sources.**

          end_date: End Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

          ids: Requested symbols or securities. This is a comma-separated list with a maximum
              limit of 1000. Each symbol can be a FactSet exchange symbol, CUSIP, or SEDOL.

          primary_id: Type of identifier search

              - true - Returns headlines of stories that have the searched identifier(s) as
                the primary identifier.
              - false - Returns headlines of stories that mentioned or referred to the
                identifier.

          search_text: Restricts the search to include only document stories which include the text
              searched.

          sort: Sorting the results in chronological (oldest to newest) or reverse chronological
              (newest to oldest) order.

              - desc - sorting results in reverse chronological (descending) order. This is
                the default value if the sort parameter isn't used in the query.
              - asc - sorting results in chronological (ascending) order. If a start date is
                not specified, the API has a 10-year searching limitation.

          start_date: Start Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

              **Note:** **The API supports data from 1995 onwards. Ensure that the provided
              Date falls within this range for accurate results.**

          time_zone: timeZone to return story dates and times.Time zones, represented in POSIX
              format, are automatically adjusted for daylight savings. timeZone names are
              sourced from the IANA timezone registry.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "sources": sources,
                        "_pagination_limit": _pagination_limit,
                        "_pagination_offset": _pagination_offset,
                        "categories": categories,
                        "edgar_accession": edgar_accession,
                        "edgar_form_type": edgar_form_type,
                        "end_date": end_date,
                        "ids": ids,
                        "primary_id": primary_id,
                        "search_text": search_text,
                        "sort": sort,
                        "start_date": start_date,
                        "time_zone": time_zone,
                    },
                    filing_search_params.FilingSearchParams,
                ),
            ),
            cast_to=InvestmentResearch,
        )


class AsyncFilingsResource(AsyncAPIResource):
    @cached_property
    def references(self) -> AsyncReferencesResource:
        return AsyncReferencesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFilingsResourceWithRawResponse:
        return AsyncFilingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilingsResourceWithStreamingResponse:
        return AsyncFilingsResourceWithStreamingResponse(self)

    async def count(
        self,
        *,
        sources: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FilingCountResponse:
        """
        Returns the count of filings documents along with other response fields.

        Args:
          sources: Code for document source to include.This is a comma-separated list. Use the
              `/reference/sources` endpoint to get the list of available sources.

          end_date: End Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

          ids: Requested symbols or securities. This is a comma-separated list with a maximum
              limit of 1000. Each symbol can be a FactSet exchange symbol, CUSIP, or SEDOL.

          start_date: Start Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

              **Note:** **The API supports data from 1995 onwards. Ensure that the provided
              Date falls within this range for accurate results.**

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/count",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "sources": sources,
                        "end_date": end_date,
                        "ids": ids,
                        "start_date": start_date,
                    },
                    filing_count_params.FilingCountParams,
                ),
            ),
            cast_to=FilingCountResponse,
        )

    async def search(
        self,
        *,
        sources: List[str],
        _pagination_limit: int | NotGiven = NOT_GIVEN,
        _pagination_offset: int | NotGiven = NOT_GIVEN,
        categories: List[str] | NotGiven = NOT_GIVEN,
        edgar_accession: str | NotGiven = NOT_GIVEN,
        edgar_form_type: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        primary_id: Literal[True, False] | NotGiven = NOT_GIVEN,
        search_text: str | NotGiven = NOT_GIVEN,
        sort: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        time_zone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> InvestmentResearch:
        """
        Returns the filings documents within FactSet coverage along with other response
        fields.

        Args:
          sources: Code for document source to include. This is a comma-separated list. Use the
              `/reference/sources` endpoint to get the list of available sources.

          _pagination_limit: Number of results to return per page.

          _pagination_offset: Page number of the results to return.

          categories: Code for categories to include. This is a comma-separated list. Use the
              `/reference/categories` endpoint to get the list of available categories.

              Default = All categories.

          edgar_accession: A unique identifier given to each EDGAR filings document. e.g.
              accession=0001013237-21-000069&sources=EDG.

              **Note: When used in conjunction with the 'source' parameter set to 'EDGAR', the
              API considers this accession for data retrieval. For non-EDGAR sources, this
              parameter is ignored.**

          edgar_form_type: Restricts the search to include any form types of EDGAR.

              **Note:This parameter applies exclusively to EDGAR searches; it is ignored when
              used with non-EDGAR sources.**

          end_date: End Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

          ids: Requested symbols or securities. This is a comma-separated list with a maximum
              limit of 1000. Each symbol can be a FactSet exchange symbol, CUSIP, or SEDOL.

          primary_id: Type of identifier search

              - true - Returns headlines of stories that have the searched identifier(s) as
                the primary identifier.
              - false - Returns headlines of stories that mentioned or referred to the
                identifier.

          search_text: Restricts the search to include only document stories which include the text
              searched.

          sort: Sorting the results in chronological (oldest to newest) or reverse chronological
              (newest to oldest) order.

              - desc - sorting results in reverse chronological (descending) order. This is
                the default value if the sort parameter isn't used in the query.
              - asc - sorting results in chronological (ascending) order. If a start date is
                not specified, the API has a 10-year searching limitation.

          start_date: Start Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

              **Note:** **The API supports data from 1995 onwards. Ensure that the provided
              Date falls within this range for accurate results.**

          time_zone: timeZone to return story dates and times.Time zones, represented in POSIX
              format, are automatically adjusted for daylight savings. timeZone names are
              sourced from the IANA timezone registry.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "sources": sources,
                        "_pagination_limit": _pagination_limit,
                        "_pagination_offset": _pagination_offset,
                        "categories": categories,
                        "edgar_accession": edgar_accession,
                        "edgar_form_type": edgar_form_type,
                        "end_date": end_date,
                        "ids": ids,
                        "primary_id": primary_id,
                        "search_text": search_text,
                        "sort": sort,
                        "start_date": start_date,
                        "time_zone": time_zone,
                    },
                    filing_search_params.FilingSearchParams,
                ),
            ),
            cast_to=InvestmentResearch,
        )


class FilingsResourceWithRawResponse:
    def __init__(self, filings: FilingsResource) -> None:
        self._filings = filings

        self.count = to_raw_response_wrapper(
            filings.count,
        )
        self.search = to_raw_response_wrapper(
            filings.search,
        )

    @cached_property
    def references(self) -> ReferencesResourceWithRawResponse:
        return ReferencesResourceWithRawResponse(self._filings.references)


class AsyncFilingsResourceWithRawResponse:
    def __init__(self, filings: AsyncFilingsResource) -> None:
        self._filings = filings

        self.count = async_to_raw_response_wrapper(
            filings.count,
        )
        self.search = async_to_raw_response_wrapper(
            filings.search,
        )

    @cached_property
    def references(self) -> AsyncReferencesResourceWithRawResponse:
        return AsyncReferencesResourceWithRawResponse(self._filings.references)


class FilingsResourceWithStreamingResponse:
    def __init__(self, filings: FilingsResource) -> None:
        self._filings = filings

        self.count = to_streamed_response_wrapper(
            filings.count,
        )
        self.search = to_streamed_response_wrapper(
            filings.search,
        )

    @cached_property
    def references(self) -> ReferencesResourceWithStreamingResponse:
        return ReferencesResourceWithStreamingResponse(self._filings.references)


class AsyncFilingsResourceWithStreamingResponse:
    def __init__(self, filings: AsyncFilingsResource) -> None:
        self._filings = filings

        self.count = async_to_streamed_response_wrapper(
            filings.count,
        )
        self.search = async_to_streamed_response_wrapper(
            filings.search,
        )

    @cached_property
    def references(self) -> AsyncReferencesResourceWithStreamingResponse:
        return AsyncReferencesResourceWithStreamingResponse(self._filings.references)
