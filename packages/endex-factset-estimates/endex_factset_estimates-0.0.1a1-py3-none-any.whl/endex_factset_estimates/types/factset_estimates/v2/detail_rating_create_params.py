# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DetailRatingCreateParams"]


class DetailRatingCreateParams(TypedDict, total=False):
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

    include_all: Annotated[bool, PropertyInfo(alias="includeAll")]
    """
    Include All filter is used to identify included and excluded broker details from
    the consensus By default the service would return only the brokers included in
    the consensus-

    - **TRUE** = Returns all the brokers included and excluded in the consensus
    - **FALSE** = Returns only the broker details included in the consensus
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    If left blank, the API will default to previous close. Future dates (T+1) are
    not accepted in this #endpoint.
    """
