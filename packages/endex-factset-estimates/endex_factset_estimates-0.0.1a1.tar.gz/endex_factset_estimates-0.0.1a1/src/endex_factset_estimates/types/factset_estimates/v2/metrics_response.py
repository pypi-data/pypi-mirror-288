# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["MetricsResponse", "Data"]


class Data(BaseModel):
    category: Optional[str] = None
    """
    Primary Category of metric item, such as, FINANCIAL_STATEMENT or INDUSTRY_METRIC
    """

    metric: Optional[str] = None
    """
    Metric identifier to be used as `metrics` input in the FactSet Estimate
    endpoints.
    """

    name: Optional[str] = None
    """Plain text name of the metric."""

    o_aurl: Optional[str] = FieldInfo(alias="OAurl", default=None)
    """
    The Online Assistant Page URL, used to lookup the definition and methodology of
    the requested item.
    """

    subcategory: Optional[str] = None
    """Sub-category of metric items, such as the INCOME_STATEMENT or AIRLINES."""


class MetricsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """
    Array of metric objects representing the metrics that can be requested from the
    estimates APIs.
    """
