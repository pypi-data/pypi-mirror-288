# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import datetime
from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SecurityHoldersResponse", "Data"]


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

    The service will default to the local currency if the currency is not requested.
    For a list of currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    date: Optional[datetime.date] = None
    """Date of the reported holding in YYYY-MM-DD format.

    For more details regarding date resolution, visit
    [Online Assistant Page #11262](https://oa.apps.factset.com/pages/11262).
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Security Identifier of security requested.

    This does not represent the FactSet permanent identifier for the holder, but
    rather the requested id. Six alpha-numeric characters, excluding vowels, with an
    -S suffix (XXXXXX-S). All equity and fixed income securities that exist on
    FactSet are allocated a security-level permanent identifier.
    """

    holder_entity_id: Optional[str] = FieldInfo(alias="holderEntityId", default=None)
    """FactSet Entity ID that corresponds to the specified holder ID."""

    holder_id: Optional[str] = FieldInfo(alias="holderId", default=None)
    """FactSet Ownership Holders ID that corresponds to the requested security holder."""

    holder_name: Optional[str] = FieldInfo(alias="holderName", default=None)
    """Name of the holder for the requested security identifier."""

    holder_type: Optional[str] = FieldInfo(alias="holderType", default=None)
    """Holder Type name of the respective holder object.

    The name will align to the holderType requested.
    """

    investor_type: Optional[str] = FieldInfo(alias="investorType", default=None)
    """
    FactSet Ownership Institution, Mutual Fund, and Insider/Stakeholder investor
    types. To learn more about the different investor types, visit
    [Online Assistant Page #11656](https://my.apps.factset.com/oa/pages/11656).
    """

    percent_outstanding: Optional[float] = FieldInfo(alias="percentOutstanding", default=None)
    """
    The percent of the outstanding common shares held by a particular filing
    institution. To learn more, visit
    [Online Assistant Page #11041](https://my.apps.factset.com/oa/pages/11041).
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Security Identifier that was used in the request."""

    source: Optional[str] = None
    """
    Either the 13F Form or ND-30D report filed where the security holdings data was
    sourced from. To learn more about source, please visit
    https://my.apps.factset.com/oa/pages/11260
    """

    weight_close: Optional[float] = FieldInfo(alias="weightClose", default=None)
    """
    "Closing weight of the security for the holders of the requested security
    (percent). To learn more about how ownership weight is calculated please visit
    [Online Assistant Page #11247](https://my.apps.factset.com/oa/pages/11247)."
    """


class SecurityHoldersResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Array of Security Holders"""
