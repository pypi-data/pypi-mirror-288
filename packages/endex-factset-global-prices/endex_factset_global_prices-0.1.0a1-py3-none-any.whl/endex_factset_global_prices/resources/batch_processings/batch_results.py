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
from ...types.batch_processings import batch_result_retrieve_params
from ...types.batch_processings.batch_result_response import BatchResultResponse

__all__ = ["BatchResultsResource", "AsyncBatchResultsResource"]


class BatchResultsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatchResultsResourceWithRawResponse:
        return BatchResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchResultsResourceWithStreamingResponse:
        return BatchResultsResourceWithStreamingResponse(self)

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
    ) -> BatchResultResponse:
        """
        Returns the response data for the underlying batch request that is specified by
        the id.

        By default, this endpoint will return data as JSON. If you wish to receive your
        data in CSV format, you can edit the header to have the "accept" parameter as
        "text/csv" instead of "application/json".

        Args:
          id: Batch Request identifier.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/factset-global-prices/v1/batch-result",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"id": id}, batch_result_retrieve_params.BatchResultRetrieveParams),
            ),
            cast_to=BatchResultResponse,
        )


class AsyncBatchResultsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatchResultsResourceWithRawResponse:
        return AsyncBatchResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchResultsResourceWithStreamingResponse:
        return AsyncBatchResultsResourceWithStreamingResponse(self)

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
    ) -> BatchResultResponse:
        """
        Returns the response data for the underlying batch request that is specified by
        the id.

        By default, this endpoint will return data as JSON. If you wish to receive your
        data in CSV format, you can edit the header to have the "accept" parameter as
        "text/csv" instead of "application/json".

        Args:
          id: Batch Request identifier.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/factset-global-prices/v1/batch-result",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"id": id}, batch_result_retrieve_params.BatchResultRetrieveParams),
            ),
            cast_to=BatchResultResponse,
        )


class BatchResultsResourceWithRawResponse:
    def __init__(self, batch_results: BatchResultsResource) -> None:
        self._batch_results = batch_results

        self.retrieve = to_raw_response_wrapper(
            batch_results.retrieve,
        )


class AsyncBatchResultsResourceWithRawResponse:
    def __init__(self, batch_results: AsyncBatchResultsResource) -> None:
        self._batch_results = batch_results

        self.retrieve = async_to_raw_response_wrapper(
            batch_results.retrieve,
        )


class BatchResultsResourceWithStreamingResponse:
    def __init__(self, batch_results: BatchResultsResource) -> None:
        self._batch_results = batch_results

        self.retrieve = to_streamed_response_wrapper(
            batch_results.retrieve,
        )


class AsyncBatchResultsResourceWithStreamingResponse:
    def __init__(self, batch_results: AsyncBatchResultsResource) -> None:
        self._batch_results = batch_results

        self.retrieve = async_to_streamed_response_wrapper(
            batch_results.retrieve,
        )
