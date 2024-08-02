# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DealsResponse", "Data", "DataBuyer", "DataSeller", "DataTarget"]


class DataBuyer(BaseModel):
    fsym_id: str = FieldInfo(alias="fsymId")
    """FactSet Permanent Identifier of the participant.

    Six alpha-numeric characters, excluding vowels, with an -E suffix (XXXXXX-E).
    """

    industry: Optional[str] = None
    """
    Industry of the participant based on the FactSet Industry Classification system.
    """

    name: Optional[str] = None
    """Entity name of the participant."""

    ultimate_parent_id: Optional[str] = FieldInfo(alias="ultimateParentId", default=None)
    """FactSet Permanent Identifier of the ultimate parent of the participant.

    Six alpha-numeric characters, excluding vowels, with an -E suffix (XXXXXX-E).
    """


class DataSeller(BaseModel):
    fsym_id: str = FieldInfo(alias="fsymId")
    """FactSet Permanent Identifier of the participant.

    Six alpha-numeric characters, excluding vowels, with an -E suffix (XXXXXX-E).
    """

    industry: Optional[str] = None
    """
    Industry of the participant based on the FactSet Industry Classification system.
    """

    name: Optional[str] = None
    """Entity name of the participant."""

    ultimate_parent_id: Optional[str] = FieldInfo(alias="ultimateParentId", default=None)
    """FactSet Permanent Identifier of the ultimate parent of the participant.

    Six alpha-numeric characters, excluding vowels, with an -E suffix (XXXXXX-E).
    """


class DataTarget(BaseModel):
    fsym_id: str = FieldInfo(alias="fsymId")
    """FactSet Permanent Identifier of the participant.

    Six alpha-numeric characters, excluding vowels, with an -E suffix (XXXXXX-E).
    """

    industry: Optional[str] = None
    """
    Industry of the participant based on the FactSet Industry Classification system.
    """

    name: Optional[str] = None
    """Entity name of the participant."""


class Data(BaseModel):
    announce_date: Optional[date] = FieldInfo(alias="announceDate", default=None)
    """Date the deal was announced.

    If the deal has a status of `rumor` or `rumor cancelled`, then this may be the
    same as `rumorDate`.
    """

    buyers: Optional[List[DataBuyer]] = None
    """Array of participants in the deal who are buyers."""

    close_date: Optional[date] = FieldInfo(alias="closeDate", default=None)
    """Date the deal was closed."""

    deal_id: Optional[str] = FieldInfo(alias="dealId", default=None)
    """Identifier for the deal."""

    deal_type: Optional[Literal["Acquisition / Merger", "Majority Stake", "Minority Stake", "Spinoff"]] = FieldInfo(
        alias="dealType", default=None
    )
    """Type of deal."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    sellers: Optional[List[DataSeller]] = None
    """Array of participants in the deal who are sellers."""

    status: Optional[Literal["Pending", "Complete", "Cancelled", "Rumor", "Rumor Cancelled"]] = None
    """Status of the deal"""

    target: Optional[DataTarget] = None
    """Target Object"""

    transaction_value: Optional[float] = FieldInfo(alias="transactionValue", default=None)
    """
    Base Equity Value plus the value of the target’s outstanding net debt (where
    applicable). The target's outstanding net debt is defined as the total amount of
    short and long term interest-bearing debt less any cash and cash equivalents.
    The target's outstanding net debt will only be included in the Transaction Value
    calculation if a.) the acquirer is seeking to own 100% of the target, b.) the
    target is a non-financial company; and c.) the target's outstanding net debt is
    publicly disclosed (or the acquirer publicly states it is assuming a specific
    amount of liabilities). Otherwise, Transaction Value will be equal to the amount
    paid for the portion of the target acquired (Base Equity Value) and will exclude
    the target's outstanding net debt. Amounts returned are in USD.
    """


class DealsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Deals Objects"""
