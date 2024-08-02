# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_estimates import EndexFactsetEstimates, AsyncEndexFactsetEstimates
from endex_factset_estimates.types.factset_estimates.v2 import (
    SurpriseResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSurprise:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetEstimates) -> None:
        surprise = client.factset_estimates.v2.surprise.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetEstimates) -> None:
        surprise = client.factset_estimates.v2.surprise.create(
            ids=["FDS-US"],
            metrics=["SALES"],
            currency="USD",
            end_date="2019-12-31",
            frequency="AM",
            periodicity="ANN",
            start_date="2019-01-01",
            statistic="MEDIAN",
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetEstimates) -> None:
        response = client.factset_estimates.v2.surprise.with_raw_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        surprise = response.parse()
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetEstimates) -> None:
        with client.factset_estimates.v2.surprise.with_streaming_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            surprise = response.parse()
            assert_matches_type(SurpriseResponse, surprise, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: EndexFactsetEstimates) -> None:
        surprise = client.factset_estimates.v2.surprise.retrieve(
            ids=["string"],
            metrics=["SALES"],
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: EndexFactsetEstimates) -> None:
        surprise = client.factset_estimates.v2.surprise.retrieve(
            ids=["string"],
            metrics=["SALES"],
            currency="currency",
            end_date="endDate",
            frequency="D",
            periodicity="ANN",
            start_date="startDate",
            statistic="MEAN",
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: EndexFactsetEstimates) -> None:
        response = client.factset_estimates.v2.surprise.with_raw_response.retrieve(
            ids=["string"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        surprise = response.parse()
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: EndexFactsetEstimates) -> None:
        with client.factset_estimates.v2.surprise.with_streaming_response.retrieve(
            ids=["string"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            surprise = response.parse()
            assert_matches_type(SurpriseResponse, surprise, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSurprise:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        surprise = await async_client.factset_estimates.v2.surprise.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetEstimates) -> None:
        surprise = await async_client.factset_estimates.v2.surprise.create(
            ids=["FDS-US"],
            metrics=["SALES"],
            currency="USD",
            end_date="2019-12-31",
            frequency="AM",
            periodicity="ANN",
            start_date="2019-01-01",
            statistic="MEDIAN",
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        response = await async_client.factset_estimates.v2.surprise.with_raw_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        surprise = await response.parse()
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        async with async_client.factset_estimates.v2.surprise.with_streaming_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            surprise = await response.parse()
            assert_matches_type(SurpriseResponse, surprise, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEndexFactsetEstimates) -> None:
        surprise = await async_client.factset_estimates.v2.surprise.retrieve(
            ids=["string"],
            metrics=["SALES"],
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEndexFactsetEstimates) -> None:
        surprise = await async_client.factset_estimates.v2.surprise.retrieve(
            ids=["string"],
            metrics=["SALES"],
            currency="currency",
            end_date="endDate",
            frequency="D",
            periodicity="ANN",
            start_date="startDate",
            statistic="MEAN",
        )
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEndexFactsetEstimates) -> None:
        response = await async_client.factset_estimates.v2.surprise.with_raw_response.retrieve(
            ids=["string"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        surprise = await response.parse()
        assert_matches_type(SurpriseResponse, surprise, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEndexFactsetEstimates) -> None:
        async with async_client.factset_estimates.v2.surprise.with_streaming_response.retrieve(
            ids=["string"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            surprise = await response.parse()
            assert_matches_type(SurpriseResponse, surprise, path=["response"])

        assert cast(Any, response.is_closed) is True
