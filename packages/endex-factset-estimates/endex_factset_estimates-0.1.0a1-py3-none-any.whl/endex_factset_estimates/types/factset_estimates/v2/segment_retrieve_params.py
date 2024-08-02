# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SegmentRetrieveParams"]


class SegmentRetrieveParams(TypedDict, total=False):
    ids: Required[List[str]]
    """Security or Entity identifiers.

    FactSet Identifiers, tickers, CUSIP and SEDOL are accepted input. <p>**\\**ids
    limit** = 50 per request*</p> * Make Note - id limit of 50 for defaults,
    otherwise the service is limited to a 30 second duration. This can be reached
    when increasing total number of metrics requested and depth of history. \\**
    """

    metrics: Required[List[str]]
    """Requested metrics.

    Use the /metrics endpoint to return a list of available estimate items. Note,
    the number of metrics you are allowed to supply is limited to 1 for now. **Top
    10** most used metrics are **EPS, SALES, DPS, EBITDA,EBIT, PRICE_TGT, CFPS, BPS,
    NET_INC, and ASSETS**. For more details, visit
    [Online Assistant Page #15034](https://oa.apps.factset.com/pages/15034).
    """

    segment_type: Required[Annotated[Literal["BUS", "GEO"], PropertyInfo(alias="segmentType")]]
    """Controls the type of segment selected.

    - **BUS** = Business / Product Segment
    - **GEO** = Geographic Segment
    """

    currency: str
    """Currency code for adjusting the data.

    Use 'ESTIMATE' as input value for the values in Estimate Currency. For a list of
    currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
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

    periodicity: Literal["ANN", "QTR", "SEMI", "NTMA", "LTMA"]
    """
    The periodicity for the estimates requested, allowing you to fetch Quarterly,
    Semi-Annual, Annual, and NTMA/LTMA Estimates.

    - **ANN** - Annual
    - **QTR** - Quarterly
    - **SEMI** - Semi-Annual
    - **NTMA** - Next-Twelve-Months - Time-weighted Annual. Estimates use a
      percentage of annual estimates from two fiscal years to create an estimate
      based on the 12-month period. Visit
      [OA 16614](https://my.apps.factset.com/oa/pages/16614) for detail.
    - **LTMA** - Last-Twelve-Months - Time-weighted Annual. Estimates use a
      percentage of annual estimates from two fiscal years to create an estimate
      based on the 12-month period. Visit
      [OA 16614](https://my.apps.factset.com/oa/pages/16614) for detail.
    """

    relative_fiscal_end: Annotated[int, PropertyInfo(alias="relativeFiscalEnd")]
    """Relative fiscal period, expressed as an integer, used to filter results.

    This is combined with the periodicity parameter to specify a relative estimate
    period. For example, set to 2 and periodicity to ANN to ask for relative Fiscal
    Year 1 (FY2).
    """

    relative_fiscal_start: Annotated[int, PropertyInfo(alias="relativeFiscalStart")]
    """Relative fiscal period, expressed as an integer, used to filter results.

    This is combined with the periodicity parameter to specify a relative estimate
    period. For example, set to 1 and periodicity to ANN to ask for relative Fiscal
    Year 1 (FY1).
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Start date for point in time of estimates expressed in YYYY-MM-DD format."""
