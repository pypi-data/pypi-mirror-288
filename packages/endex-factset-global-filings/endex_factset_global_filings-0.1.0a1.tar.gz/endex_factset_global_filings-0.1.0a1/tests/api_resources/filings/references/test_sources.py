# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_global_filings import EndexFactsetGlobalFilings, AsyncEndexFactsetGlobalFilings
from endex_factset_global_filings.types.filings.references import SourceListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: EndexFactsetGlobalFilings) -> None:
        source = client.filings.references.sources.list()
        assert_matches_type(SourceListResponse, source, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetGlobalFilings) -> None:
        response = client.filings.references.sources.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        source = response.parse()
        assert_matches_type(SourceListResponse, source, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetGlobalFilings) -> None:
        with client.filings.references.sources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            source = response.parse()
            assert_matches_type(SourceListResponse, source, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSources:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        source = await async_client.filings.references.sources.list()
        assert_matches_type(SourceListResponse, source, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        response = await async_client.filings.references.sources.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        source = await response.parse()
        assert_matches_type(SourceListResponse, source, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetGlobalFilings) -> None:
        async with async_client.filings.references.sources.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            source = await response.parse()
            assert_matches_type(SourceListResponse, source, path=["response"])

        assert cast(Any, response.is_closed) is True
