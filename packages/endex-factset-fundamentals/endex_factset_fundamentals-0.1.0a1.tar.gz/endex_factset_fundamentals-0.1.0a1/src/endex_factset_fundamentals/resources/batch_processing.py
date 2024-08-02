# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import batch_processing_result_params, batch_processing_status_params
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
from ..types.batch_result_response import BatchResultResponse
from ..types.batch_status_response import BatchStatusResponse

__all__ = ["BatchProcessingResource", "AsyncBatchProcessingResource"]


class BatchProcessingResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatchProcessingResourceWithRawResponse:
        return BatchProcessingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchProcessingResourceWithStreamingResponse:
        return BatchProcessingResourceWithStreamingResponse(self)

    def result(
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
            "/batch-result",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"id": id}, batch_processing_result_params.BatchProcessingResultParams),
            ),
            cast_to=BatchResultResponse,
        )

    def status(
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
            "/batch-status",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"id": id}, batch_processing_status_params.BatchProcessingStatusParams),
            ),
            cast_to=BatchStatusResponse,
        )


class AsyncBatchProcessingResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatchProcessingResourceWithRawResponse:
        return AsyncBatchProcessingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchProcessingResourceWithStreamingResponse:
        return AsyncBatchProcessingResourceWithStreamingResponse(self)

    async def result(
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
            "/batch-result",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"id": id}, batch_processing_result_params.BatchProcessingResultParams
                ),
            ),
            cast_to=BatchResultResponse,
        )

    async def status(
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
            "/batch-status",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"id": id}, batch_processing_status_params.BatchProcessingStatusParams
                ),
            ),
            cast_to=BatchStatusResponse,
        )


class BatchProcessingResourceWithRawResponse:
    def __init__(self, batch_processing: BatchProcessingResource) -> None:
        self._batch_processing = batch_processing

        self.result = to_raw_response_wrapper(
            batch_processing.result,
        )
        self.status = to_raw_response_wrapper(
            batch_processing.status,
        )


class AsyncBatchProcessingResourceWithRawResponse:
    def __init__(self, batch_processing: AsyncBatchProcessingResource) -> None:
        self._batch_processing = batch_processing

        self.result = async_to_raw_response_wrapper(
            batch_processing.result,
        )
        self.status = async_to_raw_response_wrapper(
            batch_processing.status,
        )


class BatchProcessingResourceWithStreamingResponse:
    def __init__(self, batch_processing: BatchProcessingResource) -> None:
        self._batch_processing = batch_processing

        self.result = to_streamed_response_wrapper(
            batch_processing.result,
        )
        self.status = to_streamed_response_wrapper(
            batch_processing.status,
        )


class AsyncBatchProcessingResourceWithStreamingResponse:
    def __init__(self, batch_processing: AsyncBatchProcessingResource) -> None:
        self._batch_processing = batch_processing

        self.result = async_to_streamed_response_wrapper(
            batch_processing.result,
        )
        self.status = async_to_streamed_response_wrapper(
            batch_processing.status,
        )
