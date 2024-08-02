# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["MetricCreateParams"]


class MetricCreateParams(TypedDict, total=False):
    category: Literal["FINANCIAL_STATEMENT", "INDUSTRY_METRIC", "OTHER"]
    """Filters the list of Estimate metrics by major category -

    - **FINANCIAL_STATEMENT** = Includes Balance Sheet, Cash Flow, and Income
      Statement.
    - **INDUSTRY_METRICS** = Industry specific metrics.
    - **OTHER** = Target Price
    """

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
    """Sub-Category Filter for the Primary Category Requested.

    Choose a related sub-category for the Category requested. For methodology, visit
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
    """
