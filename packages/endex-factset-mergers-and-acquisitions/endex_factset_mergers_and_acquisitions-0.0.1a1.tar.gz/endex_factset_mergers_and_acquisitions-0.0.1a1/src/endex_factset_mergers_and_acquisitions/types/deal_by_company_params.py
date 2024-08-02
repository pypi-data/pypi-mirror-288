# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DealByCompanyParams", "Data"]


class DealByCompanyParams(TypedDict, total=False):
    data: Required[Data]
    """Deals Request Body"""


class Data(TypedDict, total=False):
    ids: Required[List[str]]
    """The requested list of security identifiers.

    Accepted ID types include Market Tickers, SEDOL, ISINs, CUSIPs, or FactSet
    Permanent Ids. Maximum of 500 IDs are supported.
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """The end date requested for a given date range in **YYYY-MM-DD** format.

    Future dates (T+1) are not accepted in this endpoint.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    Future dates (T+1) are not accepted in this endpoint.
    """
