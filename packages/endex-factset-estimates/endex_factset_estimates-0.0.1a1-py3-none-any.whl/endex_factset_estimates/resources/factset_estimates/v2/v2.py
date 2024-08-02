# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .metrics import (
    MetricsResource,
    AsyncMetricsResource,
    MetricsResourceWithRawResponse,
    AsyncMetricsResourceWithRawResponse,
    MetricsResourceWithStreamingResponse,
    AsyncMetricsResourceWithStreamingResponse,
)
from .segments import (
    SegmentsResource,
    AsyncSegmentsResource,
    SegmentsResourceWithRawResponse,
    AsyncSegmentsResourceWithRawResponse,
    SegmentsResourceWithStreamingResponse,
    AsyncSegmentsResourceWithStreamingResponse,
)
from .surprise import (
    SurpriseResource,
    AsyncSurpriseResource,
    SurpriseResourceWithRawResponse,
    AsyncSurpriseResourceWithRawResponse,
    SurpriseResourceWithStreamingResponse,
    AsyncSurpriseResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .fixed_detail import (
    FixedDetailResource,
    AsyncFixedDetailResource,
    FixedDetailResourceWithRawResponse,
    AsyncFixedDetailResourceWithRawResponse,
    FixedDetailResourceWithStreamingResponse,
    AsyncFixedDetailResourceWithStreamingResponse,
)
from .detail_ratings import (
    DetailRatingsResource,
    AsyncDetailRatingsResource,
    DetailRatingsResourceWithRawResponse,
    AsyncDetailRatingsResourceWithRawResponse,
    DetailRatingsResourceWithStreamingResponse,
    AsyncDetailRatingsResourceWithStreamingResponse,
)
from .rolling_detail import (
    RollingDetailResource,
    AsyncRollingDetailResource,
    RollingDetailResourceWithRawResponse,
    AsyncRollingDetailResourceWithRawResponse,
    RollingDetailResourceWithStreamingResponse,
    AsyncRollingDetailResourceWithStreamingResponse,
)
from .fixed_consensus import (
    FixedConsensusResource,
    AsyncFixedConsensusResource,
    FixedConsensusResourceWithRawResponse,
    AsyncFixedConsensusResourceWithRawResponse,
    FixedConsensusResourceWithStreamingResponse,
    AsyncFixedConsensusResourceWithStreamingResponse,
)
from .consensus_ratings import (
    ConsensusRatingsResource,
    AsyncConsensusRatingsResource,
    ConsensusRatingsResourceWithRawResponse,
    AsyncConsensusRatingsResourceWithRawResponse,
    ConsensusRatingsResourceWithStreamingResponse,
    AsyncConsensusRatingsResourceWithStreamingResponse,
)
from .rolling_consensus import (
    RollingConsensusResource,
    AsyncRollingConsensusResource,
    RollingConsensusResourceWithRawResponse,
    AsyncRollingConsensusResourceWithRawResponse,
    RollingConsensusResourceWithStreamingResponse,
    AsyncRollingConsensusResourceWithStreamingResponse,
)

__all__ = ["V2Resource", "AsyncV2Resource"]


class V2Resource(SyncAPIResource):
    @cached_property
    def rolling_consensus(self) -> RollingConsensusResource:
        return RollingConsensusResource(self._client)

    @cached_property
    def fixed_consensus(self) -> FixedConsensusResource:
        return FixedConsensusResource(self._client)

    @cached_property
    def rolling_detail(self) -> RollingDetailResource:
        return RollingDetailResource(self._client)

    @cached_property
    def fixed_detail(self) -> FixedDetailResource:
        return FixedDetailResource(self._client)

    @cached_property
    def consensus_ratings(self) -> ConsensusRatingsResource:
        return ConsensusRatingsResource(self._client)

    @cached_property
    def detail_ratings(self) -> DetailRatingsResource:
        return DetailRatingsResource(self._client)

    @cached_property
    def surprise(self) -> SurpriseResource:
        return SurpriseResource(self._client)

    @cached_property
    def segments(self) -> SegmentsResource:
        return SegmentsResource(self._client)

    @cached_property
    def metrics(self) -> MetricsResource:
        return MetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> V2ResourceWithRawResponse:
        return V2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V2ResourceWithStreamingResponse:
        return V2ResourceWithStreamingResponse(self)


class AsyncV2Resource(AsyncAPIResource):
    @cached_property
    def rolling_consensus(self) -> AsyncRollingConsensusResource:
        return AsyncRollingConsensusResource(self._client)

    @cached_property
    def fixed_consensus(self) -> AsyncFixedConsensusResource:
        return AsyncFixedConsensusResource(self._client)

    @cached_property
    def rolling_detail(self) -> AsyncRollingDetailResource:
        return AsyncRollingDetailResource(self._client)

    @cached_property
    def fixed_detail(self) -> AsyncFixedDetailResource:
        return AsyncFixedDetailResource(self._client)

    @cached_property
    def consensus_ratings(self) -> AsyncConsensusRatingsResource:
        return AsyncConsensusRatingsResource(self._client)

    @cached_property
    def detail_ratings(self) -> AsyncDetailRatingsResource:
        return AsyncDetailRatingsResource(self._client)

    @cached_property
    def surprise(self) -> AsyncSurpriseResource:
        return AsyncSurpriseResource(self._client)

    @cached_property
    def segments(self) -> AsyncSegmentsResource:
        return AsyncSegmentsResource(self._client)

    @cached_property
    def metrics(self) -> AsyncMetricsResource:
        return AsyncMetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV2ResourceWithRawResponse:
        return AsyncV2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV2ResourceWithStreamingResponse:
        return AsyncV2ResourceWithStreamingResponse(self)


class V2ResourceWithRawResponse:
    def __init__(self, v2: V2Resource) -> None:
        self._v2 = v2

    @cached_property
    def rolling_consensus(self) -> RollingConsensusResourceWithRawResponse:
        return RollingConsensusResourceWithRawResponse(self._v2.rolling_consensus)

    @cached_property
    def fixed_consensus(self) -> FixedConsensusResourceWithRawResponse:
        return FixedConsensusResourceWithRawResponse(self._v2.fixed_consensus)

    @cached_property
    def rolling_detail(self) -> RollingDetailResourceWithRawResponse:
        return RollingDetailResourceWithRawResponse(self._v2.rolling_detail)

    @cached_property
    def fixed_detail(self) -> FixedDetailResourceWithRawResponse:
        return FixedDetailResourceWithRawResponse(self._v2.fixed_detail)

    @cached_property
    def consensus_ratings(self) -> ConsensusRatingsResourceWithRawResponse:
        return ConsensusRatingsResourceWithRawResponse(self._v2.consensus_ratings)

    @cached_property
    def detail_ratings(self) -> DetailRatingsResourceWithRawResponse:
        return DetailRatingsResourceWithRawResponse(self._v2.detail_ratings)

    @cached_property
    def surprise(self) -> SurpriseResourceWithRawResponse:
        return SurpriseResourceWithRawResponse(self._v2.surprise)

    @cached_property
    def segments(self) -> SegmentsResourceWithRawResponse:
        return SegmentsResourceWithRawResponse(self._v2.segments)

    @cached_property
    def metrics(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self._v2.metrics)


class AsyncV2ResourceWithRawResponse:
    def __init__(self, v2: AsyncV2Resource) -> None:
        self._v2 = v2

    @cached_property
    def rolling_consensus(self) -> AsyncRollingConsensusResourceWithRawResponse:
        return AsyncRollingConsensusResourceWithRawResponse(self._v2.rolling_consensus)

    @cached_property
    def fixed_consensus(self) -> AsyncFixedConsensusResourceWithRawResponse:
        return AsyncFixedConsensusResourceWithRawResponse(self._v2.fixed_consensus)

    @cached_property
    def rolling_detail(self) -> AsyncRollingDetailResourceWithRawResponse:
        return AsyncRollingDetailResourceWithRawResponse(self._v2.rolling_detail)

    @cached_property
    def fixed_detail(self) -> AsyncFixedDetailResourceWithRawResponse:
        return AsyncFixedDetailResourceWithRawResponse(self._v2.fixed_detail)

    @cached_property
    def consensus_ratings(self) -> AsyncConsensusRatingsResourceWithRawResponse:
        return AsyncConsensusRatingsResourceWithRawResponse(self._v2.consensus_ratings)

    @cached_property
    def detail_ratings(self) -> AsyncDetailRatingsResourceWithRawResponse:
        return AsyncDetailRatingsResourceWithRawResponse(self._v2.detail_ratings)

    @cached_property
    def surprise(self) -> AsyncSurpriseResourceWithRawResponse:
        return AsyncSurpriseResourceWithRawResponse(self._v2.surprise)

    @cached_property
    def segments(self) -> AsyncSegmentsResourceWithRawResponse:
        return AsyncSegmentsResourceWithRawResponse(self._v2.segments)

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self._v2.metrics)


class V2ResourceWithStreamingResponse:
    def __init__(self, v2: V2Resource) -> None:
        self._v2 = v2

    @cached_property
    def rolling_consensus(self) -> RollingConsensusResourceWithStreamingResponse:
        return RollingConsensusResourceWithStreamingResponse(self._v2.rolling_consensus)

    @cached_property
    def fixed_consensus(self) -> FixedConsensusResourceWithStreamingResponse:
        return FixedConsensusResourceWithStreamingResponse(self._v2.fixed_consensus)

    @cached_property
    def rolling_detail(self) -> RollingDetailResourceWithStreamingResponse:
        return RollingDetailResourceWithStreamingResponse(self._v2.rolling_detail)

    @cached_property
    def fixed_detail(self) -> FixedDetailResourceWithStreamingResponse:
        return FixedDetailResourceWithStreamingResponse(self._v2.fixed_detail)

    @cached_property
    def consensus_ratings(self) -> ConsensusRatingsResourceWithStreamingResponse:
        return ConsensusRatingsResourceWithStreamingResponse(self._v2.consensus_ratings)

    @cached_property
    def detail_ratings(self) -> DetailRatingsResourceWithStreamingResponse:
        return DetailRatingsResourceWithStreamingResponse(self._v2.detail_ratings)

    @cached_property
    def surprise(self) -> SurpriseResourceWithStreamingResponse:
        return SurpriseResourceWithStreamingResponse(self._v2.surprise)

    @cached_property
    def segments(self) -> SegmentsResourceWithStreamingResponse:
        return SegmentsResourceWithStreamingResponse(self._v2.segments)

    @cached_property
    def metrics(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self._v2.metrics)


class AsyncV2ResourceWithStreamingResponse:
    def __init__(self, v2: AsyncV2Resource) -> None:
        self._v2 = v2

    @cached_property
    def rolling_consensus(self) -> AsyncRollingConsensusResourceWithStreamingResponse:
        return AsyncRollingConsensusResourceWithStreamingResponse(self._v2.rolling_consensus)

    @cached_property
    def fixed_consensus(self) -> AsyncFixedConsensusResourceWithStreamingResponse:
        return AsyncFixedConsensusResourceWithStreamingResponse(self._v2.fixed_consensus)

    @cached_property
    def rolling_detail(self) -> AsyncRollingDetailResourceWithStreamingResponse:
        return AsyncRollingDetailResourceWithStreamingResponse(self._v2.rolling_detail)

    @cached_property
    def fixed_detail(self) -> AsyncFixedDetailResourceWithStreamingResponse:
        return AsyncFixedDetailResourceWithStreamingResponse(self._v2.fixed_detail)

    @cached_property
    def consensus_ratings(self) -> AsyncConsensusRatingsResourceWithStreamingResponse:
        return AsyncConsensusRatingsResourceWithStreamingResponse(self._v2.consensus_ratings)

    @cached_property
    def detail_ratings(self) -> AsyncDetailRatingsResourceWithStreamingResponse:
        return AsyncDetailRatingsResourceWithStreamingResponse(self._v2.detail_ratings)

    @cached_property
    def surprise(self) -> AsyncSurpriseResourceWithStreamingResponse:
        return AsyncSurpriseResourceWithStreamingResponse(self._v2.surprise)

    @cached_property
    def segments(self) -> AsyncSegmentsResourceWithStreamingResponse:
        return AsyncSegmentsResourceWithStreamingResponse(self._v2.segments)

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self._v2.metrics)
