# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["FundHoldingCreateParams"]


class FundHoldingCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """List of Fund identifiers."""

    asset_type: Annotated[Literal["ALL", "EQ", "FI"], PropertyInfo(alias="assetType")]
    """
    Select type of assets returned, whereby EQ = Equity, FI = Fixed Income, and ALL
    = all asset types.
    """

    currency: str
    """Currency code for adjusting prices.

    Default is Local. For a list of currency ISO codes, visit
    [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).
    """

    date: str
    """Date of holdings expressed in YYYY-MM-DD format."""

    topn: str
    """Limits number of holdings or holders displayed by the top _n_ securities.

    Default is ALL, or use integer to limit number.
    """
