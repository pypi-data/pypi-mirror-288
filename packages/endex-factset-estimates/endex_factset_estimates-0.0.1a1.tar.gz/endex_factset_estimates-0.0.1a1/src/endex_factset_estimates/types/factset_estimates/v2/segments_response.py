# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SegmentsResponse", "Data"]


class Data(BaseModel):
    currency: Optional[str] = None
    """Currency used estimates in consensus calculations.

    Use 'ESTIMATE' as input for values in Estimate Currency. For a list of currency
    ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    down: Optional[int] = None
    """Number of Up Revisions within the consensus for the metric and period.

    The default window size is 100 days. For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114).
    """

    estimate_count: Optional[int] = FieldInfo(alias="estimateCount", default=None)
    """Count or NEST of estimates in consensus calculation.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114)
    """

    estimate_currency: Optional[str] = FieldInfo(alias="estimateCurrency", default=None)
    """Estimate currency of the requested Security"""

    estimate_date: Optional[date] = FieldInfo(alias="estimateDate", default=None)
    """The date the estimates are as of in YYYY-MM-DD format."""

    fiscal_end_date: Optional[date] = FieldInfo(alias="fiscalEndDate", default=None)
    """
    Company's 'fiscal end date' for the estimate record expressed in YYYY-MM-DD
    format. For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    fiscal_period: Optional[int] = FieldInfo(alias="fiscalPeriod", default=None)
    """Company's 'fiscal period' for the estimate record.

    Periods for periodicity of ANN = 1, and SEMI = 2. For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598).
    """

    fiscal_year: Optional[int] = FieldInfo(alias="fiscalYear", default=None)
    """Company's 'fiscal year' for the estimate record.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """Factset Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security’s best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    high: Optional[float] = None
    """Highest estimate in consensus calculation.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114).
    """

    low: Optional[float] = None
    """Lowest estimate in consensus calculation.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114)
    """

    mean: Optional[float] = None
    """Mean of estimates in consensus calculation.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114)
    """

    median: Optional[float] = None
    """Median of estimates in consensus calculation.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114)
    """

    metric: Optional[str] = None
    """Company's Financial statement 'metric' that is estimated.

    Use the factset-estimates/v#/metrics endpoint for a complete list. For more
    details, visit
    [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034)
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    segment_label: Optional[str] = FieldInfo(alias="segmentLabel", default=None)
    """Displays the specific label of the segment."""

    segment_level: Optional[str] = FieldInfo(alias="segmentLevel", default=None)
    """Returns the level of the segment item as either P = Parent or S = Subordinate"""

    segment_type: Optional[str] = FieldInfo(alias="segmentType", default=None)
    """Segment selected"""

    standard_deviation: Optional[float] = FieldInfo(alias="standardDeviation", default=None)
    """Standard deviation of estimates in consensus calculation.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114)
    """

    up: Optional[int] = None
    """Number of Up Revisions within the consensus for the metric and period.

    The default window size is 100 days For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16114).
    """


class SegmentsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Segments objects"""
