# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from endex_factset_mergers_and_acquisitions import (
    EndexFactsetMergersAndAcquisitions,
    AsyncEndexFactsetMergersAndAcquisitions,
)
from endex_factset_mergers_and_acquisitions.types import (
    DealsResponse,
    DetailsResponse,
    DealsPublicResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeals:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_by_company(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        deal = client.deals.by_company(
            data={"ids": ["IBM-US"]},
        )
        assert_matches_type(DealsResponse, deal, path=["response"])

    @parametrize
    def test_method_by_company_with_all_params(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        deal = client.deals.by_company(
            data={
                "ids": ["IBM-US"],
                "start_date": "2023-10-30",
                "end_date": "2023-12-31",
            },
        )
        assert_matches_type(DealsResponse, deal, path=["response"])

    @parametrize
    def test_raw_response_by_company(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        response = client.deals.with_raw_response.by_company(
            data={"ids": ["IBM-US"]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deal = response.parse()
        assert_matches_type(DealsResponse, deal, path=["response"])

    @parametrize
    def test_streaming_response_by_company(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        with client.deals.with_streaming_response.by_company(
            data={"ids": ["IBM-US"]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deal = response.parse()
            assert_matches_type(DealsResponse, deal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_details(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        deal = client.deals.details(
            data={"deal_ids": ["4143886MM"]},
        )
        assert_matches_type(DetailsResponse, deal, path=["response"])

    @parametrize
    def test_raw_response_details(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        response = client.deals.with_raw_response.details(
            data={"deal_ids": ["4143886MM"]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deal = response.parse()
        assert_matches_type(DetailsResponse, deal, path=["response"])

    @parametrize
    def test_streaming_response_details(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        with client.deals.with_streaming_response.details(
            data={"deal_ids": ["4143886MM"]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deal = response.parse()
            assert_matches_type(DetailsResponse, deal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_public_targets(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        deal = client.deals.public_targets(
            data={},
        )
        assert_matches_type(DealsPublicResponse, deal, path=["response"])

    @parametrize
    def test_method_public_targets_with_all_params(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        deal = client.deals.public_targets(
            data={
                "start_date": "2023-10-30",
                "end_date": "2023-12-31",
                "status": "All",
            },
        )
        assert_matches_type(DealsPublicResponse, deal, path=["response"])

    @parametrize
    def test_raw_response_public_targets(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        response = client.deals.with_raw_response.public_targets(
            data={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deal = response.parse()
        assert_matches_type(DealsPublicResponse, deal, path=["response"])

    @parametrize
    def test_streaming_response_public_targets(self, client: EndexFactsetMergersAndAcquisitions) -> None:
        with client.deals.with_streaming_response.public_targets(
            data={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deal = response.parse()
            assert_matches_type(DealsPublicResponse, deal, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDeals:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_by_company(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        deal = await async_client.deals.by_company(
            data={"ids": ["IBM-US"]},
        )
        assert_matches_type(DealsResponse, deal, path=["response"])

    @parametrize
    async def test_method_by_company_with_all_params(
        self, async_client: AsyncEndexFactsetMergersAndAcquisitions
    ) -> None:
        deal = await async_client.deals.by_company(
            data={
                "ids": ["IBM-US"],
                "start_date": "2023-10-30",
                "end_date": "2023-12-31",
            },
        )
        assert_matches_type(DealsResponse, deal, path=["response"])

    @parametrize
    async def test_raw_response_by_company(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        response = await async_client.deals.with_raw_response.by_company(
            data={"ids": ["IBM-US"]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deal = await response.parse()
        assert_matches_type(DealsResponse, deal, path=["response"])

    @parametrize
    async def test_streaming_response_by_company(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        async with async_client.deals.with_streaming_response.by_company(
            data={"ids": ["IBM-US"]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deal = await response.parse()
            assert_matches_type(DealsResponse, deal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_details(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        deal = await async_client.deals.details(
            data={"deal_ids": ["4143886MM"]},
        )
        assert_matches_type(DetailsResponse, deal, path=["response"])

    @parametrize
    async def test_raw_response_details(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        response = await async_client.deals.with_raw_response.details(
            data={"deal_ids": ["4143886MM"]},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deal = await response.parse()
        assert_matches_type(DetailsResponse, deal, path=["response"])

    @parametrize
    async def test_streaming_response_details(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        async with async_client.deals.with_streaming_response.details(
            data={"deal_ids": ["4143886MM"]},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deal = await response.parse()
            assert_matches_type(DetailsResponse, deal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_public_targets(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        deal = await async_client.deals.public_targets(
            data={},
        )
        assert_matches_type(DealsPublicResponse, deal, path=["response"])

    @parametrize
    async def test_method_public_targets_with_all_params(
        self, async_client: AsyncEndexFactsetMergersAndAcquisitions
    ) -> None:
        deal = await async_client.deals.public_targets(
            data={
                "start_date": "2023-10-30",
                "end_date": "2023-12-31",
                "status": "All",
            },
        )
        assert_matches_type(DealsPublicResponse, deal, path=["response"])

    @parametrize
    async def test_raw_response_public_targets(self, async_client: AsyncEndexFactsetMergersAndAcquisitions) -> None:
        response = await async_client.deals.with_raw_response.public_targets(
            data={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deal = await response.parse()
        assert_matches_type(DealsPublicResponse, deal, path=["response"])

    @parametrize
    async def test_streaming_response_public_targets(
        self, async_client: AsyncEndexFactsetMergersAndAcquisitions
    ) -> None:
        async with async_client.deals.with_streaming_response.public_targets(
            data={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deal = await response.parse()
            assert_matches_type(DealsPublicResponse, deal, path=["response"])

        assert cast(Any, response.is_closed) is True
