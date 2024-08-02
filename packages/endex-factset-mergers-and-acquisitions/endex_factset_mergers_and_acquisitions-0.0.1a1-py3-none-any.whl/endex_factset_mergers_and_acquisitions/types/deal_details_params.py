# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DealDetailsParams", "Data"]


class DealDetailsParams(TypedDict, total=False):
    data: Required[Data]
    """Details Request Body"""


class Data(TypedDict, total=False):
    deal_ids: Required[Annotated[List[str], PropertyInfo(alias="dealIds")]]
    """The requested list of deal identifiers. Maximum of 100 IDs are supported."""
