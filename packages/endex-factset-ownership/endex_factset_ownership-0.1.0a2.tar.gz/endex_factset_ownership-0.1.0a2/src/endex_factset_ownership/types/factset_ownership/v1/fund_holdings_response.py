# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["FundHoldingsResponse", "Data"]


class Data(BaseModel):
    adj_holding: Optional[float] = FieldInfo(alias="adjHolding", default=None)
    """Adjusted number of shares held.

    All positions and prices are adjusted for splits and name changes, but they are
    not adjusted for spinoffs or mergers. If a given company announces a split
    today, FactSet's Ownership data will reflect that split either tomorrow or the
    day after, depending upon the time in which the FactSet Symbology team makes
    record of the change. For more details, visit
    [Online Assistant Page #11262](https://oa.apps.factset.com/pages/11262).
    """

    adj_market_value: Optional[float] = FieldInfo(alias="adjMarketValue", default=None)
    """Adjusted market values of shares held.

    Market Value. All positions and prices are adjusted for splits and name changes,
    but they are not adjusted for spinoffs or mergers. If a given company announces
    a split today, FactSet's Ownership data will reflect that split either tomorrow
    or the day after, depending upon the time in which the FactSet Symbology team
    makes record of the change. For more details, visit
    [Online Assistant Page #11262](https://oa.apps.factset.com/pages/11262).
    """

    currency: Optional[str] = None
    """Currency code.

    The service will default to the funds local currency. For a list of currency ISO
    codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    date: Optional[datetime.date] = None
    """Date of the reported holding in YYYY-MM-DD format.

    For more details, visit
    [Online Assistant Page #11262](https://oa.apps.factset.com/pages/11262).
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Security Identifier of Fund.

    Identifies the security level id of the Fund requested (not-representing the
    underlying holding). Six alpha-numeric characters, excluding vowels, with an -S
    suffix (XXXXXX-S). All equity and fixed income securities that exist on FactSet
    are allocated a security-level permanent identifier.
    """

    fsym_regional_id: Optional[str] = FieldInfo(alias="fsymRegionalId", default=None)
    """FactSet Regional Security identifier of the security held in the fund."""

    fsym_security_id: Optional[str] = FieldInfo(alias="fsymSecurityId", default=None)
    """Represents the security id for the underlying holding, not the parent holding.

    Six alpha-numeric characters, excluding vowels, with an -S suffix (XXXXXX-S).
    All equity and fixed income securities that exist on FactSet are allocated a
    security-level permanent identifier.
    """

    issue_type: Optional[str] = FieldInfo(alias="issueType", default=None)
    """Issue type of held security.

    For more details, visit
    [Online Assistant Page #11262](https://oa.apps.factset.com/pages/11262).
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Fund Identifier that was used in the request."""

    security_name: Optional[str] = FieldInfo(alias="securityName", default=None)
    """Name of held security."""

    security_ticker: Optional[str] = FieldInfo(alias="securityTicker", default=None)
    """Ticker of held security."""

    weight_close: Optional[float] = FieldInfo(alias="weightClose", default=None)
    """Closing weight of security in the fund for the requested asset type (percent)."""


class FundHoldingsResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Fund holdings"""
