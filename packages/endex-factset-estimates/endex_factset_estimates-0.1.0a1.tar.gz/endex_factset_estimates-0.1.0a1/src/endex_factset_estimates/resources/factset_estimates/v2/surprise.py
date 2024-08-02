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
from ....types.factset_estimates.v2 import surprise_create_params, surprise_retrieve_params
from ....types.factset_estimates.v2.surprise_response import SurpriseResponse

__all__ = ["SurpriseResource", "AsyncSurpriseResource"]


class SurpriseResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SurpriseResourceWithRawResponse:
        return SurpriseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SurpriseResourceWithStreamingResponse:
        return SurpriseResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        statistic: Literal["MEAN", "MEDIAN", "HIGH", "LOW", "COUNT", "STDDEV"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SurpriseResponse:
        """
        Returns FactSet Estimates surprise data using rolling fiscal dates.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. _ Make Note - id limit
              of 3000 for defaults, otherwise the service is limited to a 30 second duration.
              This can be reached when increasing total number of metrics requested and depth
              of history. _

          metrics: Requested metrics. Use the metrics endpoint for a list of estimate items. Note,
              the number of metrics you are allowed to supply is limited to 1 for now. For
              more details, visit
              [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).

          currency: Currency code for adjusting the data. Use input as 'ESTIMATE' for values in
              Estimate currency. For a list of currency ISO codes, visit
              [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).

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

          periodicity: The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
              Estimates.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          statistic: Statistic for consensus calculation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-estimates/v2/surprise",
            body=maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "frequency": frequency,
                    "periodicity": periodicity,
                    "start_date": start_date,
                    "statistic": statistic,
                },
                surprise_create_params.SurpriseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SurpriseResponse,
        )

    def retrieve(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        statistic: Literal["MEAN", "MEDIAN", "HIGH", "LOW", "COUNT", "STDDEV"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SurpriseResponse:
        """
        Returns FactSet Estimates surprise data using rolling fiscal dates.

        Args:
          ids: Security or Entity identifiers. FactSet Identifiers, tickers, CUSIP and SEDOL
              are accepted input. <p>**\\**ids limit** = 3000 per request*</p> * Make Note - id
              limit of 3000 for defaults, otherwise the service is limited to a 30 second
              duration. This can be reached when increasing total number of metrics requested
              and depth of history. \\**

          metrics: Requested metrics. Use the /metrics endpoint to return a list of available
              estimate items. Note, the number of metrics you are allowed to supply is limited
              to 1 for now. **Top 10** most used metrics are **EPS, SALES, DPS, EBITDA,EBIT,
              PRICE_TGT, CFPS, BPS, NET_INC, and ASSETS**. For more details, visit
              [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).

          currency: Currency code for adjusting the data. Use 'ESTIMATE' as input value for the
              values in Estimate Currency. For a list of currency ISO codes, visit
              [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).

          end_date: End date for point in time of estimates expressed in YYYY-MM-DD format.

          frequency: Controls the frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          periodicity: The periodicity for the estimates requested, allowing you to fetch Quarterly,
              Semi-Annual and Annual Estimates.

              - **ANN** - Annual
              - **QTR** - Quarterly
              - **SEMI** - Semi-Annual

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          statistic: Statistic for consensus calculation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-estimates/v2/surprise",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "metrics": metrics,
                        "currency": currency,
                        "end_date": end_date,
                        "frequency": frequency,
                        "periodicity": periodicity,
                        "start_date": start_date,
                        "statistic": statistic,
                    },
                    surprise_retrieve_params.SurpriseRetrieveParams,
                ),
            ),
            cast_to=SurpriseResponse,
        )


class AsyncSurpriseResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSurpriseResourceWithRawResponse:
        return AsyncSurpriseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSurpriseResourceWithStreamingResponse:
        return AsyncSurpriseResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        statistic: Literal["MEAN", "MEDIAN", "HIGH", "LOW", "COUNT", "STDDEV"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SurpriseResponse:
        """
        Returns FactSet Estimates surprise data using rolling fiscal dates.

        Args:
          ids: The requested list of security identifiers. Accepted ID types include Market
              Tickers, SEDOL, ISINs, CUSIPs, or FactSet Permanent Ids. _ Make Note - id limit
              of 3000 for defaults, otherwise the service is limited to a 30 second duration.
              This can be reached when increasing total number of metrics requested and depth
              of history. _

          metrics: Requested metrics. Use the metrics endpoint for a list of estimate items. Note,
              the number of metrics you are allowed to supply is limited to 1 for now. For
              more details, visit
              [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).

          currency: Currency code for adjusting the data. Use input as 'ESTIMATE' for values in
              Estimate currency. For a list of currency ISO codes, visit
              [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).

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

          periodicity: The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
              Estimates.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          statistic: Statistic for consensus calculation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-estimates/v2/surprise",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "frequency": frequency,
                    "periodicity": periodicity,
                    "start_date": start_date,
                    "statistic": statistic,
                },
                surprise_create_params.SurpriseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SurpriseResponse,
        )

    async def retrieve(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        statistic: Literal["MEAN", "MEDIAN", "HIGH", "LOW", "COUNT", "STDDEV"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SurpriseResponse:
        """
        Returns FactSet Estimates surprise data using rolling fiscal dates.

        Args:
          ids: Security or Entity identifiers. FactSet Identifiers, tickers, CUSIP and SEDOL
              are accepted input. <p>**\\**ids limit** = 3000 per request*</p> * Make Note - id
              limit of 3000 for defaults, otherwise the service is limited to a 30 second
              duration. This can be reached when increasing total number of metrics requested
              and depth of history. \\**

          metrics: Requested metrics. Use the /metrics endpoint to return a list of available
              estimate items. Note, the number of metrics you are allowed to supply is limited
              to 1 for now. **Top 10** most used metrics are **EPS, SALES, DPS, EBITDA,EBIT,
              PRICE_TGT, CFPS, BPS, NET_INC, and ASSETS**. For more details, visit
              [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).

          currency: Currency code for adjusting the data. Use 'ESTIMATE' as input value for the
              values in Estimate Currency. For a list of currency ISO codes, visit
              [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).

          end_date: End date for point in time of estimates expressed in YYYY-MM-DD format.

          frequency: Controls the frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          periodicity: The periodicity for the estimates requested, allowing you to fetch Quarterly,
              Semi-Annual and Annual Estimates.

              - **ANN** - Annual
              - **QTR** - Quarterly
              - **SEMI** - Semi-Annual

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          statistic: Statistic for consensus calculation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-estimates/v2/surprise",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "metrics": metrics,
                        "currency": currency,
                        "end_date": end_date,
                        "frequency": frequency,
                        "periodicity": periodicity,
                        "start_date": start_date,
                        "statistic": statistic,
                    },
                    surprise_retrieve_params.SurpriseRetrieveParams,
                ),
            ),
            cast_to=SurpriseResponse,
        )


class SurpriseResourceWithRawResponse:
    def __init__(self, surprise: SurpriseResource) -> None:
        self._surprise = surprise

        self.create = to_raw_response_wrapper(
            surprise.create,
        )
        self.retrieve = to_raw_response_wrapper(
            surprise.retrieve,
        )


class AsyncSurpriseResourceWithRawResponse:
    def __init__(self, surprise: AsyncSurpriseResource) -> None:
        self._surprise = surprise

        self.create = async_to_raw_response_wrapper(
            surprise.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            surprise.retrieve,
        )


class SurpriseResourceWithStreamingResponse:
    def __init__(self, surprise: SurpriseResource) -> None:
        self._surprise = surprise

        self.create = to_streamed_response_wrapper(
            surprise.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            surprise.retrieve,
        )


class AsyncSurpriseResourceWithStreamingResponse:
    def __init__(self, surprise: AsyncSurpriseResource) -> None:
        self._surprise = surprise

        self.create = async_to_streamed_response_wrapper(
            surprise.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            surprise.retrieve,
        )
