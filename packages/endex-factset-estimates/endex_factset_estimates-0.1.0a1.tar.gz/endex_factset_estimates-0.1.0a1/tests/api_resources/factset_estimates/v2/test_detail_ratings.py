# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_estimates import EndexFactsetEstimates, AsyncEndexFactsetEstimates
from endex_factset_estimates.types.factset_estimates.v2 import (
    DetailRatingsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDetailRatings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetEstimates) -> None:
        detail_rating = client.factset_estimates.v2.detail_ratings.create(
            ids=["FDS-US"],
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetEstimates) -> None:
        detail_rating = client.factset_estimates.v2.detail_ratings.create(
            ids=["FDS-US"],
            end_date="2019-12-31",
            include_all=False,
            start_date="2019-01-01",
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetEstimates) -> None:
        response = client.factset_estimates.v2.detail_ratings.with_raw_response.create(
            ids=["FDS-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        detail_rating = response.parse()
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetEstimates) -> None:
        with client.factset_estimates.v2.detail_ratings.with_streaming_response.create(
            ids=["FDS-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            detail_rating = response.parse()
            assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetEstimates) -> None:
        detail_rating = client.factset_estimates.v2.detail_ratings.retrieve(
            ids=["string"],
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetEstimates) -> None:
        detail_rating = client.factset_estimates.v2.detail_ratings.retrieve(
            ids=["string"],
            end_date="endDate",
            include_all=True,
            start_date="startDate",
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetEstimates) -> None:
        response = client.factset_estimates.v2.detail_ratings.with_raw_response.retrieve(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        detail_rating = response.parse()
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetEstimates) -> None:
        with client.factset_estimates.v2.detail_ratings.with_streaming_response.retrieve(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            detail_rating = response.parse()
            assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDetailRatings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        detail_rating = await async_client.factset_estimates.v2.detail_ratings.create(
            ids=["FDS-US"],
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetEstimates) -> None:
        detail_rating = await async_client.factset_estimates.v2.detail_ratings.create(
            ids=["FDS-US"],
            end_date="2019-12-31",
            include_all=False,
            start_date="2019-01-01",
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        response = await async_client.factset_estimates.v2.detail_ratings.with_raw_response.create(
            ids=["FDS-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        detail_rating = await response.parse()
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        async with async_client.factset_estimates.v2.detail_ratings.with_streaming_response.create(
            ids=["FDS-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            detail_rating = await response.parse()
            assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetEstimates) -> None:
        detail_rating = await async_client.factset_estimates.v2.detail_ratings.retrieve(
            ids=["string"],
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetEstimates) -> None:
        detail_rating = await async_client.factset_estimates.v2.detail_ratings.retrieve(
            ids=["string"],
            end_date="endDate",
            include_all=True,
            start_date="startDate",
        )
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetEstimates) -> None:
        response = await async_client.factset_estimates.v2.detail_ratings.with_raw_response.retrieve(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        detail_rating = await response.parse()
        assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetEstimates) -> None:
        async with async_client.factset_estimates.v2.detail_ratings.with_streaming_response.retrieve(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            detail_rating = await response.parse()
            assert_matches_type(DetailRatingsResponse, detail_rating, path=["response"])

        assert cast(Any, response.is_closed) is True
