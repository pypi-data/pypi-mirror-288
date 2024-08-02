# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .fund_holdings import (
    FundHoldingsResource,
    AsyncFundHoldingsResource,
    FundHoldingsResourceWithRawResponse,
    AsyncFundHoldingsResourceWithRawResponse,
    FundHoldingsResourceWithStreamingResponse,
    AsyncFundHoldingsResourceWithStreamingResponse,
)
from .security_holders import (
    SecurityHoldersResource,
    AsyncSecurityHoldersResource,
    SecurityHoldersResourceWithRawResponse,
    AsyncSecurityHoldersResourceWithRawResponse,
    SecurityHoldersResourceWithStreamingResponse,
    AsyncSecurityHoldersResourceWithStreamingResponse,
)

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def fund_holdings(self) -> FundHoldingsResource:
        return FundHoldingsResource(self._client)

    @cached_property
    def security_holders(self) -> SecurityHoldersResource:
        return SecurityHoldersResource(self._client)

    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self)


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def fund_holdings(self) -> AsyncFundHoldingsResource:
        return AsyncFundHoldingsResource(self._client)

    @cached_property
    def security_holders(self) -> AsyncSecurityHoldersResource:
        return AsyncSecurityHoldersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self)


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

    @cached_property
    def fund_holdings(self) -> FundHoldingsResourceWithRawResponse:
        return FundHoldingsResourceWithRawResponse(self._v1.fund_holdings)

    @cached_property
    def security_holders(self) -> SecurityHoldersResourceWithRawResponse:
        return SecurityHoldersResourceWithRawResponse(self._v1.security_holders)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

    @cached_property
    def fund_holdings(self) -> AsyncFundHoldingsResourceWithRawResponse:
        return AsyncFundHoldingsResourceWithRawResponse(self._v1.fund_holdings)

    @cached_property
    def security_holders(self) -> AsyncSecurityHoldersResourceWithRawResponse:
        return AsyncSecurityHoldersResourceWithRawResponse(self._v1.security_holders)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

    @cached_property
    def fund_holdings(self) -> FundHoldingsResourceWithStreamingResponse:
        return FundHoldingsResourceWithStreamingResponse(self._v1.fund_holdings)

    @cached_property
    def security_holders(self) -> SecurityHoldersResourceWithStreamingResponse:
        return SecurityHoldersResourceWithStreamingResponse(self._v1.security_holders)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

    @cached_property
    def fund_holdings(self) -> AsyncFundHoldingsResourceWithStreamingResponse:
        return AsyncFundHoldingsResourceWithStreamingResponse(self._v1.fund_holdings)

    @cached_property
    def security_holders(self) -> AsyncSecurityHoldersResourceWithStreamingResponse:
        return AsyncSecurityHoldersResourceWithStreamingResponse(self._v1.security_holders)
