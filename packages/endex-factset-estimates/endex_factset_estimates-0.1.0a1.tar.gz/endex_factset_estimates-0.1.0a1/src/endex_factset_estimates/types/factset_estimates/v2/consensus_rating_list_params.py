# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["ConsensusRatingListParams"]


class ConsensusRatingListParams(TypedDict, total=False):
    ids: Required[List[str]]
    """Security or Entity identifiers.

    FactSet Identifiers, tickers, CUSIP and SEDOL are accepted input. <p>**\\**ids
    limit** = 3000 per request*</p> * Make Note - id limit of 3000 for defaults,
    otherwise the service is limited to a 30 second duration. This can be reached
    when increasing total number of metrics requested and depth of history. \\**
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """End date for point in time of estimates expressed in YYYY-MM-DD format."""

    frequency: Literal["D", "W", "AM", "AQ", "AY"]
    """Controls the frequency of the data returned.

    - **D** = Daily
    - **W** = Weekly, based on the last day of the week of the start date.
    - **AM** = Monthly, based on the start date (e.g., if the start date is June 16,
      data is displayed for June 16, May 16, April 16 etc.).
    - **AQ** = Quarterly, based on the start date.
    - **AY** = Actual Annual, based on the start date.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Start date for point in time of estimates expressed in YYYY-MM-DD format."""
