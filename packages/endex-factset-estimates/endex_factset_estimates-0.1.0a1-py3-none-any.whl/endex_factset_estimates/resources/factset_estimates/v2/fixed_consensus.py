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
from ....types.factset_estimates.v2 import fixed_consensus_create_params, fixed_consensus_retrieve_params
from ....types.shared.consensus_response import ConsensusResponse

__all__ = ["FixedConsensusResource", "AsyncFixedConsensusResource"]


class FixedConsensusResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FixedConsensusResourceWithRawResponse:
        return FixedConsensusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FixedConsensusResourceWithStreamingResponse:
        return FixedConsensusResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "LTMA", "NTMA"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using fixed fiscal dates.

        For example,
        if the company's current unreported year is 12/2020, all data returned by
        formulas that specify as the period/report basis will be for 12/2005 regardless
        of what perspective dates (startDate/endDate) are used. The fixed dates are
        "locked" in time and all estimated values are for that explicit date. If you are
        requesting that the estimated periods can change with the perspective date,
        please use the rolling-consensus endpoint.

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

          fiscal_period_end: Fiscal period end expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Month-end** - MM/YYYY (e.g., 11/2019)
              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Semiannual Period-end** - YYYY/FSA (e.g., 2019/1S, 2019/2S)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          fiscal_period_start: Fiscal period start expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Semiannual Period-end** - YYYY/FSA (e.g., 2019/1S, 2019/2S)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          periodicity: The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
              Estimates. Next-twelve-months (NTMA) and Last-twelve-months (LTMA) also
              supported.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-estimates/v2/fixed-consensus",
            body=maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "fiscal_period_end": fiscal_period_end,
                    "fiscal_period_start": fiscal_period_start,
                    "frequency": frequency,
                    "periodicity": periodicity,
                    "start_date": start_date,
                },
                fixed_consensus_create_params.FixedConsensusCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsensusResponse,
        )

    def retrieve(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "NTMA", "LTMA"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using fixed fiscal dates.

        For example,
        if the company's current unreported year is 12/2020, all data returned by
        formulas that specify as the period/report basis will be for 12/2005 regardless
        of what perspective dates (startDate/endDate) are used. The fixed dates are
        "locked" in time and all estimated values are for that explicit date. If you are
        requesting that the estimated periods can change with the perspective date,
        please use the rolling-consensus endpoint.

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

          fiscal_period_end: Fiscal period start expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          fiscal_period_start: Fiscal period start expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          frequency: Controls the frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          periodicity: The periodicity for the estimates requested, allowing you to fetch Quarterly,
              Semi-Annual, Annual, and NTMA/LTMA Estimates.

              - **ANN** - Annual
              - **QTR** - Quarterly
              - **SEMI** - Semi-Annual
              - **NTMA** - Next-Twelve-Months - Time-weighted Annual. Estimates use a
                percentage of annual estimates from two fiscal years to create an estimate
                based on the 12-month period. Visit
                [OA 16614](https://my.apps.factset.com/oa/pages/16614) for detail.
              - **LTMA** - Last-Twelve-Months - Time-weighted Annual. Estimates use a
                percentage of annual estimates from two fiscal years to create an estimate
                based on the 12-month period. Visit
                [OA 16614](https://my.apps.factset.com/oa/pages/16614) for detail.

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-estimates/v2/fixed-consensus",
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
                        "fiscal_period_end": fiscal_period_end,
                        "fiscal_period_start": fiscal_period_start,
                        "frequency": frequency,
                        "periodicity": periodicity,
                        "start_date": start_date,
                    },
                    fixed_consensus_retrieve_params.FixedConsensusRetrieveParams,
                ),
            ),
            cast_to=ConsensusResponse,
        )


class AsyncFixedConsensusResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFixedConsensusResourceWithRawResponse:
        return AsyncFixedConsensusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFixedConsensusResourceWithStreamingResponse:
        return AsyncFixedConsensusResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "LTMA", "NTMA"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using fixed fiscal dates.

        For example,
        if the company's current unreported year is 12/2020, all data returned by
        formulas that specify as the period/report basis will be for 12/2005 regardless
        of what perspective dates (startDate/endDate) are used. The fixed dates are
        "locked" in time and all estimated values are for that explicit date. If you are
        requesting that the estimated periods can change with the perspective date,
        please use the rolling-consensus endpoint.

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

          fiscal_period_end: Fiscal period end expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Month-end** - MM/YYYY (e.g., 11/2019)
              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Semiannual Period-end** - YYYY/FSA (e.g., 2019/1S, 2019/2S)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          fiscal_period_start: Fiscal period start expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Semiannual Period-end** - YYYY/FSA (e.g., 2019/1S, 2019/2S)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          frequency: Controls the display frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          periodicity: The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
              Estimates. Next-twelve-months (NTMA) and Last-twelve-months (LTMA) also
              supported.

          start_date: The start date requested for a given date range in **YYYY-MM-DD** format. If
              left blank, the API will default to previous close. Future dates (T+1) are not
              accepted in this #endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-estimates/v2/fixed-consensus",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "fiscal_period_end": fiscal_period_end,
                    "fiscal_period_start": fiscal_period_start,
                    "frequency": frequency,
                    "periodicity": periodicity,
                    "start_date": start_date,
                },
                fixed_consensus_create_params.FixedConsensusCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsensusResponse,
        )

    async def retrieve(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        fiscal_period_end: str | NotGiven = NOT_GIVEN,
        fiscal_period_start: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "NTMA", "LTMA"] | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using fixed fiscal dates.

        For example,
        if the company's current unreported year is 12/2020, all data returned by
        formulas that specify as the period/report basis will be for 12/2005 regardless
        of what perspective dates (startDate/endDate) are used. The fixed dates are
        "locked" in time and all estimated values are for that explicit date. If you are
        requesting that the estimated periods can change with the perspective date,
        please use the rolling-consensus endpoint.

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

          fiscal_period_end: Fiscal period start expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          fiscal_period_start: Fiscal period start expressed in absolute date formats. Date that will fall back
              to most recent completed period during resolution.

              - **Fiscal Quarter-end** - YYYY/FQ (e.g., 2019/1F, 2019/2F, 2019/3F, 2019/4F)
              - **Fiscal Year-end** - YYYY (e.g. 2019)

          frequency: Controls the frequency of the data returned.

              - **D** = Daily
              - **W** = Weekly, based on the last day of the week of the start date.
              - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
                data is displayed for June 16, May 16, April 16 etc.).
              - **AQ** = Quarterly, based on the start date.
              - **AY** = Actual Annual, based on the start date.

          periodicity: The periodicity for the estimates requested, allowing you to fetch Quarterly,
              Semi-Annual, Annual, and NTMA/LTMA Estimates.

              - **ANN** - Annual
              - **QTR** - Quarterly
              - **SEMI** - Semi-Annual
              - **NTMA** - Next-Twelve-Months - Time-weighted Annual. Estimates use a
                percentage of annual estimates from two fiscal years to create an estimate
                based on the 12-month period. Visit
                [OA 16614](https://my.apps.factset.com/oa/pages/16614) for detail.
              - **LTMA** - Last-Twelve-Months - Time-weighted Annual. Estimates use a
                percentage of annual estimates from two fiscal years to create an estimate
                based on the 12-month period. Visit
                [OA 16614](https://my.apps.factset.com/oa/pages/16614) for detail.

          start_date: Start date for point in time of estimates expressed in YYYY-MM-DD format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-estimates/v2/fixed-consensus",
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
                        "fiscal_period_end": fiscal_period_end,
                        "fiscal_period_start": fiscal_period_start,
                        "frequency": frequency,
                        "periodicity": periodicity,
                        "start_date": start_date,
                    },
                    fixed_consensus_retrieve_params.FixedConsensusRetrieveParams,
                ),
            ),
            cast_to=ConsensusResponse,
        )


class FixedConsensusResourceWithRawResponse:
    def __init__(self, fixed_consensus: FixedConsensusResource) -> None:
        self._fixed_consensus = fixed_consensus

        self.create = to_raw_response_wrapper(
            fixed_consensus.create,
        )
        self.retrieve = to_raw_response_wrapper(
            fixed_consensus.retrieve,
        )


class AsyncFixedConsensusResourceWithRawResponse:
    def __init__(self, fixed_consensus: AsyncFixedConsensusResource) -> None:
        self._fixed_consensus = fixed_consensus

        self.create = async_to_raw_response_wrapper(
            fixed_consensus.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            fixed_consensus.retrieve,
        )


class FixedConsensusResourceWithStreamingResponse:
    def __init__(self, fixed_consensus: FixedConsensusResource) -> None:
        self._fixed_consensus = fixed_consensus

        self.create = to_streamed_response_wrapper(
            fixed_consensus.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            fixed_consensus.retrieve,
        )


class AsyncFixedConsensusResourceWithStreamingResponse:
    def __init__(self, fixed_consensus: AsyncFixedConsensusResource) -> None:
        self._fixed_consensus = fixed_consensus

        self.create = async_to_streamed_response_wrapper(
            fixed_consensus.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            fixed_consensus.retrieve,
        )
