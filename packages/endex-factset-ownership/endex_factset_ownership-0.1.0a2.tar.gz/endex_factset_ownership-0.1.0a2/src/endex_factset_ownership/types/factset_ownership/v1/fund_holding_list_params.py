# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["FundHoldingListParams"]


class FundHoldingListParams(TypedDict, total=False):
    ids: Required[List[str]]
    """List of requested fund identifiers. <p>**\\**ids limit** = 10 per request\\**</p>"""

    asset_type: Annotated[Literal["ALL", "EQ", "FI"], PropertyInfo(alias="assetType")]
    """Filter holdings by the following major asset classes -

    - **EQ** = Equity
    - **FI** = Fixed Income
    - **ALL** = ALL
    """

    currency: str
    """Currency code for adjusting prices.

    Default is Local. For a list of currency ISO codes, visit
    [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).
    """

    date: str
    """Date of holdings expressed in YYYY-MM-DD format.

    The fund-holdings endpoint will default to latest month-end close.
    """

    topn: str
    """
    Limits number of holdings or holders displayed by the top _n_ securities based
    on positions Market Value. Default is ALL, otherwise use number to limit number.
    """
