# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .v1 import (
    V1Resource,
    AsyncV1Resource,
    V1ResourceWithRawResponse,
    AsyncV1ResourceWithRawResponse,
    V1ResourceWithStreamingResponse,
    AsyncV1ResourceWithStreamingResponse,
)
from .v1.v1 import V1Resource, AsyncV1Resource
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["FactsetOwnershipResource", "AsyncFactsetOwnershipResource"]


class FactsetOwnershipResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> FactsetOwnershipResourceWithRawResponse:
        return FactsetOwnershipResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FactsetOwnershipResourceWithStreamingResponse:
        return FactsetOwnershipResourceWithStreamingResponse(self)


class AsyncFactsetOwnershipResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFactsetOwnershipResourceWithRawResponse:
        return AsyncFactsetOwnershipResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFactsetOwnershipResourceWithStreamingResponse:
        return AsyncFactsetOwnershipResourceWithStreamingResponse(self)


class FactsetOwnershipResourceWithRawResponse:
    def __init__(self, factset_ownership: FactsetOwnershipResource) -> None:
        self._factset_ownership = factset_ownership

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._factset_ownership.v1)


class AsyncFactsetOwnershipResourceWithRawResponse:
    def __init__(self, factset_ownership: AsyncFactsetOwnershipResource) -> None:
        self._factset_ownership = factset_ownership

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._factset_ownership.v1)


class FactsetOwnershipResourceWithStreamingResponse:
    def __init__(self, factset_ownership: FactsetOwnershipResource) -> None:
        self._factset_ownership = factset_ownership

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._factset_ownership.v1)


class AsyncFactsetOwnershipResourceWithStreamingResponse:
    def __init__(self, factset_ownership: AsyncFactsetOwnershipResource) -> None:
        self._factset_ownership = factset_ownership

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._factset_ownership.v1)
