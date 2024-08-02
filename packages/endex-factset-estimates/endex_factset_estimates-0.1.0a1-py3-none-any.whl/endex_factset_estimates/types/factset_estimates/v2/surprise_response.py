# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SurpriseResponse", "Data"]


class Data(BaseModel):
    currency: Optional[str] = None
    """Currency code for adjusting the data.

    Use 'ESTIMATE' as input value for the values in Estimate Currency. For a list of
    currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    date: Optional[datetime.date] = None
    """Date for data expressed in YYYY-MM-DD format."""

    estimate_currency: Optional[str] = FieldInfo(alias="estimateCurrency", default=None)
    """Estimate currency of the requested Security"""

    event_description: Optional[str] = FieldInfo(alias="eventDescription", default=None)
    """Description of event.

    For more details, visit
    [Online Assistant Page #16601](https://oa.apps.factset.com/pages/16601).
    """

    event_flag: Optional[int] = FieldInfo(alias="eventFlag", default=None)
    """Flag for event.

    Code of Event Flag, where 0 = results and 1 = profit warning. For more details,
    visit [Online Assistant Page #16601](https://oa.apps.factset.com/pages/16601).
    """

    fiscal_end_date: Optional[datetime.date] = FieldInfo(alias="fiscalEndDate", default=None)
    """
    Company's 'fiscal end date' for the estimate record expressed in YYYY-MM-DD
    format
    """

    fiscal_period: Optional[int] = FieldInfo(alias="fiscalPeriod", default=None)
    """Company's 'fiscal period' for the estimate record.

    'Periodicity' defines context for period.
    """

    fiscal_year: Optional[int] = FieldInfo(alias="fiscalYear", default=None)
    """Company's 'fiscal year' for the estimate record"""

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)

    metric: Optional[str] = None
    """Company's Financial statement 'metric' that is estimated.

    Use the factset-estimates/v#/metrics endpoint for a complete list. For more
    details, visit
    [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).
    """

    periodicity: Optional[str] = None
    """
    Company's 'periodicity' for the estimate record, reflecting Annual, Quarterly,
    or Semi-Annual report periods. Next-twelve-months (NTMA) and Last-twelve-months
    (LTMA) also supported.
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)

    statistic: Optional[str] = None
    """Method of calculation for the consensus 'statistic'.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114).
    """

    surprise_after: Optional[float] = FieldInfo(alias="surpriseAfter", default=None)
    """Actual value after event.

    For more details, visit
    [Online Assistant Page #16145](https://oa.apps.factset.com/pages/16145).
    """

    surprise_amount: Optional[float] = FieldInfo(alias="surpriseAmount", default=None)
    """Amount of difference between last consensus and actual.

    For more details, visit
    [Online Assistant Page #16145](https://oa.apps.factset.com/pages/16145).
    """

    surprise_before: Optional[float] = FieldInfo(alias="surpriseBefore", default=None)
    """Last consensus before event.

    For more details, visit
    [Online Assistant Page #16145](https://oa.apps.factset.com/pages/16145).
    """

    surprise_date: Optional[datetime.date] = FieldInfo(alias="surpriseDate", default=None)
    """Date of the reported event expressed in YYYY-MM-DD format.

    For more details, visit
    [Online Assistant Page #16601](https://oa.apps.factset.com/pages/16601).
    """

    surprise_percent: Optional[float] = FieldInfo(alias="surprisePercent", default=None)
    """Percent difference between last consensus and actual.

    For more details, visit
    [Online Assistant Page #16145](https://oa.apps.factset.com/pages/16145).
    """


class SurpriseResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of surprises"""
