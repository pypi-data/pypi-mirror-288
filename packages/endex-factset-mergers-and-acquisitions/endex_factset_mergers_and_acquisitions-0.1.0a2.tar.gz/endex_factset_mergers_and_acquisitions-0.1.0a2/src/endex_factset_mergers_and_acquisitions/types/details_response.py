# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DetailsResponse", "Data", "DataBuyer", "DataDealValue", "DataSeller", "DataTarget"]


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


class DataDealValue(BaseModel):
    ann_offer_price_share: Optional[float] = FieldInfo(alias="annOfferPriceShare", default=None)
    """
    The current price offered for each share of target stock (including all forms of
    consideration). In a transaction in which the acquirer has increased or decrease
    the price they are offering on a per share basis from their original offer
    price, this item will always reflect the most current price per share being
    offered. Amounts returned are in USD.
    """

    base_equity: Optional[float] = FieldInfo(alias="baseEquity", default=None)
    """
    The total value of cash and all other forms of payment made to the Target –
    commonly cash and/or stock, though the calculation can include other methods of
    payment (e.g., notes, convertible debt, preferred stock, etc.) if disclosed and
    calculable. In transactions where multiple forms of payment are being made
    (e.g., cash and stock), the individual consideration components are calculated
    separately and then summed to arrive at the total Base Equity Value (e.g., cash
    component + stock component). Amounts returned are in USD.
    """

    buyer_exchange_ratio: Optional[float] = FieldInfo(alias="buyerExchangeRatio", default=None)
    """Number of shares being issued by the acquirer to the target.

    Applicable only if the acquirer is issuing stock in the transaction. For
    example, Express Scripts, Inc. acquired Medco Health Solutions, Inc. in April
    2012 for $28.5 bil in cash and stock. Medco shareholders received $28.8 in cash
    and 0.81 Express Scripts shares for every share held. Here, Stock Exchange
    Ratio - Buyers Shares is 0.81.
    """

    buyer_shares_issued: Optional[float] = FieldInfo(alias="buyerSharesIssued", default=None)
    """The number of shares issued by the buyer to the target as part of the payment."""

    cash_share: Optional[float] = FieldInfo(alias="cashShare", default=None)
    """Portion of the current offer price per share to be paid in cash.

    For example, Pfizer acquired Wyeth in 2009 for
    $66.8 in cash and stock. Pfizer paid $50.19 per share, comprised of $33 in cash and 0.985 shares of Pfizer stock (representing $17.19 based upon Pfizer's last closing stock price of $17.45 prior to announcement). Here, the Price/Share - Cash ($)
    is 33. Amounts returned are in USD.
    """

    choice: Optional[bool] = None
    """
    Indicates if the acquirer is offering the target shareholders a choice of
    considerations (which is almost always a choice between selecting cash only,
    stock only or a mixture of cash and stock) for the specified deal identifier.
    """

    enterprise_value: Optional[float] = FieldInfo(alias="enterpriseValue", default=None)
    """
    The full value of the business acquired, using % sought to determine the value
    of 100% of the business if less than 100% was sought in the transaction. Amounts
    returned are in USD.
    """

    payment_method: Optional[
        List[
            Optional[
                Literal[
                    "Cash",
                    "Cash & Stock",
                    "Convertible Preferred Stock",
                    "Debt",
                    "Notes",
                    "Other",
                    "Preferred Stock",
                    "Stock",
                    "Warrant / Options",
                ]
            ]
        ]
    ] = FieldInfo(alias="paymentMethod", default=None)
    """
    Payment method/structure used in the transaction, including cash, stock,
    combination, or debt.
    """

    percent_sought: Optional[float] = FieldInfo(alias="percentSought", default=None)
    """
    The percentage of the target company's stock sought by the acquirer at the time
    the transaction was publicly announced.
    """

    premium1_day: Optional[float] = FieldInfo(alias="premium1Day", default=None)
    """
    The percentage difference between the price per share offered by the acquirer
    and the target's closing stock price 1 trading day prior to the announcement
    date. This data is only available if the target is a public company and the
    price/share is disclosed.
    """

    premium30_day: Optional[float] = FieldInfo(alias="premium30Day", default=None)
    """
    The percentage difference between the price per share offered by the acquirer
    and the target's closing stock price 30 trading days prior to the announcement
    date. This data is only available if the target is a public company and the
    price/share is disclosed.
    """

    premium5_day: Optional[float] = FieldInfo(alias="premium5Day", default=None)
    """
    The percentage difference between the price per share offered by the acquirer
    and the target's closing stock price 5 trading days prior to the announcement
    date. This data is only available if the target is a public company and the
    price/share is disclosed.
    """

    shares_owned_prior: Optional[float] = FieldInfo(alias="sharesOwnedPrior", default=None)
    """
    The percent of the target company's shares owned by the buyer prior to the
    transaction.
    """

    shares_sought: Optional[float] = FieldInfo(alias="sharesSought", default=None)
    """
    The number of shares of the target company's stock sought by the acquirer at the
    time the transaction was publicly announced.
    """

    stock_share: Optional[float] = FieldInfo(alias="stockShare", default=None)
    """Portion of the current offer price per share to be paid in the acquirer's stock.

    For example, Pfizer acquired Wyeth in 2009 for
    $66.8 in cash and stock. Pfizer paid $50.19 per share, comprised of $33 in cash and 0.985 shares of Pfizer stock (representing $17.19 based upon Pfizer's last closing stock price of $17.45 prior to announcement). Here, the Price/Share - Stock ($)
    is 17.19. Amounts returned are in USD.
    """

    target_exchange_ratio: Optional[float] = FieldInfo(alias="targetExchangeRatio", default=None)
    """
    Number of target shares the stock swap exchange ratio is based upon when the
    acquirer is issuing stock in the transaction. For example, Express Scripts, Inc.
    acquired Medco Health Solutions, Inc. in April 2012 for $28.5 bil in cash and
    stock. Medco shareholders received $28.8 in cash and 0.81 Express Scripts shares
    for every share held. Here, Stock Exchange Ratio - Target Shares is 1.
    """

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
    """Date the deal was announced."""

    attitude: Optional[Literal["Friendly", "Hostile", "Neutral"]] = None
    """
    The way the target's board of directors viewed the acquirer's proposal to enter
    into the transaction - Friendly, Hostile, Neutral.
    """

    bep_bv: Optional[float] = FieldInfo(alias="bepBV", default=None)
    """Ratio: BEP/BV."""

    book_value_share: Optional[float] = FieldInfo(alias="bookValueShare", default=None)
    """Book value per share at the time of the deal in USD."""

    buyer_post_merger_own: Optional[float] = FieldInfo(alias="buyerPostMergerOwn", default=None)
    """
    Post Merger Ownership % - Acquirer: The pro forma percentage of ownership to be
    held by acquirer shareholders in the newly merged company. This data item is
    designed to reflect the expected ownership of the newly merged company at the
    time the transaction was announced. This data item will not be populated for
    Going Private transactions as they are not applicable since the acquirer in a
    going private transaction is not publicly traded.
    """

    buyers: Optional[List[DataBuyer]] = None
    """Array of participants in the deal who are buyers."""

    cancel_date: Optional[date] = FieldInfo(alias="cancelDate", default=None)
    """Date the deal was cancelled."""

    cash: Optional[float] = None
    """Cash at the time of the deal in USD."""

    close_date: Optional[date] = FieldInfo(alias="closeDate", default=None)
    """Date the deal was closed."""

    deal_characteristics: Optional[
        List[
            Optional[
                Literal[
                    "Divestment",
                    "Employee Buy-Out",
                    "Exit",
                    "Investor Buy-In",
                    "Investor Buy-Out",
                    "Insolvency",
                    "Management Buy-Out",
                    "Reverse Takeover",
                    "Secondary Buy-Out",
                    "Leveraged Buy-Out",
                    "Going Private",
                    "Exit (Partial)",
                    "Control Premium Study",
                    "Private Equity Group",
                    "Asset Purchase",
                    "Related Party",
                    "Tender Offer",
                    "Unequal Voting",
                    "Target Controlling Shareholder",
                    "Auction",
                    "Club Deal - PE Group",
                    "Club Deal - Corp/PE",
                    "Venture Backed Acquirer",
                    "Unsolicited Bid",
                    "Rumor",
                    "Scheme of Arrangement",
                    "Golden Share",
                    "Merger of Equals",
                    "Privatization",
                    "Indicative / Tentative Proposal",
                    "Club Deal - Corporate Group",
                    "Multiple Target Deal",
                    "SPAC",
                    "Squeeze Out",
                    "Special Committee",
                    "Collar",
                    "Forced Regulatory Divestiture",
                    "Venture-Backed Target",
                    "Bank Branch Purchase",
                    "Bidder Special Committee",
                    "Target Special Committee",
                    "Bidder Controlling Shareholder",
                    "Property Transaction",
                    "Power Plant Purchase",
                ]
            ]
        ]
    ] = FieldInfo(alias="dealCharacteristics", default=None)
    """The secondary deal type(s)."""

    deal_id: Optional[str] = FieldInfo(alias="dealId", default=None)
    """FactSet unique deal Identifier."""

    deal_summary: Optional[str] = FieldInfo(alias="dealSummary", default=None)
    """Summary of the deal."""

    deal_type: Optional[Literal["Acquisition / Merger", "Majority Stake", "Minority Stake", "Spinoff"]] = FieldInfo(
        alias="dealType", default=None
    )
    """Type of deal."""

    deal_value: Optional[DataDealValue] = FieldInfo(alias="dealValue", default=None)
    """Deal Value Object"""

    ebit: Optional[float] = None
    """EBIT at the time of the deal in USD."""

    ebitda: Optional[float] = None
    """EBITDA at the time of the deal in USD."""

    eps: Optional[float] = None
    """Earnings per share at the time of the deal in USD."""

    ev_ebit: Optional[float] = FieldInfo(alias="evEBIT", default=None)
    """Ratio: Enterprise value/EBIT."""

    ev_ebitda: Optional[float] = FieldInfo(alias="evEBITDA", default=None)
    """Ratio: Enterprise value/EBITDA."""

    ev_sales: Optional[float] = FieldInfo(alias="evSales", default=None)
    """Ratio: Enterprise value/sales."""

    expected_close_date: Optional[date] = FieldInfo(alias="expectedCloseDate", default=None)
    """Expected close date of the deal."""

    int_bearing_debt: Optional[float] = FieldInfo(alias="intBearingDebt", default=None)
    """Interest bearing debt at the time of the deal in USD."""

    net_income: Optional[float] = FieldInfo(alias="netIncome", default=None)
    """Net income at the time of the deal in USD."""

    pref_stock_value: Optional[float] = FieldInfo(alias="prefStockValue", default=None)
    """Preferred stock value at the time of the deal in USD."""

    purpose: Optional[Literal["Financial", "Strategic"]] = None
    """Transaction purpose code or description."""

    reference_date: Optional[date] = FieldInfo(alias="referenceDate", default=None)
    """
    In a competing bid situation, the common date (earliest announcement date) used
    across all related transactions in order to determine the target's share prices,
    financials, premiums/multiples and all currency conversions (allowing for a
    common basis of comparison). For all other transactions, the Competing Bid
    Reference Date will be the same as the Announcement Date. For example, Peet's
    Coffee & Tea, Inc. announced its intent to acquire Diedrich Coffee, Inc. on
    2009-11-02. Green Mountain Coffee Roasters jumped this transaction, announcing
    its own competing bid on 2009-11-23. Green Mountain eventually won its bid,
    completing the acquisition on 2010-05-11. For both transactions, the Competing
    Bid Reference Date is 2009-11-02.
    """

    rumor_date: Optional[date] = FieldInfo(alias="rumorDate", default=None)
    """
    For a transaction that initially start out as a rumor, the date on which talks
    of the transaction first appeared in a major financial or trade publication. For
    so long as the transaction remains a rumor, the Rumor Date and the Announcement
    Date will be the same. Once confirmed and the transaction is no longer a rumor,
    the Rumor Date will remain unchanged and the Announcement Date will be updated
    to reflect the date upon which one of the parties involved in the deal disclosed
    the formal offer or a definitive agreement.
    """

    sales: Optional[float] = None
    """Sales at the time of the deal in USD."""

    sellers: Optional[List[DataSeller]] = None
    """Array of participants in the deal who are sellers."""

    shares_outstanding: Optional[float] = FieldInfo(alias="sharesOutstanding", default=None)
    """Shares outstanding at the time of the deal."""

    source_funds: Optional[
        List[
            Optional[
                Literal[
                    "Bank Loan",
                    "Bond/Note Issuance",
                    "Internally Generated Funds",
                    "Mezzanine",
                    "Private Company Debt",
                    "Private Equity/Venture Funding",
                    "Private Warrant Option",
                    "Source of Funding Not Disclosed",
                    "Stock Issuance: Pref & Com (Public)",
                ]
            ]
        ]
    ] = FieldInfo(alias="sourceFunds", default=None)
    """
    Method by which the acquirer was to finance the cash portion of the
    consideration offered in transaction (e.g., cash, bank debt, issuance of
    notes/bonds, etc.). For example, VF Corp financed its $2.2 bil all cash offer
    for The Timberland Company by issuing $900 mil in term notes and funding the
    balance through a combination of cash on hand and commercial paper.
    """

    status: Optional[Literal["Pending", "Complete", "Cancelled", "Rumor", "Rumor Cancelled"]] = None
    """Status of the deal."""

    target: Optional[DataTarget] = None
    """Target Object"""

    target_post_merger_own: Optional[float] = FieldInfo(alias="targetPostMergerOwn", default=None)
    """
    Post Merger Ownership % - Target: The pro forma percentage of ownership to be
    held by target shareholders in the newly merged company. This data item is
    designed to reflect the expected ownership of the newly merged company at the
    time the transaction was announced. This data item will not be populated for
    Going Private transactions as they are not applicable since the acquirer in a
    going private transaction is not publicly traded.
    """

    total_assets: Optional[float] = FieldInfo(alias="totalAssets", default=None)
    """Total assets at the time of the deal in USD."""


class DetailsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Details Objects"""
