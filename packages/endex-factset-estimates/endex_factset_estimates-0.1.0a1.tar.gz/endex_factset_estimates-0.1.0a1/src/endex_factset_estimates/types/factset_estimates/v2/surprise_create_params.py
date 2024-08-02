# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SurpriseCreateParams"]


class SurpriseCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids. _ Make Note - id limit of 3000 for defaults, otherwise the
    service is limited to a 30 second duration. This can be reached when increasing
    total number of metrics requested and depth of history. _
    """

    metrics: Required[List[str]]
    """Requested metrics.

    Use the metrics endpoint for a list of estimate items. Note, the number of
    metrics you are allowed to supply is limited to 1 for now. For more details,
    visit [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).
    """

    currency: str
    """Currency code for adjusting the data.

    Use input as 'ESTIMATE' for values in Estimate currency. For a list of currency
    ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """The end date requested for a given date range in **YYYY-MM-DD** format.

    If left blank, the API will default to previous close. Future dates (T+1) are
    not accepted in this endpoint.
    """

    frequency: Literal["D", "W", "AM", "AQ", "AY"]
    """Controls the display frequency of the data returned.

    - **D** = Daily
    - **W** = Weekly, based on the last day of the week of the start date.
    - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
      data is displayed for June 16, May 16, April 16 etc.).
    - **AQ** = Quarterly, based on the start date.
    - **AY** = Actual Annual, based on the start date.
    """

    periodicity: Literal["ANN", "QTR", "SEMI"]
    """
    The periodicity for the estimates, reflecting Annual, Semi-Annual and Quarterly
    Estimates.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    If left blank, the API will default to previous close. Future dates (T+1) are
    not accepted in this #endpoint.
    """

    statistic: Literal["MEAN", "MEDIAN", "HIGH", "LOW", "COUNT", "STDDEV"]
    """Statistic for consensus calculation."""
