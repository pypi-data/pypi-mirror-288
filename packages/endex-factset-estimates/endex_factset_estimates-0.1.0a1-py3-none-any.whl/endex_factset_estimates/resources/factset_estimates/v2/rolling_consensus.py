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
from ....types.factset_estimates.v2 import rolling_consensus_list_params, rolling_consensus_create_params
from ....types.shared.consensus_response import ConsensusResponse

__all__ = ["RollingConsensusResource", "AsyncRollingConsensusResource"]


class RollingConsensusResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RollingConsensusResourceWithRawResponse:
        return RollingConsensusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RollingConsensusResourceWithStreamingResponse:
        return RollingConsensusResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "LTMA", "NTMA"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using rolling fiscal dates.

        <p>The
        rolling behavior causes fiscal year to automatically roll from one year to the
        next as the historical perspective date changes. The fiscal period rolls forward
        as of each period end. This endpoint is optimized to allow the request to simply
        include a relative fiscal period (e.g. use relativeFiscalStart integer 1 and
        periodicity ANN for next unreported fiscal year end), and then see what the
        consensus thought the "next fiscal year" estimates were through time as you
        "roll" back your perspective dates. This differs from locking down an absolute
        estimate period such as explicitly stating Fiscal Year 2019. This can be done in
        the fixed-consensus endpoint.</p>

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
              Estimates. Next-twelve-months (NTMA) and Last-twelve-months (LTMA) also
              supported.

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
            "/factset-estimates/v2/rolling-consensus",
            body=maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "frequency": frequency,
                    "periodicity": periodicity,
                    "relative_fiscal_end": relative_fiscal_end,
                    "relative_fiscal_start": relative_fiscal_start,
                    "start_date": start_date,
                },
                rolling_consensus_create_params.RollingConsensusCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsensusResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "NTMA", "LTMA"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using rolling fiscal dates.

        <p>The
        rolling behavior causes fiscal year to automatically roll from one year to the
        next as the historical perspective date changes. The fiscal period rolls forward
        as of each period end. This endpoint is optimized to allow the request to simply
        include a relative fiscal period (e.g. use relativeFiscalStart integer 1 and
        periodicity ANN for next unreported fiscal year end), and then see what the
        consensus thought the "next fiscal year" estimates were through time as you
        "roll" back your perspective dates. This differs from locking down an absolute
        estimate period such as explicitly stating Fiscal Year 2019. This can be done in
        the fixed-consensus endpoint.</p>

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
            "/factset-estimates/v2/rolling-consensus",
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
                        "relative_fiscal_end": relative_fiscal_end,
                        "relative_fiscal_start": relative_fiscal_start,
                        "start_date": start_date,
                    },
                    rolling_consensus_list_params.RollingConsensusListParams,
                ),
            ),
            cast_to=ConsensusResponse,
        )


class AsyncRollingConsensusResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRollingConsensusResourceWithRawResponse:
        return AsyncRollingConsensusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRollingConsensusResourceWithStreamingResponse:
        return AsyncRollingConsensusResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "LTMA", "NTMA"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using rolling fiscal dates.

        <p>The
        rolling behavior causes fiscal year to automatically roll from one year to the
        next as the historical perspective date changes. The fiscal period rolls forward
        as of each period end. This endpoint is optimized to allow the request to simply
        include a relative fiscal period (e.g. use relativeFiscalStart integer 1 and
        periodicity ANN for next unreported fiscal year end), and then see what the
        consensus thought the "next fiscal year" estimates were through time as you
        "roll" back your perspective dates. This differs from locking down an absolute
        estimate period such as explicitly stating Fiscal Year 2019. This can be done in
        the fixed-consensus endpoint.</p>

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
              Estimates. Next-twelve-months (NTMA) and Last-twelve-months (LTMA) also
              supported.

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
            "/factset-estimates/v2/rolling-consensus",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "metrics": metrics,
                    "currency": currency,
                    "end_date": end_date,
                    "frequency": frequency,
                    "periodicity": periodicity,
                    "relative_fiscal_end": relative_fiscal_end,
                    "relative_fiscal_start": relative_fiscal_start,
                    "start_date": start_date,
                },
                rolling_consensus_create_params.RollingConsensusCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsensusResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        metrics: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        end_date: str | NotGiven = NOT_GIVEN,
        frequency: Literal["D", "W", "AM", "AQ", "AY"] | NotGiven = NOT_GIVEN,
        periodicity: Literal["ANN", "QTR", "SEMI", "NTMA", "LTMA"] | NotGiven = NOT_GIVEN,
        relative_fiscal_end: int | NotGiven = NOT_GIVEN,
        relative_fiscal_start: int | NotGiven = NOT_GIVEN,
        start_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsensusResponse:
        """Returns FactSet Estimates consensus data using rolling fiscal dates.

        <p>The
        rolling behavior causes fiscal year to automatically roll from one year to the
        next as the historical perspective date changes. The fiscal period rolls forward
        as of each period end. This endpoint is optimized to allow the request to simply
        include a relative fiscal period (e.g. use relativeFiscalStart integer 1 and
        periodicity ANN for next unreported fiscal year end), and then see what the
        consensus thought the "next fiscal year" estimates were through time as you
        "roll" back your perspective dates. This differs from locking down an absolute
        estimate period such as explicitly stating Fiscal Year 2019. This can be done in
        the fixed-consensus endpoint.</p>

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
            "/factset-estimates/v2/rolling-consensus",
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
                        "relative_fiscal_end": relative_fiscal_end,
                        "relative_fiscal_start": relative_fiscal_start,
                        "start_date": start_date,
                    },
                    rolling_consensus_list_params.RollingConsensusListParams,
                ),
            ),
            cast_to=ConsensusResponse,
        )


class RollingConsensusResourceWithRawResponse:
    def __init__(self, rolling_consensus: RollingConsensusResource) -> None:
        self._rolling_consensus = rolling_consensus

        self.create = to_raw_response_wrapper(
            rolling_consensus.create,
        )
        self.list = to_raw_response_wrapper(
            rolling_consensus.list,
        )


class AsyncRollingConsensusResourceWithRawResponse:
    def __init__(self, rolling_consensus: AsyncRollingConsensusResource) -> None:
        self._rolling_consensus = rolling_consensus

        self.create = async_to_raw_response_wrapper(
            rolling_consensus.create,
        )
        self.list = async_to_raw_response_wrapper(
            rolling_consensus.list,
        )


class RollingConsensusResourceWithStreamingResponse:
    def __init__(self, rolling_consensus: RollingConsensusResource) -> None:
        self._rolling_consensus = rolling_consensus

        self.create = to_streamed_response_wrapper(
            rolling_consensus.create,
        )
        self.list = to_streamed_response_wrapper(
            rolling_consensus.list,
        )


class AsyncRollingConsensusResourceWithStreamingResponse:
    def __init__(self, rolling_consensus: AsyncRollingConsensusResource) -> None:
        self._rolling_consensus = rolling_consensus

        self.create = async_to_streamed_response_wrapper(
            rolling_consensus.create,
        )
        self.list = async_to_streamed_response_wrapper(
            rolling_consensus.list,
        )
