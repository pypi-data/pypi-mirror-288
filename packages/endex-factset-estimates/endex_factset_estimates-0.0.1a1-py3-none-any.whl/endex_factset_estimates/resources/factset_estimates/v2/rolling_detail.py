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
from ....types.factset_estimates.v2 import rolling_detail_list_params, rolling_detail_create_params
from ....types.shared.detail_response import DetailResponse

__all__ = ["RollingDetailResource", "AsyncRollingDetailResource"]


class RollingDetailResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RollingDetailResourceWithRawResponse:
        return RollingDetailResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RollingDetailResourceWithStreamingResponse:
        return RollingDetailResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailResponse:
        """
        Updated intraday, the FactSet detail estimates apis provide individual
        broker-level estimates collected from over 800 sell-side analysts. This database
        contains 20+ years of broker history across more than 59,000 global companies.
        Content is provided for "rolling" fiscal periods.

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

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          periodicity: The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
              Estimates.

          relative_fiscal_end: Relative fiscal period, expressed as an integer, used to filter results.

          relative_fiscal_start: Relative fiscal period, expressed as an integer, used to filter results.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-estimates/v2/rolling-detail",
            body=maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "frequency": frequency,
                    "include_all": include_all,
                    "periodicity": periodicity,
                    "relative_fiscal_end": relative_fiscal_end,
                    "relative_fiscal_start": relative_fiscal_start,
                    "start_date": start_date,
                },
                rolling_detail_create_params.RollingDetailCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DetailResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailResponse:
        """
        Updated intraday, the FactSet detail estimates apis provide individual
        broker-level estimates collected from over 800 sell-side analysts. This database
        contains 20+ years of broker history across more than 59,000 global companies.
        Content is provided for "rolling" fiscal periods.

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

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          periodicity: The periodicity for the estimates requested, allowing you to fetch Quarterly,
              Semi-Annual, and Annual Estimates.

              - **ANN** - Annual
              - **QTR** - Quarterly
              - **SEMI** - Semi-Annual

          relative_fiscal_end: Relative fiscal period, expressed as an integer, used to filter results. This is
              combined with the periodicity parameter to specify a relative estimate period.
              For example, set to 2 and periodicity to ANN to ask for relative Fiscal Year 1
              (FY2).

          relative_fiscal_start: Relative fiscal period, expressed as an integer, used to filter results. This is
              combined with the periodicity parameter to specify a relative estimate period.
              For example, set to 1 and periodicity to ANN to ask for relative Fiscal Year 1
              (FY1).

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-estimates/v2/rolling-detail",
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
                        "include_all": include_all,
                        "periodicity": periodicity,
                        "relative_fiscal_end": relative_fiscal_end,
                        "relative_fiscal_start": relative_fiscal_start,
                        "start_date": start_date,
                    },
                    rolling_detail_list_params.RollingDetailListParams,
                ),
            ),
            cast_to=DetailResponse,
        )


class AsyncRollingDetailResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRollingDetailResourceWithRawResponse:
        return AsyncRollingDetailResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRollingDetailResourceWithStreamingResponse:
        return AsyncRollingDetailResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailResponse:
        """
        Updated intraday, the FactSet detail estimates apis provide individual
        broker-level estimates collected from over 800 sell-side analysts. This database
        contains 20+ years of broker history across more than 59,000 global companies.
        Content is provided for "rolling" fiscal periods.

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

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          periodicity: The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
              Estimates.

          relative_fiscal_end: Relative fiscal period, expressed as an integer, used to filter results.

          relative_fiscal_start: Relative fiscal period, expressed as an integer, used to filter results.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-estimates/v2/rolling-detail",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "frequency": frequency,
                    "include_all": include_all,
                    "periodicity": periodicity,
                    "relative_fiscal_end": relative_fiscal_end,
                    "relative_fiscal_start": relative_fiscal_start,
                    "start_date": start_date,
                },
                rolling_detail_create_params.RollingDetailCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DetailResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        include_all: bool | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailResponse:
        """
        Updated intraday, the FactSet detail estimates apis provide individual
        broker-level estimates collected from over 800 sell-side analysts. This database
        contains 20+ years of broker history across more than 59,000 global companies.
        Content is provided for "rolling" fiscal periods.

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

          include_all: Include All filter is used to identify included and excluded broker details from
              the consensus By default the service would return only the brokers included in
              the consensus-

              - **TRUE** = Returns all the brokers included and excluded in the consensus
              - **FALSE** = Returns only the broker details included in the consensus

          periodicity: The periodicity for the estimates requested, allowing you to fetch Quarterly,
              Semi-Annual, and Annual Estimates.

              - **ANN** - Annual
              - **QTR** - Quarterly
              - **SEMI** - Semi-Annual

          relative_fiscal_end: Relative fiscal period, expressed as an integer, used to filter results. This is
              combined with the periodicity parameter to specify a relative estimate period.
              For example, set to 2 and periodicity to ANN to ask for relative Fiscal Year 1
              (FY2).

          relative_fiscal_start: Relative fiscal period, expressed as an integer, used to filter results. This is
              combined with the periodicity parameter to specify a relative estimate period.
              For example, set to 1 and periodicity to ANN to ask for relative Fiscal Year 1
              (FY1).

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-estimates/v2/rolling-detail",
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
                        "include_all": include_all,
                        "periodicity": periodicity,
                        "relative_fiscal_end": relative_fiscal_end,
                        "relative_fiscal_start": relative_fiscal_start,
                        "start_date": start_date,
                    },
                    rolling_detail_list_params.RollingDetailListParams,
                ),
            ),
            cast_to=DetailResponse,
        )


class RollingDetailResourceWithRawResponse:
    def __init__(self, rolling_detail: RollingDetailResource) -> None:
        self._rolling_detail = rolling_detail

        self.create = to_raw_response_wrapper(
            rolling_detail.create,
        )
        self.list = to_raw_response_wrapper(
            rolling_detail.list,
        )


class AsyncRollingDetailResourceWithRawResponse:
    def __init__(self, rolling_detail: AsyncRollingDetailResource) -> None:
        self._rolling_detail = rolling_detail

        self.create = async_to_raw_response_wrapper(
            rolling_detail.create,
        )
        self.list = async_to_raw_response_wrapper(
            rolling_detail.list,
        )


class RollingDetailResourceWithStreamingResponse:
    def __init__(self, rolling_detail: RollingDetailResource) -> None:
        self._rolling_detail = rolling_detail

        self.create = to_streamed_response_wrapper(
            rolling_detail.create,
        )
        self.list = to_streamed_response_wrapper(
            rolling_detail.list,
        )


class AsyncRollingDetailResourceWithStreamingResponse:
    def __init__(self, rolling_detail: AsyncRollingDetailResource) -> None:
        self._rolling_detail = rolling_detail

        self.create = async_to_streamed_response_wrapper(
            rolling_detail.create,
        )
        self.list = async_to_streamed_response_wrapper(
            rolling_detail.list,
        )
