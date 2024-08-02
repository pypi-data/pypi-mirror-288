# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["DetailRatingsResponse", "Data"]


class Data(BaseModel):
    analyst_id: Optional[str] = FieldInfo(alias="analystId", default=None)
    """The FactSet Entity Identifier for the analyst making the estimate."""

    analyst_name: Optional[str] = FieldInfo(alias="analystName", default=None)
    """The name of the analyst making the estimate."""

    broker_id: Optional[str] = FieldInfo(alias="brokerId", default=None)
    """The FactSet Entity Identifier for the broker making the estimate."""

    broker_name: Optional[str] = FieldInfo(alias="brokerName", default=None)
    """The name of the broker making the estimate."""

    estimate_date: Optional[date] = FieldInfo(alias="estimateDate", default=None)
    """Date of estimate expressed in YYYY-MM-DD format.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)

    input_date_time: Optional[str] = FieldInfo(alias="inputDateTime", default=None)
    """Date and time when the data is available at the source."""

    last_modified_date: Optional[date] = FieldInfo(alias="lastModifiedDate", default=None)
    """The date at which a broker provided an estimate that is a revision."""

    ratings_note_text: Optional[str] = FieldInfo(alias="ratingsNoteText", default=None)
    """A textual representation of the analysts rating.

    Broker recommendations are divided into five main broad categories- **Buy,
    Overweight, Hold, Underweight, and Sell**.<p>Additional recommendations may be
    displayed for the below reasons -

    - Without- A rating "Without" is displayed when a broker provides estimates but
      does not provide a rating.
    - Dropping- When a broker stops covering an equity, the recommendation will show
      "Dropping."
    - Not Available- A broker may be "Not Available" due to outstanding
      circumstances with that particular security. Ratings are not displayed until a
      new rating is provided.
    - Most/Least- "Most" or "Least" favorable rating is displayed for top or bottom
      rating available for a particular security.
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""


class DetailRatingsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of detail ratings estimate objects"""
