# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ....types.factset_estimates.v2 import metric_list_params, metric_create_params
from ....types.factset_estimates.v2.metrics_response import MetricsResponse

__all__ = ["MetricsResource", "AsyncMetricsResource"]


class MetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        category: Literal["FINANCIAL_STATEMENT", "INDUSTRY_METRIC", "OTHER"] | NotGiven = NOT_GIVEN,
        subcategory: Literal[
            "AIRLINES",
            "BALANCE_SHEET",
            "BANKS",
            "CASH_FLOW",
            "COMMODITIES",
            "COMPUTER_HARDWARE",
            "CONSUMER_SERVICES",
            "EDUCATION",
            "FINANCIAL_SERVICE_PROVIDER",
            "HOME_BUILDERS",
            "HOSPITALS",
            "HOTELS",
            "INCOME_STATEMENT",
            "INSURANCE",
            "MARIJUANA",
            "MINING",
            "MISCELLANEOUS",
            "MULTIFINANCIAL",
            "OIL_AND_GAS",
            "OTHER",
            "REITS",
            "RESTAURANTS",
            "RETAILERS",
            "TELECOMMUNICATIONS",
            "TRANSPORTATION",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricsResponse:
        """
        Returns list of available Estimate metrics that can be used in the `metrics`
        parameter of related endpoints. **By default, Factset provides Estimated items
        in millions. For specific metric methodology definitions, reference the `OAurl`
        response items to launch the available methodology page.**

        Args:
          category: Filters the list of Estimate metrics by major category -

              - **FINANCIAL_STATEMENT** = Includes Balance Sheet, Cash Flow, and Income
                Statement.
              - **INDUSTRY_METRICS** = Industry specific metrics.
              - **OTHER** = Target Price

          subcategory: Sub-Category Filter for the Primary Category Requested. Choose a related
              sub-category for the Category requested. For methodology, visit
              [OA 16038](https://my.apps.factset.com/oa/pages/16038) <p>Financial Statement -

              - **BALANCE_SHEET** - Balance Sheet line items, such as Assets, Long-term Debt,
                and more.
              - **CASH_FLOW** - Cash Flow Statement line items, such as Free Cash Flow and
                Share Repurchases
              - **INCOME_STATEMENT** - Income Statement line items, such as EPS, Sales, DPS,
                and more.
              - **MISCELLANEOUS** - EPS Long Term Growth
              </p> <p> Industry Metrics -

              - **AIRLINES** - Including items such as Revenue Passenger, Total Revenue per
                ASK, Available Seats, and more.
              - **BANKS** - Including items such as Net Interest Income, Trading Income, Net
                Loans, and more. SUPPLEMENTAL
              - **COMMODITIES** - Including items such as Average Target Price.
              - **COMPUTER_HARDWARE** - Including items such as Total Addressable Market.
              - **CONSUMER_SERVICES** - Including items such as Gross Merchandise Volume
              - **EDUCATION** - Including Items such as Total Student Enrollment
              - **FINANCIAL_SERVICE_PROVIDER** - Including items such as Annual Subscription
                Value
              - **HOME_BUILDERS** - Including items such as Home Sales, Land Sales,
                Cancellation Rates, and more.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **MARIJUANA** - Including items such as Cost per Gram and Kg of Cannabis Sold.
              - **MINING** - Including items such as Realized Price and Total Production
              - **MULTIFINANCIAL** - Including items such as AUM, Net Flows, and Fee Related
                Earnings.
              - **OIL_AND_GAS** - Including items such as Downstream Income, Production per
                Day, and Exploration Expense.
              - **OTHER** - Target Price
              - **REITS** - Including items such as Funds from Operations, Implied Cap Rate,
                and LTV.
              - **RESTAURANTS** - Including items such as Restaurant Margin.
              - **RETAILERS** - Including items such as Stores Information, Selling Space and
                Net sales per square foot.
              - **TELECOMMUNICATIONS** - Including items such as Gross Adds, Monthly Revenue
                Per User, Churn, and more.
              - **TRANSPORTATION** - Including items such as Revenue Per Unit, Volume Growth,
                and Operating Ratio.</p>

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-estimates/v2/metrics",
            body=maybe_transform(
                {
                    "category": category,
                    "subcategory": subcategory,
                },
                metric_create_params.MetricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricsResponse,
        )

    def list(
        self,
        *,
        category: Literal["FINANCIAL_STATEMENT", "INDUSTRY_METRIC", "OTHER"] | NotGiven = NOT_GIVEN,
        subcategory: Literal[
            "AIRLINES",
            "BALANCE_SHEET",
            "BANKS",
            "CASH_FLOW",
            "COMMODITIES",
            "COMPUTER_HARDWARE",
            "CONSUMER_SERVICES",
            "EDUCATION",
            "FINANCIAL_SERVICE_PROVIDER",
            "HOME_BUILDERS",
            "HOSPITALS",
            "HOTELS",
            "INCOME_STATEMENT",
            "INSURANCE",
            "MARIJUANA",
            "MINING",
            "MISCELLANEOUS",
            "MULTIFINANCIAL",
            "OIL_AND_GAS",
            "OTHER",
            "REITS",
            "RESTAURANTS",
            "RETAILERS",
            "TELECOMMUNICATIONS",
            "TRANSPORTATION",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricsResponse:
        """
        Returns list of available Estimate metrics that can be used in the `metrics`
        parameter of related endpoints. **By default, Factset provides Estimated items
        in millions. For specific metric methodology definitions, reference the `OAurl`
        response items to launch the available methodology page.**

        Args:
          category: Filters the list of Estimate metrics by major category -

              - **FINANCIAL_STATEMENT** = Includes Balance Sheet, Cash Flow, and Income
                Statement.
              - **INDUSTRY_METRICS** = Industry specific metrics.
              - **OTHER** = Target Price

          subcategory: Sub-Category Filter for the Primary Category Requested. Choose a related
              sub-category for the Category requested. For methodology, visit
              [OA 16038](https://my.apps.factset.com/oa/pages/16038) <p>Financial Statement -

              - **BALANCE_SHEET** - Balance Sheet line items, such as Assets, Long-term Debt,
                and more.
              - **CASH_FLOW** - Cash Flow Statement line items, such as Free Cash Flow and
                Share Repurchases
              - **INCOME_STATEMENT** - Income Statement line items, such as EPS, Sales, DPS,
                and more.
              - **MISCELLANEOUS** - EPS Long Term Growth
              </p> <p> Industry Metrics -

              - **AIRLINES** - Including items such as Revenue Passenger, Total Revenue per
                ASK, Available Seats, and more.
              - **BANKS** - Including items such as Net Interest Income, Trading Income, Net
                Loans, and more. SUPPLEMENTAL
              - **COMMODITIES** - Including items such as Average Target Price.
              - **COMPUTER_HARDWARE** - Including items such as Total Addressable Market.
              - **CONSUMER_SERVICES** - Including items such as Gross Merchandise Volume
              - **EDUCATION** - Including Items such as Total Student Enrollment
              - **FINANCIAL_SERVICE_PROVIDER** - Including items such as Annual Subscription
                Value
              - **HOME_BUILDERS** - Including items such as Home Sales, Land Sales,
                Cancellation Rates, and more.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **MARIJUANA** - Including items such as Cost per Gram and Kg of Cannabis Sold.
              - **MINING** - Including items such as Realized Price and Total Production
              - **MULTIFINANCIAL** - Including items such as AUM, Net Flows, and Fee Related
                Earnings.
              - **OIL_AND_GAS** - Including items such as Downstream Income, Production per
                Day, and Exploration Expense.
              - **OTHER** - Target Price
              - **REITS** - Including items such as Funds from Operations, Implied Cap Rate,
                and LTV.
              - **RESTAURANTS** - Including items such as Restaurant Margin.
              - **RETAILERS** - Including items such as Stores Information, Selling Space and
                Net sales per square foot.
              - **TELECOMMUNICATIONS** - Including items such as Gross Adds, Monthly Revenue
                Per User, Churn, and more.
              - **TRANSPORTATION** - Including items such as Revenue Per Unit, Volume Growth,
                and Operating Ratio.</p>

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-estimates/v2/metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category": category,
                        "subcategory": subcategory,
                    },
                    metric_list_params.MetricListParams,
                ),
            ),
            cast_to=MetricsResponse,
        )


class AsyncMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        category: Literal["FINANCIAL_STATEMENT", "INDUSTRY_METRIC", "OTHER"] | NotGiven = NOT_GIVEN,
        subcategory: Literal[
            "AIRLINES",
            "BALANCE_SHEET",
            "BANKS",
            "CASH_FLOW",
            "COMMODITIES",
            "COMPUTER_HARDWARE",
            "CONSUMER_SERVICES",
            "EDUCATION",
            "FINANCIAL_SERVICE_PROVIDER",
            "HOME_BUILDERS",
            "HOSPITALS",
            "HOTELS",
            "INCOME_STATEMENT",
            "INSURANCE",
            "MARIJUANA",
            "MINING",
            "MISCELLANEOUS",
            "MULTIFINANCIAL",
            "OIL_AND_GAS",
            "OTHER",
            "REITS",
            "RESTAURANTS",
            "RETAILERS",
            "TELECOMMUNICATIONS",
            "TRANSPORTATION",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricsResponse:
        """
        Returns list of available Estimate metrics that can be used in the `metrics`
        parameter of related endpoints. **By default, Factset provides Estimated items
        in millions. For specific metric methodology definitions, reference the `OAurl`
        response items to launch the available methodology page.**

        Args:
          category: Filters the list of Estimate metrics by major category -

              - **FINANCIAL_STATEMENT** = Includes Balance Sheet, Cash Flow, and Income
                Statement.
              - **INDUSTRY_METRICS** = Industry specific metrics.
              - **OTHER** = Target Price

          subcategory: Sub-Category Filter for the Primary Category Requested. Choose a related
              sub-category for the Category requested. For methodology, visit
              [OA 16038](https://my.apps.factset.com/oa/pages/16038) <p>Financial Statement -

              - **BALANCE_SHEET** - Balance Sheet line items, such as Assets, Long-term Debt,
                and more.
              - **CASH_FLOW** - Cash Flow Statement line items, such as Free Cash Flow and
                Share Repurchases
              - **INCOME_STATEMENT** - Income Statement line items, such as EPS, Sales, DPS,
                and more.
              - **MISCELLANEOUS** - EPS Long Term Growth
              </p> <p> Industry Metrics -

              - **AIRLINES** - Including items such as Revenue Passenger, Total Revenue per
                ASK, Available Seats, and more.
              - **BANKS** - Including items such as Net Interest Income, Trading Income, Net
                Loans, and more. SUPPLEMENTAL
              - **COMMODITIES** - Including items such as Average Target Price.
              - **COMPUTER_HARDWARE** - Including items such as Total Addressable Market.
              - **CONSUMER_SERVICES** - Including items such as Gross Merchandise Volume
              - **EDUCATION** - Including Items such as Total Student Enrollment
              - **FINANCIAL_SERVICE_PROVIDER** - Including items such as Annual Subscription
                Value
              - **HOME_BUILDERS** - Including items such as Home Sales, Land Sales,
                Cancellation Rates, and more.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **MARIJUANA** - Including items such as Cost per Gram and Kg of Cannabis Sold.
              - **MINING** - Including items such as Realized Price and Total Production
              - **MULTIFINANCIAL** - Including items such as AUM, Net Flows, and Fee Related
                Earnings.
              - **OIL_AND_GAS** - Including items such as Downstream Income, Production per
                Day, and Exploration Expense.
              - **OTHER** - Target Price
              - **REITS** - Including items such as Funds from Operations, Implied Cap Rate,
                and LTV.
              - **RESTAURANTS** - Including items such as Restaurant Margin.
              - **RETAILERS** - Including items such as Stores Information, Selling Space and
                Net sales per square foot.
              - **TELECOMMUNICATIONS** - Including items such as Gross Adds, Monthly Revenue
                Per User, Churn, and more.
              - **TRANSPORTATION** - Including items such as Revenue Per Unit, Volume Growth,
                and Operating Ratio.</p>

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-estimates/v2/metrics",
            body=await async_maybe_transform(
                {
                    "category": category,
                    "subcategory": subcategory,
                },
                metric_create_params.MetricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricsResponse,
        )

    async def list(
        self,
        *,
        category: Literal["FINANCIAL_STATEMENT", "INDUSTRY_METRIC", "OTHER"] | NotGiven = NOT_GIVEN,
        subcategory: Literal[
            "AIRLINES",
            "BALANCE_SHEET",
            "BANKS",
            "CASH_FLOW",
            "COMMODITIES",
            "COMPUTER_HARDWARE",
            "CONSUMER_SERVICES",
            "EDUCATION",
            "FINANCIAL_SERVICE_PROVIDER",
            "HOME_BUILDERS",
            "HOSPITALS",
            "HOTELS",
            "INCOME_STATEMENT",
            "INSURANCE",
            "MARIJUANA",
            "MINING",
            "MISCELLANEOUS",
            "MULTIFINANCIAL",
            "OIL_AND_GAS",
            "OTHER",
            "REITS",
            "RESTAURANTS",
            "RETAILERS",
            "TELECOMMUNICATIONS",
            "TRANSPORTATION",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricsResponse:
        """
        Returns list of available Estimate metrics that can be used in the `metrics`
        parameter of related endpoints. **By default, Factset provides Estimated items
        in millions. For specific metric methodology definitions, reference the `OAurl`
        response items to launch the available methodology page.**

        Args:
          category: Filters the list of Estimate metrics by major category -

              - **FINANCIAL_STATEMENT** = Includes Balance Sheet, Cash Flow, and Income
                Statement.
              - **INDUSTRY_METRICS** = Industry specific metrics.
              - **OTHER** = Target Price

          subcategory: Sub-Category Filter for the Primary Category Requested. Choose a related
              sub-category for the Category requested. For methodology, visit
              [OA 16038](https://my.apps.factset.com/oa/pages/16038) <p>Financial Statement -

              - **BALANCE_SHEET** - Balance Sheet line items, such as Assets, Long-term Debt,
                and more.
              - **CASH_FLOW** - Cash Flow Statement line items, such as Free Cash Flow and
                Share Repurchases
              - **INCOME_STATEMENT** - Income Statement line items, such as EPS, Sales, DPS,
                and more.
              - **MISCELLANEOUS** - EPS Long Term Growth
              </p> <p> Industry Metrics -

              - **AIRLINES** - Including items such as Revenue Passenger, Total Revenue per
                ASK, Available Seats, and more.
              - **BANKS** - Including items such as Net Interest Income, Trading Income, Net
                Loans, and more. SUPPLEMENTAL
              - **COMMODITIES** - Including items such as Average Target Price.
              - **COMPUTER_HARDWARE** - Including items such as Total Addressable Market.
              - **CONSUMER_SERVICES** - Including items such as Gross Merchandise Volume
              - **EDUCATION** - Including Items such as Total Student Enrollment
              - **FINANCIAL_SERVICE_PROVIDER** - Including items such as Annual Subscription
                Value
              - **HOME_BUILDERS** - Including items such as Home Sales, Land Sales,
                Cancellation Rates, and more.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **HOSPITALS** - Including items such as Bad Debt Provisions, Medical Cost
                Ratio, SS Admissions and more.
              - **HOTELS** - Including items such as Average Daily Rate, Occupancy %, RevPAR,
                and more.
              - **INSURANCE** - Including items such as Gross Premiums Written, Underwriting
                Income, and Claims.
              - **MARIJUANA** - Including items such as Cost per Gram and Kg of Cannabis Sold.
              - **MINING** - Including items such as Realized Price and Total Production
              - **MULTIFINANCIAL** - Including items such as AUM, Net Flows, and Fee Related
                Earnings.
              - **OIL_AND_GAS** - Including items such as Downstream Income, Production per
                Day, and Exploration Expense.
              - **OTHER** - Target Price
              - **REITS** - Including items such as Funds from Operations, Implied Cap Rate,
                and LTV.
              - **RESTAURANTS** - Including items such as Restaurant Margin.
              - **RETAILERS** - Including items such as Stores Information, Selling Space and
                Net sales per square foot.
              - **TELECOMMUNICATIONS** - Including items such as Gross Adds, Monthly Revenue
                Per User, Churn, and more.
              - **TRANSPORTATION** - Including items such as Revenue Per Unit, Volume Growth,
                and Operating Ratio.</p>

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-estimates/v2/metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category": category,
                        "subcategory": subcategory,
                    },
                    metric_list_params.MetricListParams,
                ),
            ),
            cast_to=MetricsResponse,
        )


class MetricsResourceWithRawResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.create = to_raw_response_wrapper(
            metrics.create,
        )
        self.list = to_raw_response_wrapper(
            metrics.list,
        )


class AsyncMetricsResourceWithRawResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.create = async_to_raw_response_wrapper(
            metrics.create,
        )
        self.list = async_to_raw_response_wrapper(
            metrics.list,
        )


class MetricsResourceWithStreamingResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.create = to_streamed_response_wrapper(
            metrics.create,
        )
        self.list = to_streamed_response_wrapper(
            metrics.list,
        )


class AsyncMetricsResourceWithStreamingResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.create = async_to_streamed_response_wrapper(
            metrics.create,
        )
        self.list = async_to_streamed_response_wrapper(
            metrics.list,
        )
