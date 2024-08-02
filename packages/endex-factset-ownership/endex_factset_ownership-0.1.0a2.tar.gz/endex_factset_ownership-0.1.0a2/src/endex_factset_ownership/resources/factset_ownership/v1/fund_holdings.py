# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.factset_ownership.v1 import fund_holding_list_params, fund_holding_create_params
from ....types.factset_ownership.v1.fund_holdings_response import FundHoldingsResponse

__all__ = ["FundHoldingsResource", "AsyncFundHoldingsResource"]


class FundHoldingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FundHoldingsResourceWithRawResponse:
        return FundHoldingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FundHoldingsResourceWithStreamingResponse:
        return FundHoldingsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        asset_type: Literal["ALL", "EQ", "FI"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundHoldingsResponse:
        """
        Gets Holding information for a long list of Fund objects.

        Args:
          ids: List of Fund identifiers.

          asset_type: Select type of assets returned, whereby EQ = Equity, FI = Fixed Income, and ALL
              = all asset types.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format.

          topn: Limits number of holdings or holders displayed by the top _n_ securities.
              Default is ALL, or use integer to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-ownership/v1/fund-holdings",
            body=maybe_transform(
                {
                    "ids": ids,
                    "asset_type": asset_type,
                    "currency": currency,
                    "date": date,
                    "topn": topn,
                },
                fund_holding_create_params.FundHoldingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FundHoldingsResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        asset_type: Literal["ALL", "EQ", "FI"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundHoldingsResponse:
        """Gets holdings information for list of fund identifiers.

        The service allows you
        to filter by the TopN holdings and Asset Type.

        Args:
          ids: List of requested fund identifiers. <p>**\\**ids limit** = 10 per request\\**</p>

          asset_type: Filter holdings by the following major asset classes -

              - **EQ** = Equity
              - **FI** = Fixed Income
              - **ALL** = ALL

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format. The fund-holdings endpoint will
              default to latest month-end close.

          topn: Limits number of holdings or holders displayed by the top _n_ securities based
              on positions Market Value. Default is ALL, otherwise use number to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-ownership/v1/fund-holdings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "asset_type": asset_type,
                        "currency": currency,
                        "date": date,
                        "topn": topn,
                    },
                    fund_holding_list_params.FundHoldingListParams,
                ),
            ),
            cast_to=FundHoldingsResponse,
        )


class AsyncFundHoldingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFundHoldingsResourceWithRawResponse:
        return AsyncFundHoldingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFundHoldingsResourceWithStreamingResponse:
        return AsyncFundHoldingsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        asset_type: Literal["ALL", "EQ", "FI"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundHoldingsResponse:
        """
        Gets Holding information for a long list of Fund objects.

        Args:
          ids: List of Fund identifiers.

          asset_type: Select type of assets returned, whereby EQ = Equity, FI = Fixed Income, and ALL
              = all asset types.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format.

          topn: Limits number of holdings or holders displayed by the top _n_ securities.
              Default is ALL, or use integer to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-ownership/v1/fund-holdings",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "asset_type": asset_type,
                    "currency": currency,
                    "date": date,
                    "topn": topn,
                },
                fund_holding_create_params.FundHoldingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FundHoldingsResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        asset_type: Literal["ALL", "EQ", "FI"] | NotGiven = NOT_GIVEN,
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FundHoldingsResponse:
        """Gets holdings information for list of fund identifiers.

        The service allows you
        to filter by the TopN holdings and Asset Type.

        Args:
          ids: List of requested fund identifiers. <p>**\\**ids limit** = 10 per request\\**</p>

          asset_type: Filter holdings by the following major asset classes -

              - **EQ** = Equity
              - **FI** = Fixed Income
              - **ALL** = ALL

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format. The fund-holdings endpoint will
              default to latest month-end close.

          topn: Limits number of holdings or holders displayed by the top _n_ securities based
              on positions Market Value. Default is ALL, otherwise use number to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-ownership/v1/fund-holdings",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "asset_type": asset_type,
                        "currency": currency,
                        "date": date,
                        "topn": topn,
                    },
                    fund_holding_list_params.FundHoldingListParams,
                ),
            ),
            cast_to=FundHoldingsResponse,
        )


class FundHoldingsResourceWithRawResponse:
    def __init__(self, fund_holdings: FundHoldingsResource) -> None:
        self._fund_holdings = fund_holdings

        self.create = to_raw_response_wrapper(
            fund_holdings.create,
        )
        self.list = to_raw_response_wrapper(
            fund_holdings.list,
        )


class AsyncFundHoldingsResourceWithRawResponse:
    def __init__(self, fund_holdings: AsyncFundHoldingsResource) -> None:
        self._fund_holdings = fund_holdings

        self.create = async_to_raw_response_wrapper(
            fund_holdings.create,
        )
        self.list = async_to_raw_response_wrapper(
            fund_holdings.list,
        )


class FundHoldingsResourceWithStreamingResponse:
    def __init__(self, fund_holdings: FundHoldingsResource) -> None:
        self._fund_holdings = fund_holdings

        self.create = to_streamed_response_wrapper(
            fund_holdings.create,
        )
        self.list = to_streamed_response_wrapper(
            fund_holdings.list,
        )


class AsyncFundHoldingsResourceWithStreamingResponse:
    def __init__(self, fund_holdings: AsyncFundHoldingsResource) -> None:
        self._fund_holdings = fund_holdings

        self.create = async_to_streamed_response_wrapper(
            fund_holdings.create,
        )
        self.list = async_to_streamed_response_wrapper(
            fund_holdings.list,
        )
