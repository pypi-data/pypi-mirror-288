# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ConsensusRatingCreateParams"]


class ConsensusRatingCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids. _ Make Note - id limit of 3000 for defaults, otherwise the
    service is limited to a 30 second duration. This can be reached when increasing
    total number of metrics requested and depth of history. _
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

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    If left blank, the API will default to previous close. Future dates (T+1) are
    not accepted in this #endpoint.
    """
