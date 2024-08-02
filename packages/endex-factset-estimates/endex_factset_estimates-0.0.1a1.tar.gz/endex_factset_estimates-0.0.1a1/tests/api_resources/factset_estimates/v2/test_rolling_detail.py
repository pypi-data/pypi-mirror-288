# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_estimates import EndexFactsetEstimates, AsyncEndexFactsetEstimates
from endex_factset_estimates.types.shared import DetailResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRollingDetail:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetEstimates) -> None:
        rolling_detail = client.factset_estimates.v2.rolling_detail.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetEstimates) -> None:
        rolling_detail = client.factset_estimates.v2.rolling_detail.create(
            ids=["FDS-US"],
            metrics=["SALES"],
            currency="USD",
            end_date="2019-12-31",
            frequency="AM",
            include_all=False,
            periodicity="ANN",
            relative_fiscal_end=3,
            relative_fiscal_start=1,
            start_date="2019-01-01",
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetEstimates) -> None:
        response = client.factset_estimates.v2.rolling_detail.with_raw_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rolling_detail = response.parse()
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetEstimates) -> None:
        with client.factset_estimates.v2.rolling_detail.with_streaming_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rolling_detail = response.parse()
            assert_matches_type(DetailResponse, rolling_detail, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetEstimates) -> None:
        rolling_detail = client.factset_estimates.v2.rolling_detail.list(
            ids=["string"],
            metrics=["SALES"],
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetEstimates) -> None:
        rolling_detail = client.factset_estimates.v2.rolling_detail.list(
            ids=["string"],
            metrics=["SALES"],
            currency="currency",
            end_date="endDate",
            frequency="D",
            include_all=True,
            periodicity="ANN",
            relative_fiscal_end=0,
            relative_fiscal_start=0,
            start_date="startDate",
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetEstimates) -> None:
        response = client.factset_estimates.v2.rolling_detail.with_raw_response.list(
            ids=["string"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rolling_detail = response.parse()
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetEstimates) -> None:
        with client.factset_estimates.v2.rolling_detail.with_streaming_response.list(
            ids=["string"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rolling_detail = response.parse()
            assert_matches_type(DetailResponse, rolling_detail, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRollingDetail:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        rolling_detail = await async_client.factset_estimates.v2.rolling_detail.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetEstimates) -> None:
        rolling_detail = await async_client.factset_estimates.v2.rolling_detail.create(
            ids=["FDS-US"],
            metrics=["SALES"],
            currency="USD",
            end_date="2019-12-31",
            frequency="AM",
            include_all=False,
            periodicity="ANN",
            relative_fiscal_end=3,
            relative_fiscal_start=1,
            start_date="2019-01-01",
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        response = await async_client.factset_estimates.v2.rolling_detail.with_raw_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rolling_detail = await response.parse()
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetEstimates) -> None:
        async with async_client.factset_estimates.v2.rolling_detail.with_streaming_response.create(
            ids=["FDS-US"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rolling_detail = await response.parse()
            assert_matches_type(DetailResponse, rolling_detail, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetEstimates) -> None:
        rolling_detail = await async_client.factset_estimates.v2.rolling_detail.list(
            ids=["string"],
            metrics=["SALES"],
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetEstimates) -> None:
        rolling_detail = await async_client.factset_estimates.v2.rolling_detail.list(
            ids=["string"],
            metrics=["SALES"],
            currency="currency",
            end_date="endDate",
            frequency="D",
            include_all=True,
            periodicity="ANN",
            relative_fiscal_end=0,
            relative_fiscal_start=0,
            start_date="startDate",
        )
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetEstimates) -> None:
        response = await async_client.factset_estimates.v2.rolling_detail.with_raw_response.list(
            ids=["string"],
            metrics=["SALES"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rolling_detail = await response.parse()
        assert_matches_type(DetailResponse, rolling_detail, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetEstimates) -> None:
        async with async_client.factset_estimates.v2.rolling_detail.with_streaming_response.list(
            ids=["string"],
            metrics=["SALES"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rolling_detail = await response.parse()
            assert_matches_type(DetailResponse, rolling_detail, path=["response"])

        assert cast(Any, response.is_closed) is True
