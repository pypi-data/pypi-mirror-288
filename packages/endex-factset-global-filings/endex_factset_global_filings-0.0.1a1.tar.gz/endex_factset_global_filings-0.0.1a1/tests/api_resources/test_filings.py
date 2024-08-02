# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_filings import EndexFactsetGlobalFilings, AsyncEndexFactsetGlobalFilings
from endex_factset_global_filings.types import (
    InvestmentResearch,
    FilingCountResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFilings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_count(self, client: EndexFactsetGlobalFilings) -> None:
        filing = client.filings.count(
            sources=["string", "string", "string"],
        )
        assert_matches_type(FilingCountResponse, filing, path=["response"])

    @parametrize
    def test_method_count_with_all_params(self, client: EndexFactsetGlobalFilings) -> None:
        filing = client.filings.count(
            sources=["string", "string", "string"],
            end_date="endDate",
            ids=["string", "string", "string"],
            start_date="startDate",
        )
        assert_matches_type(FilingCountResponse, filing, path=["response"])

    @parametrize
    def test_raw_response_count(self, client: EndexFactsetGlobalFilings) -> None:
        response = client.filings.with_raw_response.count(
            sources=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        filing = response.parse()
        assert_matches_type(FilingCountResponse, filing, path=["response"])

    @parametrize
    def test_streaming_response_count(self, client: EndexFactsetGlobalFilings) -> None:
        with client.filings.with_streaming_response.count(
            sources=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            filing = response.parse()
            assert_matches_type(FilingCountResponse, filing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search(self, client: EndexFactsetGlobalFilings) -> None:
        filing = client.filings.search(
            sources=["string", "string", "string"],
        )
        assert_matches_type(InvestmentResearch, filing, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: EndexFactsetGlobalFilings) -> None:
        filing = client.filings.search(
            sources=["string", "string", "string"],
            _pagination_limit=0,
            _pagination_offset=0,
            categories=["string", "string", "string"],
            edgar_accession="edgarAccession",
            edgar_form_type="edgarFormType",
            end_date="endDate",
            ids=["string", "string", "string"],
            primary_id=True,
            search_text="searchText",
            sort="asc",
            start_date="startDate",
            time_zone="timeZone",
        )
        assert_matches_type(InvestmentResearch, filing, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: EndexFactsetGlobalFilings) -> None:
        response = client.filings.with_raw_response.search(
            sources=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        filing = response.parse()
        assert_matches_type(InvestmentResearch, filing, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: EndexFactsetGlobalFilings) -> None:
        with client.filings.with_streaming_response.search(
            sources=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            filing = response.parse()
            assert_matches_type(InvestmentResearch, filing, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFilings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_count(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        filing = await async_client.filings.count(
            sources=["string", "string", "string"],
        )
        assert_matches_type(FilingCountResponse, filing, path=["response"])

    @parametrize
    async def test_method_count_with_all_params(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        filing = await async_client.filings.count(
            sources=["string", "string", "string"],
            end_date="endDate",
            ids=["string", "string", "string"],
            start_date="startDate",
        )
        assert_matches_type(FilingCountResponse, filing, path=["response"])

    @parametrize
    async def test_raw_response_count(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        response = await async_client.filings.with_raw_response.count(
            sources=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        filing = await response.parse()
        assert_matches_type(FilingCountResponse, filing, path=["response"])

    @parametrize
    async def test_streaming_response_count(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        async with async_client.filings.with_streaming_response.count(
            sources=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            filing = await response.parse()
            assert_matches_type(FilingCountResponse, filing, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        filing = await async_client.filings.search(
            sources=["string", "string", "string"],
        )
        assert_matches_type(InvestmentResearch, filing, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        filing = await async_client.filings.search(
            sources=["string", "string", "string"],
            _pagination_limit=0,
            _pagination_offset=0,
            categories=["string", "string", "string"],
            edgar_accession="edgarAccession",
            edgar_form_type="edgarFormType",
            end_date="endDate",
            ids=["string", "string", "string"],
            primary_id=True,
            search_text="searchText",
            sort="asc",
            start_date="startDate",
            time_zone="timeZone",
        )
        assert_matches_type(InvestmentResearch, filing, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        response = await async_client.filings.with_raw_response.search(
            sources=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        filing = await response.parse()
        assert_matches_type(InvestmentResearch, filing, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        async with async_client.filings.with_streaming_response.search(
            sources=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            filing = await response.parse()
            assert_matches_type(InvestmentResearch, filing, path=["response"])

        assert cast(Any, response.is_closed) is True
