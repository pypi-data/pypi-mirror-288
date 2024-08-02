# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SecurityHolderCreateParams"]


class SecurityHolderCreateParams(TypedDict, total=False):
    ids: Required[List[str]]
    """Security Requested for Holders information."""

    currency: str
    """Currency code for adjusting prices.

    Default is Local. For a list of currency ISO codes, visit
    [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).
    """

    date: str
    """Date of holdings expressed in YYYY-MM-DD format."""

    holder_type: Annotated[Literal["F", "M", "S", "FS", "B"], PropertyInfo(alias="holderType")]
    """Controls the Holder Type of the data returned.

    By default, the service will return Institutional Holders. Requesting All
    Holders is not currently supported. Only a single Holder Type is allowed per
    request.

    - **F** = Institutions
    - **M** = Mutual Funds
    - **S** = Insiders/Stakeholders
    - **FS** = Institutions/Insiders
    - **B** = Beneficial Owners
    """

    topn: str
    """Limits number of holdings or holders displayed by the top _n_ securities.

    Default is ALL, or use integer to limit number.
    """
