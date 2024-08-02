# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.factset_estimates.v2 import consensus_rating_list_params, consensus_rating_create_params
from ....types.factset_estimates.v2.consensus_ratings_response import ConsensusRatingsResponse

__all__ = ["ConsensusRatingsResource", "AsyncConsensusRatingsResource"]


class ConsensusRatingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConsensusRatingsResourceWithRawResponse:
        return ConsensusRatingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsensusRatingsResourceWithStreamingResponse:
        return ConsensusRatingsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusRatingsResponse:
        """
        Returns ratings from the FactSet Estimates database for current and historical
        for an individual security using rolling fiscal dates as of a specific date.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. _ Make Note - id limit
              of 3000 for defaults, otherwise the service is limited to a 30 second duration.
              This can be reached when increasing total number of metrics requested and depth
              of history. _

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. If left
              blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this endpoint.

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-estimates/v2/consensus-ratings",
            body=maybe_transform(
                {
                    "ids": ids,
                    "end_date": end_date,
                    "frequency": frequency,
                    "start_date": start_date,
                },
                consensus_rating_create_params.ConsensusRatingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsensusRatingsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusRatingsResponse:
        """
        Returns ratings from the FactSet Estimates database for current and historical
        for an individual security using rolling fiscal dates as of a specific date.

        Args:
          ids: Security or Entity identifiers. FactSet Identifiers, tickers, CUSIP and SEDOL
              are accepted input. <p>**\\**ids limit** = 3000 per request*</p> * Make Note - id
              limit of 3000 for defaults, otherwise the service is limited to a 30 second
              duration. This can be reached when increasing total number of metrics requested
              and depth of history. \\**

          end_date: End date for point in time of estimates expressed in YYYY-MM-DD format.

          frequency: Controls the frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-estimates/v2/consensus-ratings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "end_date": end_date,
                        "frequency": frequency,
                        "start_date": start_date,
                    },
                    consensus_rating_list_params.ConsensusRatingListParams,
                ),
            ),
            cast_to=ConsensusRatingsResponse,
        )


class AsyncConsensusRatingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConsensusRatingsResourceWithRawResponse:
        return AsyncConsensusRatingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsensusRatingsResourceWithStreamingResponse:
        return AsyncConsensusRatingsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusRatingsResponse:
        """
        Returns ratings from the FactSet Estimates database for current and historical
        for an individual security using rolling fiscal dates as of a specific date.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. _ Make Note - id limit
              of 3000 for defaults, otherwise the service is limited to a 30 second duration.
              This can be reached when increasing total number of metrics requested and depth
              of history. _

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. If left
              blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this endpoint.

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-estimates/v2/consensus-ratings",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "end_date": end_date,
                    "frequency": frequency,
                    "start_date": start_date,
                },
                consensus_rating_create_params.ConsensusRatingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsensusRatingsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusRatingsResponse:
        """
        Returns ratings from the FactSet Estimates database for current and historical
        for an individual security using rolling fiscal dates as of a specific date.

        Args:
          ids: Security or Entity identifiers. FactSet Identifiers, tickers, CUSIP and SEDOL
              are accepted input. <p>**\\**ids limit** = 3000 per request*</p> * Make Note - id
              limit of 3000 for defaults, otherwise the service is limited to a 30 second
              duration. This can be reached when increasing total number of metrics requested
              and depth of history. \\**

          end_date: End date for point in time of estimates expressed in YYYY-MM-DD format.

          frequency: Controls the frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-estimates/v2/consensus-ratings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "end_date": end_date,
                        "frequency": frequency,
                        "start_date": start_date,
                    },
                    consensus_rating_list_params.ConsensusRatingListParams,
                ),
            ),
            cast_to=ConsensusRatingsResponse,
        )


class ConsensusRatingsResourceWithRawResponse:
    def __init__(self, consensus_ratings: ConsensusRatingsResource) -> None:
        self._consensus_ratings = consensus_ratings

        self.create = to_raw_response_wrapper(
            consensus_ratings.create,
        )
        self.list = to_raw_response_wrapper(
            consensus_ratings.list,
        )


class AsyncConsensusRatingsResourceWithRawResponse:
    def __init__(self, consensus_ratings: AsyncConsensusRatingsResource) -> None:
        self._consensus_ratings = consensus_ratings

        self.create = async_to_raw_response_wrapper(
            consensus_ratings.create,
        )
        self.list = async_to_raw_response_wrapper(
            consensus_ratings.list,
        )


class ConsensusRatingsResourceWithStreamingResponse:
    def __init__(self, consensus_ratings: ConsensusRatingsResource) -> None:
        self._consensus_ratings = consensus_ratings

        self.create = to_streamed_response_wrapper(
            consensus_ratings.create,
        )
        self.list = to_streamed_response_wrapper(
            consensus_ratings.list,
        )


class AsyncConsensusRatingsResourceWithStreamingResponse:
    def __init__(self, consensus_ratings: AsyncConsensusRatingsResource) -> None:
        self._consensus_ratings = consensus_ratings

        self.create = async_to_streamed_response_wrapper(
            consensus_ratings.create,
        )
        self.list = async_to_streamed_response_wrapper(
            consensus_ratings.list,
        )
