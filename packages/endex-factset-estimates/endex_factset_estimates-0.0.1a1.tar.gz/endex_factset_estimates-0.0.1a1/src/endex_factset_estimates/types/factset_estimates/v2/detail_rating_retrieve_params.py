# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DetailRatingRetrieveParams"]


class DetailRatingRetrieveParams(TypedDict, total=False):
    ids: Required[List[str]]
    """Security or Entity identifiers.

    FactSet Identifiers, tickers, CUSIP and SEDOL are accepted input. <p>**\\**ids
    limit** = 3000 per request*</p> * Make Note - id limit of 3000 for defaults,
    otherwise the service is limited to a 30 second duration. This can be reached
    when increasing total number of metrics requested and depth of history. \\**
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """End date for point in time of estimates expressed in YYYY-MM-DD format."""

    include_all: Annotated[bool, PropertyInfo(alias="includeAll")]
    """
    Include All filter is used to identify included and excluded broker details from
    the consensus By default the service would return only the brokers included in
    the consensus-

    - **TRUE** = Returns all the brokers included and excluded in the consensus
    - **FALSE** = Returns only the broker details included in the consensus
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Start date for point in time of estimates expressed in YYYY-MM-DD format."""
