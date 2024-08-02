# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import deal_details_params, deal_by_company_params, deal_public_targets_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.deals_response import DealsResponse
from ..types.details_response import DetailsResponse
from ..types.deals_public_response import DealsPublicResponse

__all__ = ["DealsResource", "AsyncDealsResource"]


class DealsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DealsResourceWithRawResponse:
        return DealsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DealsResourceWithStreamingResponse:
        return DealsResourceWithStreamingResponse(self)

    def by_company(
        self,
        *,
        data: deal_by_company_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DealsResponse:
        """Gets deals for a specified list of companies within a date range.

        Deals returned
        are any in which the requested company is involved as either the buyer, seller,
        or target. The start and end date parameters will find deals based on their
        announcement date. The response of this endpoint includes `dealId` which can be
        sent to the `/deals/details` endpoint for more information about the deal.

        Args:
          data: Deals Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/deals/by-company",
            body=maybe_transform({"data": data}, deal_by_company_params.DealByCompanyParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DealsResponse,
        )

    def details(
        self,
        *,
        data: deal_details_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailsResponse:
        """Gets deal details for a specified list of FactSet deal identifiers.

        Monetary
        values returned by this API are converted and represented in USD.

        Args:
          data: Details Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/deals/details",
            body=maybe_transform({"data": data}, deal_details_params.DealDetailsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DetailsResponse,
        )

    def public_targets(
        self,
        *,
        data: deal_public_targets_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DealsPublicResponse:
        """
        Gets deals in which the target is a public company for a specified date range
        and status. The start and end date parameters will find deals based on their
        announcement date. The response of this endpoint includes `dealId` which can be
        sent to the `/deals/details` endpoint for more information about the deal.

        Args:
          data: Deals Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/deals/public-targets",
            body=maybe_transform({"data": data}, deal_public_targets_params.DealPublicTargetsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DealsPublicResponse,
        )


class AsyncDealsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDealsResourceWithRawResponse:
        return AsyncDealsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDealsResourceWithStreamingResponse:
        return AsyncDealsResourceWithStreamingResponse(self)

    async def by_company(
        self,
        *,
        data: deal_by_company_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DealsResponse:
        """Gets deals for a specified list of companies within a date range.

        Deals returned
        are any in which the requested company is involved as either the buyer, seller,
        or target. The start and end date parameters will find deals based on their
        announcement date. The response of this endpoint includes `dealId` which can be
        sent to the `/deals/details` endpoint for more information about the deal.

        Args:
          data: Deals Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/deals/by-company",
            body=await async_maybe_transform({"data": data}, deal_by_company_params.DealByCompanyParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DealsResponse,
        )

    async def details(
        self,
        *,
        data: deal_details_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DetailsResponse:
        """Gets deal details for a specified list of FactSet deal identifiers.

        Monetary
        values returned by this API are converted and represented in USD.

        Args:
          data: Details Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/deals/details",
            body=await async_maybe_transform({"data": data}, deal_details_params.DealDetailsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DetailsResponse,
        )

    async def public_targets(
        self,
        *,
        data: deal_public_targets_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DealsPublicResponse:
        """
        Gets deals in which the target is a public company for a specified date range
        and status. The start and end date parameters will find deals based on their
        announcement date. The response of this endpoint includes `dealId` which can be
        sent to the `/deals/details` endpoint for more information about the deal.

        Args:
          data: Deals Request Body

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/deals/public-targets",
            body=await async_maybe_transform({"data": data}, deal_public_targets_params.DealPublicTargetsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DealsPublicResponse,
        )


class DealsResourceWithRawResponse:
    def __init__(self, deals: DealsResource) -> None:
        self._deals = deals

        self.by_company = to_raw_response_wrapper(
            deals.by_company,
        )
        self.details = to_raw_response_wrapper(
            deals.details,
        )
        self.public_targets = to_raw_response_wrapper(
            deals.public_targets,
        )


class AsyncDealsResourceWithRawResponse:
    def __init__(self, deals: AsyncDealsResource) -> None:
        self._deals = deals

        self.by_company = async_to_raw_response_wrapper(
            deals.by_company,
        )
        self.details = async_to_raw_response_wrapper(
            deals.details,
        )
        self.public_targets = async_to_raw_response_wrapper(
            deals.public_targets,
        )


class DealsResourceWithStreamingResponse:
    def __init__(self, deals: DealsResource) -> None:
        self._deals = deals

        self.by_company = to_streamed_response_wrapper(
            deals.by_company,
        )
        self.details = to_streamed_response_wrapper(
            deals.details,
        )
        self.public_targets = to_streamed_response_wrapper(
            deals.public_targets,
        )


class AsyncDealsResourceWithStreamingResponse:
    def __init__(self, deals: AsyncDealsResource) -> None:
        self._deals = deals

        self.by_company = async_to_streamed_response_wrapper(
            deals.by_company,
        )
        self.details = async_to_streamed_response_wrapper(
            deals.details,
        )
        self.public_targets = async_to_streamed_response_wrapper(
            deals.public_targets,
        )
