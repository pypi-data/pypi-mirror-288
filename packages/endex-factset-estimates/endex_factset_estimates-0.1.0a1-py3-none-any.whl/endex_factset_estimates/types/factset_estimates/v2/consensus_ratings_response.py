# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["ConsensusRatingsResponse", "Data"]


class Data(BaseModel):
    buy_count: Optional[int] = FieldInfo(alias="buyCount", default=None)
    """The number of Buy ratings taken into account in the calculation of a consensus.

    This information is shown only for a 100-day consensus.
    """

    estimate_date: Optional[date] = FieldInfo(alias="estimateDate", default=None)
    """Date of estimate expressed in YYYY-MM-DD format.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)

    hold_count: Optional[int] = FieldInfo(alias="holdCount", default=None)
    """The number of Hold ratings taken into account in the calculation of a consensus.

    This information is shown only for a 100-day consensus.
    """

    overweight_count: Optional[int] = FieldInfo(alias="overweightCount", default=None)
    """
    The number of Overweight ratings taken into account in the calculation of a
    consensus. This information is shown only for a 100-day consensus.
    """

    ratings_nest_total: Optional[int] = FieldInfo(alias="ratingsNestTotal", default=None)
    """The total number of ratings taken into account in the calculation of a
    consensus.

    This information is shown only for a 100-day consensus.
    """

    ratings_note: Optional[float] = FieldInfo(alias="ratingsNote", default=None)
    """
    The mean average of ratings for the fiscal dates indicated, where each
    underlying rating is given a numerical score and then aggregated to a mean
    consensus - **_Individual Ratings Scores_** |Value|Rating Description| |---|---|
    |1|Buy| |1.5|Overweight| |2|Hold| |2.5|Underweight| |3|Sell|
    """

    ratings_note_text: Optional[str] = FieldInfo(alias="ratingsNoteText", default=None)
    """The mean textual rating for the fiscal dates indicated.

    The text rating is assigned by falling within the below defined ranges -
    **_Textual Ranges for Average_** |Value|Rating Description| |---|---| |<
    1.25|Buy| |< 1.75|Overweight| |< 2.25|Hold| |< 2.75|Underweight| |<= 3|Sell|
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    sell_count: Optional[int] = FieldInfo(alias="sellCount", default=None)
    """The number of Sell ratings taken into account in the calculation of a consensus.

    This information is shown only for a 100-day consensus.
    """

    underweight_count: Optional[int] = FieldInfo(alias="underweightCount", default=None)
    """
    The number of Underweight ratings taken into account in the calculation of a
    consensus. This information is shown only for a 100-day consensus.
    """


class ConsensusRatingsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of consensus ratings estimate objects"""
