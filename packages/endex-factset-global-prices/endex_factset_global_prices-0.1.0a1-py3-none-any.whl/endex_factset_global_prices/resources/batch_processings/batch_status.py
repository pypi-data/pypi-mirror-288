# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.batch_processings import batch_status_retrieve_params
from ...types.batch_processings.batch_status_response import BatchStatusResponse

__all__ = ["BatchStatusResource", "AsyncBatchStatusResource"]


class BatchStatusResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatchStatusResourceWithRawResponse:
        return BatchStatusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchStatusResourceWithStreamingResponse:
        return BatchStatusResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BatchStatusResponse:
        """
        Return the status for the underlying batch request that is specified by the id.

        Args:
          id: Batch Request identifier.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-global-prices/v1/batch-status",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"id": id}, batch_status_retrieve_params.BatchStatusRetrieveParams),
            ),
            cast_to=BatchStatusResponse,
        )


class AsyncBatchStatusResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatchStatusResourceWithRawResponse:
        return AsyncBatchStatusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchStatusResourceWithStreamingResponse:
        return AsyncBatchStatusResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BatchStatusResponse:
        """
        Return the status for the underlying batch request that is specified by the id.

        Args:
          id: Batch Request identifier.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-global-prices/v1/batch-status",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"id": id}, batch_status_retrieve_params.BatchStatusRetrieveParams),
            ),
            cast_to=BatchStatusResponse,
        )


class BatchStatusResourceWithRawResponse:
    def __init__(self, batch_status: BatchStatusResource) -> None:
        self._batch_status = batch_status

        self.retrieve = to_raw_response_wrapper(
            batch_status.retrieve,
        )


class AsyncBatchStatusResourceWithRawResponse:
    def __init__(self, batch_status: AsyncBatchStatusResource) -> None:
        self._batch_status = batch_status

        self.retrieve = async_to_raw_response_wrapper(
            batch_status.retrieve,
        )


class BatchStatusResourceWithStreamingResponse:
    def __init__(self, batch_status: BatchStatusResource) -> None:
        self._batch_status = batch_status

        self.retrieve = to_streamed_response_wrapper(
            batch_status.retrieve,
        )


class AsyncBatchStatusResourceWithStreamingResponse:
    def __init__(self, batch_status: AsyncBatchStatusResource) -> None:
        self._batch_status = batch_status

        self.retrieve = async_to_streamed_response_wrapper(
            batch_status.retrieve,
        )
