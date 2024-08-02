# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DealPublicTargetsParams", "Data"]


class DealPublicTargetsParams(TypedDict, total=False):
    data: Required[Data]
    """Deals Request Body"""


class Data(TypedDict, total=False):
    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """The end date requested for a given date range in **YYYY-MM-DD** format.

    Future dates (T+1) are not accepted in this endpoint.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """The start date requested for a given date range in **YYYY-MM-DD** format.

    Future dates (T+1) are not accepted in this endpoint.
    """

    status: Literal["All", "Pending", "Complete"]
    """Status of the deal"""
