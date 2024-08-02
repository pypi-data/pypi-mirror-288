# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .batch_status import (
    BatchStatusResource,
    AsyncBatchStatusResource,
    BatchStatusResourceWithRawResponse,
    AsyncBatchStatusResourceWithRawResponse,
    BatchStatusResourceWithStreamingResponse,
    AsyncBatchStatusResourceWithStreamingResponse,
)
from .batch_results import (
    BatchResultsResource,
    AsyncBatchResultsResource,
    BatchResultsResourceWithRawResponse,
    AsyncBatchResultsResourceWithRawResponse,
    BatchResultsResourceWithStreamingResponse,
    AsyncBatchResultsResourceWithStreamingResponse,
)

__all__ = ["BatchProcessingsResource", "AsyncBatchProcessingsResource"]


class BatchProcessingsResource(SyncAPIResource):
    @cached_property
    def batch_status(self) -> BatchStatusResource:
        return BatchStatusResource(self._client)

    @cached_property
    def batch_results(self) -> BatchResultsResource:
        return BatchResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> BatchProcessingsResourceWithRawResponse:
        return BatchProcessingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchProcessingsResourceWithStreamingResponse:
        return BatchProcessingsResourceWithStreamingResponse(self)


class AsyncBatchProcessingsResource(AsyncAPIResource):
    @cached_property
    def batch_status(self) -> AsyncBatchStatusResource:
        return AsyncBatchStatusResource(self._client)

    @cached_property
    def batch_results(self) -> AsyncBatchResultsResource:
        return AsyncBatchResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBatchProcessingsResourceWithRawResponse:
        return AsyncBatchProcessingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchProcessingsResourceWithStreamingResponse:
        return AsyncBatchProcessingsResourceWithStreamingResponse(self)


class BatchProcessingsResourceWithRawResponse:
    def __init__(self, batch_processings: BatchProcessingsResource) -> None:
        self._batch_processings = batch_processings

    @cached_property
    def batch_status(self) -> BatchStatusResourceWithRawResponse:
        return BatchStatusResourceWithRawResponse(self._batch_processings.batch_status)

    @cached_property
    def batch_results(self) -> BatchResultsResourceWithRawResponse:
        return BatchResultsResourceWithRawResponse(self._batch_processings.batch_results)


class AsyncBatchProcessingsResourceWithRawResponse:
    def __init__(self, batch_processings: AsyncBatchProcessingsResource) -> None:
        self._batch_processings = batch_processings

    @cached_property
    def batch_status(self) -> AsyncBatchStatusResourceWithRawResponse:
        return AsyncBatchStatusResourceWithRawResponse(self._batch_processings.batch_status)

    @cached_property
    def batch_results(self) -> AsyncBatchResultsResourceWithRawResponse:
        return AsyncBatchResultsResourceWithRawResponse(self._batch_processings.batch_results)


class BatchProcessingsResourceWithStreamingResponse:
    def __init__(self, batch_processings: BatchProcessingsResource) -> None:
        self._batch_processings = batch_processings

    @cached_property
    def batch_status(self) -> BatchStatusResourceWithStreamingResponse:
        return BatchStatusResourceWithStreamingResponse(self._batch_processings.batch_status)

    @cached_property
    def batch_results(self) -> BatchResultsResourceWithStreamingResponse:
        return BatchResultsResourceWithStreamingResponse(self._batch_processings.batch_results)


class AsyncBatchProcessingsResourceWithStreamingResponse:
    def __init__(self, batch_processings: AsyncBatchProcessingsResource) -> None:
        self._batch_processings = batch_processings

    @cached_property
    def batch_status(self) -> AsyncBatchStatusResourceWithStreamingResponse:
        return AsyncBatchStatusResourceWithStreamingResponse(self._batch_processings.batch_status)

    @cached_property
    def batch_results(self) -> AsyncBatchResultsResourceWithStreamingResponse:
        return AsyncBatchResultsResourceWithStreamingResponse(self._batch_processings.batch_results)
