# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .v2 import (
    V2Resource,
    AsyncV2Resource,
    V2ResourceWithRawResponse,
    AsyncV2ResourceWithRawResponse,
    V2ResourceWithStreamingResponse,
    AsyncV2ResourceWithStreamingResponse,
)
from .v2.v2 import V2Resource, AsyncV2Resource
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["FactsetEstimatesResource", "AsyncFactsetEstimatesResource"]


class FactsetEstimatesResource(SyncAPIResource):
    @cached_property
    def v2(self) -> V2Resource:
        return V2Resource(self._client)

    @cached_property
    def with_raw_response(self) -> FactsetEstimatesResourceWithRawResponse:
        return FactsetEstimatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FactsetEstimatesResourceWithStreamingResponse:
        return FactsetEstimatesResourceWithStreamingResponse(self)


class AsyncFactsetEstimatesResource(AsyncAPIResource):
    @cached_property
    def v2(self) -> AsyncV2Resource:
        return AsyncV2Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFactsetEstimatesResourceWithRawResponse:
        return AsyncFactsetEstimatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFactsetEstimatesResourceWithStreamingResponse:
        return AsyncFactsetEstimatesResourceWithStreamingResponse(self)


class FactsetEstimatesResourceWithRawResponse:
    def __init__(self, factset_estimates: FactsetEstimatesResource) -> None:
        self._factset_estimates = factset_estimates

    @cached_property
    def v2(self) -> V2ResourceWithRawResponse:
        return V2ResourceWithRawResponse(self._factset_estimates.v2)


class AsyncFactsetEstimatesResourceWithRawResponse:
    def __init__(self, factset_estimates: AsyncFactsetEstimatesResource) -> None:
        self._factset_estimates = factset_estimates

    @cached_property
    def v2(self) -> AsyncV2ResourceWithRawResponse:
        return AsyncV2ResourceWithRawResponse(self._factset_estimates.v2)


class FactsetEstimatesResourceWithStreamingResponse:
    def __init__(self, factset_estimates: FactsetEstimatesResource) -> None:
        self._factset_estimates = factset_estimates

    @cached_property
    def v2(self) -> V2ResourceWithStreamingResponse:
        return V2ResourceWithStreamingResponse(self._factset_estimates.v2)


class AsyncFactsetEstimatesResourceWithStreamingResponse:
    def __init__(self, factset_estimates: AsyncFactsetEstimatesResource) -> None:
        self._factset_estimates = factset_estimates

    @cached_property
    def v2(self) -> AsyncV2ResourceWithStreamingResponse:
        return AsyncV2ResourceWithStreamingResponse(self._factset_estimates.v2)
