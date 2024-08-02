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
from ....types.factset_ownership.v1 import security_holder_list_params, security_holder_create_params
from ....types.factset_ownership.v1.security_holders_response import SecurityHoldersResponse

__all__ = ["SecurityHoldersResource", "AsyncSecurityHoldersResource"]


class SecurityHoldersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SecurityHoldersResourceWithRawResponse:
        return SecurityHoldersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SecurityHoldersResourceWithStreamingResponse:
        return SecurityHoldersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        ids: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        holder_type: Literal["F", "M", "S", "FS", "B"] | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SecurityHoldersResponse:
        """
        Gets security ownership details and activity for the requested security
        identifiers. The services allows filtering by "Topn" holders and by holder
        "type", such as Institutions, Insiders, and Stakeholders.

        Args:
          ids: Security Requested for Holders information.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format.

          holder_type: Controls the Holder Type of the data returned. By default, the service will
              return Institutional Holders. Requesting All Holders is not currently supported.
              Only a single Holder Type is allowed per request.

              - **F** = Institutions
              - **M** = Mutual Funds
              - **S** = Insiders/Stakeholders
              - **FS** = Institutions/Insiders
              - **B** = Beneficial Owners

          topn: Limits number of holdings or holders displayed by the top _n_ securities.
              Default is ALL, or use integer to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/factset-ownership/v1/security-holders",
            body=maybe_transform(
                {
                    "ids": ids,
                    "currency": currency,
                    "date": date,
                    "holder_type": holder_type,
                    "topn": topn,
                },
                security_holder_create_params.SecurityHolderCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SecurityHoldersResponse,
        )

    def list(
        self,
        *,
        ids: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        holder_type: Literal["F", "M", "S", "FS", "B"] | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SecurityHoldersResponse:
        """
        Gets security ownership details and activity for the requested security
        identifiers. The services allows filtering by "Topn" holders and by holder
        "type", such as Institutions, Insiders, and Stakeholders.

        Args:
          ids: Requested list of security identifiers. <p>**\\**ids limit** = 1 per
              request\\**</p>.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format. The fund-holdings endpoint will
              default to latest month-end close.

          holder_type: Controls the Holder Type of the data returned. By default, the service will
              return Institutional Holders. Requesting All Holders is not currently supported.
              Only a single Holder Type is allowed per request.

              - **F** = Institutions
              - **M** = Mutual Funds
              - **S** = Insiders/Stakeholders
              - **FS** = Institutions/Insiders
              - **B** = Beneficial Owners

          topn: Limits number of holdings or holders displayed by the top _n_ securities based
              on positions Market Value. Default is ALL, otherwise use number to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-ownership/v1/security-holders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "currency": currency,
                        "date": date,
                        "holder_type": holder_type,
                        "topn": topn,
                    },
                    security_holder_list_params.SecurityHolderListParams,
                ),
            ),
            cast_to=SecurityHoldersResponse,
        )


class AsyncSecurityHoldersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSecurityHoldersResourceWithRawResponse:
        return AsyncSecurityHoldersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSecurityHoldersResourceWithStreamingResponse:
        return AsyncSecurityHoldersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        ids: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        holder_type: Literal["F", "M", "S", "FS", "B"] | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SecurityHoldersResponse:
        """
        Gets security ownership details and activity for the requested security
        identifiers. The services allows filtering by "Topn" holders and by holder
        "type", such as Institutions, Insiders, and Stakeholders.

        Args:
          ids: Security Requested for Holders information.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format.

          holder_type: Controls the Holder Type of the data returned. By default, the service will
              return Institutional Holders. Requesting All Holders is not currently supported.
              Only a single Holder Type is allowed per request.

              - **F** = Institutions
              - **M** = Mutual Funds
              - **S** = Insiders/Stakeholders
              - **FS** = Institutions/Insiders
              - **B** = Beneficial Owners

          topn: Limits number of holdings or holders displayed by the top _n_ securities.
              Default is ALL, or use integer to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/factset-ownership/v1/security-holders",
            body=await async_maybe_transform(
                {
                    "ids": ids,
                    "currency": currency,
                    "date": date,
                    "holder_type": holder_type,
                    "topn": topn,
                },
                security_holder_create_params.SecurityHolderCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SecurityHoldersResponse,
        )

    async def list(
        self,
        *,
        ids: List[str],
        currency: str | NotGiven = NOT_GIVEN,
        date: str | NotGiven = NOT_GIVEN,
        holder_type: Literal["F", "M", "S", "FS", "B"] | NotGiven = NOT_GIVEN,
        topn: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SecurityHoldersResponse:
        """
        Gets security ownership details and activity for the requested security
        identifiers. The services allows filtering by "Topn" holders and by holder
        "type", such as Institutions, Insiders, and Stakeholders.

        Args:
          ids: Requested list of security identifiers. <p>**\\**ids limit** = 1 per
              request\\**</p>.

          currency: Currency code for adjusting prices. Default is Local. For a list of currency ISO
              codes, visit
              [Online Assistant Page 1470](https://oa.apps.factset.com/pages/1470).

          date: Date of holdings expressed in YYYY-MM-DD format. The fund-holdings endpoint will
              default to latest month-end close.

          holder_type: Controls the Holder Type of the data returned. By default, the service will
              return Institutional Holders. Requesting All Holders is not currently supported.
              Only a single Holder Type is allowed per request.

              - **F** = Institutions
              - **M** = Mutual Funds
              - **S** = Insiders/Stakeholders
              - **FS** = Institutions/Insiders
              - **B** = Beneficial Owners

          topn: Limits number of holdings or holders displayed by the top _n_ securities based
              on positions Market Value. Default is ALL, otherwise use number to limit number.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-ownership/v1/security-holders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "currency": currency,
                        "date": date,
                        "holder_type": holder_type,
                        "topn": topn,
                    },
                    security_holder_list_params.SecurityHolderListParams,
                ),
            ),
            cast_to=SecurityHoldersResponse,
        )


class SecurityHoldersResourceWithRawResponse:
    def __init__(self, security_holders: SecurityHoldersResource) -> None:
        self._security_holders = security_holders

        self.create = to_raw_response_wrapper(
            security_holders.create,
        )
        self.list = to_raw_response_wrapper(
            security_holders.list,
        )


class AsyncSecurityHoldersResourceWithRawResponse:
    def __init__(self, security_holders: AsyncSecurityHoldersResource) -> None:
        self._security_holders = security_holders

        self.create = async_to_raw_response_wrapper(
            security_holders.create,
        )
        self.list = async_to_raw_response_wrapper(
            security_holders.list,
        )


class SecurityHoldersResourceWithStreamingResponse:
    def __init__(self, security_holders: SecurityHoldersResource) -> None:
        self._security_holders = security_holders

        self.create = to_streamed_response_wrapper(
            security_holders.create,
        )
        self.list = to_streamed_response_wrapper(
            security_holders.list,
        )


class AsyncSecurityHoldersResourceWithStreamingResponse:
    def __init__(self, security_holders: AsyncSecurityHoldersResource) -> None:
        self._security_holders = security_holders

        self.create = async_to_streamed_response_wrapper(
            security_holders.create,
        )
        self.list = async_to_streamed_response_wrapper(
            security_holders.list,
        )
