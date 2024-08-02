# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

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
from ....types.factset_estimates.v2 import detail_rating_create_params, detail_rating_retrieve_params
from ....types.factset_estimates.v2.detail_ratings_response import DetailRatingsResponse

__all__ = ["DetailRatingsResource", "AsyncDetailRatingsResource"]


class DetailRatingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DetailRatingsResourceWithRawResponse:
        return DetailRatingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DetailRatingsResourceWithStreamingResponse:
        return DetailRatingsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailRatingsResponse:
        """Retrieves the Broker Level ratings for the requested Id and date range.

        Ratings
        include Buy, Hold, Sell, Overweight, and Underweight.

        <p>The `startDate` and `endDate` parameters controls the range of perspective dates. By default, the service will return the range of estimateDates within the latest company's reporting period. As you expand the date range, additional full historical reporting periods and all ratings estimateDates per broker will be returned.</p>

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. _ Make Note - id limit
              of 3000 for defaults, otherwise the service is limited to a 30 second duration.
              This can be reached when increasing total number of metrics requested and depth
              of history. _

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. If left
              blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this endpoint.

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-estimates/v2/detail-ratings",
            body=maybe_transform(
                {
                    "ids": ids,
                    "end_date": end_date,
                    "include_all": include_all,
                    "start_date": start_date,
                },
                detail_rating_create_params.DetailRatingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DetailRatingsResponse,
        )

    def retrieve(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailRatingsResponse:
        """Retrieves the Broker Level ratings for the requested Id and date range.

        Ratings
        include Buy, Hold, Sell, Overweight, and Underweight.

        <p>The `startDate` and `endDate` parameters controls the range of perspective dates. By default, the service will return the range of estimateDates within the latest company's reporting period. As you expand the date range, additional full historical reporting periods and all ratings estimateDates per broker will be returned.</p>

        Args:
          ids: Security or Entity identifiers. FactSet Identifiers, tickers, CUSIP and SEDOL
              are accepted input. <p>**\\**ids limit** = 3000 per request*</p> * Make Note - id
              limit of 3000 for defaults, otherwise the service is limited to a 30 second
              duration. This can be reached when increasing total number of metrics requested
              and depth of history. \\**

          end_date: End date for point in time of estimates expressed in YYYY-MM-DD format.

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-estimates/v2/detail-ratings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "end_date": end_date,
                        "include_all": include_all,
                        "start_date": start_date,
                    },
                    detail_rating_retrieve_params.DetailRatingRetrieveParams,
                ),
            ),
            cast_to=DetailRatingsResponse,
        )


class AsyncDetailRatingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDetailRatingsResourceWithRawResponse:
        return AsyncDetailRatingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDetailRatingsResourceWithStreamingResponse:
        return AsyncDetailRatingsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailRatingsResponse:
        """Retrieves the Broker Level ratings for the requested Id and date range.

        Ratings
        include Buy, Hold, Sell, Overweight, and Underweight.

        <p>The `startDate` and `endDate` parameters controls the range of perspective dates. By default, the service will return the range of estimateDates within the latest company's reporting period. As you expand the date range, additional full historical reporting periods and all ratings estimateDates per broker will be returned.</p>

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. _ Make Note - id limit
              of 3000 for defaults, otherwise the service is limited to a 30 second duration.
              This can be reached when increasing total number of metrics requested and depth
              of history. _

          end_date: The end date requested for a given date range in **YYYY-MM-DD** format. If left
              blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this endpoint.

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-estimates/v2/detail-ratings",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "end_date": end_date,
                    "include_all": include_all,
                    "start_date": start_date,
                },
                detail_rating_create_params.DetailRatingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DetailRatingsResponse,
        )

    async def retrieve(
        self,
        *,
        ids: List[str],
        end_date: str | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailRatingsResponse:
        """Retrieves the Broker Level ratings for the requested Id and date range.

        Ratings
        include Buy, Hold, Sell, Overweight, and Underweight.

        <p>The `startDate` and `endDate` parameters controls the range of perspective dates. By default, the service will return the range of estimateDates within the latest company's reporting period. As you expand the date range, additional full historical reporting periods and all ratings estimateDates per broker will be returned.</p>

        Args:
          ids: Security or Entity identifiers. FactSet Identifiers, tickers, CUSIP and SEDOL
              are accepted input. <p>**\\**ids limit** = 3000 per request*</p> * Make Note - id
              limit of 3000 for defaults, otherwise the service is limited to a 30 second
              duration. This can be reached when increasing total number of metrics requested
              and depth of history. \\**

          end_date: End date for point in time of estimates expressed in YYYY-MM-DD format.

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-estimates/v2/detail-ratings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "end_date": end_date,
                        "include_all": include_all,
                        "start_date": start_date,
                    },
                    detail_rating_retrieve_params.DetailRatingRetrieveParams,
                ),
            ),
            cast_to=DetailRatingsResponse,
        )


class DetailRatingsResourceWithRawResponse:
    def __init__(self, detail_ratings: DetailRatingsResource) -> None:
        self._detail_ratings = detail_ratings

        self.create = to_raw_response_wrapper(
            detail_ratings.create,
        )
        self.retrieve = to_raw_response_wrapper(
            detail_ratings.retrieve,
        )


class AsyncDetailRatingsResourceWithRawResponse:
    def __init__(self, detail_ratings: AsyncDetailRatingsResource) -> None:
        self._detail_ratings = detail_ratings

        self.create = async_to_raw_response_wrapper(
            detail_ratings.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            detail_ratings.retrieve,
        )


class DetailRatingsResourceWithStreamingResponse:
    def __init__(self, detail_ratings: DetailRatingsResource) -> None:
        self._detail_ratings = detail_ratings

        self.create = to_streamed_response_wrapper(
            detail_ratings.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            detail_ratings.retrieve,
        )


class AsyncDetailRatingsResourceWithStreamingResponse:
    def __init__(self, detail_ratings: AsyncDetailRatingsResource) -> None:
        self._detail_ratings = detail_ratings

        self.create = async_to_streamed_response_wrapper(
            detail_ratings.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            detail_ratings.retrieve,
        )
