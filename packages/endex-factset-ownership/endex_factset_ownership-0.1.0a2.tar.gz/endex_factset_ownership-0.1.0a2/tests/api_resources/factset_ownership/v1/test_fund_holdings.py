# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_ownership import EndexFactsetOwnership, AsyncEndexFactsetOwnership
from endex_factset_ownership.types.factset_ownership.v1 import (
    FundHoldingsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFundHoldings:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: EndexFactsetOwnership) -> None:
        fund_holding = client.factset_ownership.v1.fund_holdings.create(
            ids=["VTI-US"],
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: EndexFactsetOwnership) -> None:
        fund_holding = client.factset_ownership.v1.fund_holdings.create(
            ids=["VTI-US"],
            asset_type="EQ",
            currency="USD",
            date="2019-12-31",
            topn="topn",
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: EndexFactsetOwnership) -> None:
        response = client.factset_ownership.v1.fund_holdings.with_raw_response.create(
            ids=["VTI-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fund_holding = response.parse()
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: EndexFactsetOwnership) -> None:
        with client.factset_ownership.v1.fund_holdings.with_streaming_response.create(
            ids=["VTI-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fund_holding = response.parse()
            assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: EndexFactsetOwnership) -> None:
        fund_holding = client.factset_ownership.v1.fund_holdings.list(
            ids=["string"],
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: EndexFactsetOwnership) -> None:
        fund_holding = client.factset_ownership.v1.fund_holdings.list(
            ids=["string"],
            asset_type="ALL",
            currency="currency",
            date="date",
            topn="topn",
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: EndexFactsetOwnership) -> None:
        response = client.factset_ownership.v1.fund_holdings.with_raw_response.list(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fund_holding = response.parse()
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: EndexFactsetOwnership) -> None:
        with client.factset_ownership.v1.fund_holdings.with_streaming_response.list(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fund_holding = response.parse()
            assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFundHoldings:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEndexFactsetOwnership) -> None:
        fund_holding = await async_client.factset_ownership.v1.fund_holdings.create(
            ids=["VTI-US"],
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEndexFactsetOwnership) -> None:
        fund_holding = await async_client.factset_ownership.v1.fund_holdings.create(
            ids=["VTI-US"],
            asset_type="EQ",
            currency="USD",
            date="2019-12-31",
            topn="topn",
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEndexFactsetOwnership) -> None:
        response = await async_client.factset_ownership.v1.fund_holdings.with_raw_response.create(
            ids=["VTI-US"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fund_holding = await response.parse()
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEndexFactsetOwnership) -> None:
        async with async_client.factset_ownership.v1.fund_holdings.with_streaming_response.create(
            ids=["VTI-US"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fund_holding = await response.parse()
            assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncEndexFactsetOwnership) -> None:
        fund_holding = await async_client.factset_ownership.v1.fund_holdings.list(
            ids=["string"],
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEndexFactsetOwnership) -> None:
        fund_holding = await async_client.factset_ownership.v1.fund_holdings.list(
            ids=["string"],
            asset_type="ALL",
            currency="currency",
            date="date",
            topn="topn",
        )
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEndexFactsetOwnership) -> None:
        response = await async_client.factset_ownership.v1.fund_holdings.with_raw_response.list(
            ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fund_holding = await response.parse()
        assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEndexFactsetOwnership) -> None:
        async with async_client.factset_ownership.v1.fund_holdings.with_streaming_response.list(
            ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fund_holding = await response.parse()
            assert_matches_type(FundHoldingsResponse, fund_holding, path=["response"])

        assert cast(Any, response.is_closed) is True
