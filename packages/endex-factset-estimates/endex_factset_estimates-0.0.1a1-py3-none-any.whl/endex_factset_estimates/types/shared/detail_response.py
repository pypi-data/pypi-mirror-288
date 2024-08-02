# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["DetailResponse", "Data"]


class Data(BaseModel):
    analyst_id: Optional[str] = FieldInfo(alias="analystId", default=None)
    """The FactSet Entity Identifier for the analyst making the estimate."""

    analyst_name: Optional[str] = FieldInfo(alias="analystName", default=None)
    """The name of the analyst making the estimate."""

    broker_estimate_currency: Optional[str] = FieldInfo(alias="brokerEstimateCurrency", default=None)
    """The currency in which estimates are made by broker."""

    broker_id: Optional[str] = FieldInfo(alias="brokerId", default=None)
    """The FactSet Entity Identifier for the broker making the estimate."""

    broker_name: Optional[str] = FieldInfo(alias="brokerName", default=None)
    """The name of the broker making the estimate."""

    currency: Optional[str] = None
    """Currency code for adjusting the data.

    Use 'ESTIMATE' as input value for the values in Estimate Currency. For a list of
    currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    estimate_currency: Optional[str] = FieldInfo(alias="estimateCurrency", default=None)
    """Estimate currency of the requested Security"""

    estimate_date: Optional[date] = FieldInfo(alias="estimateDate", default=None)
    """Date of estimate expressed in YYYY-MM-DD format.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    estimate_value: Optional[float] = FieldInfo(alias="estimateValue", default=None)
    """The value of the estimate."""

    fiscal_end_date: Optional[date] = FieldInfo(alias="fiscalEndDate", default=None)
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

    input_date_time: Optional[str] = FieldInfo(alias="inputDateTime", default=None)
    """Date and time when the data is available at the source."""

    last_modified_date: Optional[date] = FieldInfo(alias="lastModifiedDate", default=None)
    """The date at which a broker provided an estimate that is a revision."""

    metric: Optional[str] = None
    """Company's Financial statement 'metric' that is estimated.

    Use the factset-estimates/v#/metrics endpoint for a complete list. For more
    details, visit
    [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).
    """

    periodicity: Optional[str] = None
    """
    Company's 'periodicity' for the estimate record, reflecting Annual, Quarterly,
    or Semi-Annual report periods.
    """

    prev_estimate_date: Optional[date] = FieldInfo(alias="prevEstimateDate", default=None)
    """Date the previous estimate was made expressed in YYYY-MM-DD format.

    For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    prev_estimate_value: Optional[float] = FieldInfo(alias="prevEstimateValue", default=None)
    """The value of the previous estimate."""

    relative_period: Optional[int] = FieldInfo(alias="relativePeriod", default=None)
    """'Fiscal period' based on relationship to 'estimate date'.

    This is not applicable for fixed-consensus endpoint. For more details, visit
    [Online Assistant Page #16598](https://oa.apps.factset.com/pages/16598)
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    section: Optional[str] = None
    """
    Section of the estimate.Returns the details of brokers inlcuded and excluded in
    the consensus
    """

    security_currency: Optional[str] = FieldInfo(alias="securityCurrency", default=None)
    """The currency that the company trades in."""

    status_code: Optional[int] = FieldInfo(alias="statusCode", default=None)
    """Status code of the estimate."""

    status_text: Optional[str] = FieldInfo(alias="statusText", default=None)
    """Status description of the estimate."""


class DetailResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of consensus estimate objects"""
