# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "EndexFactsetGlobalPrices",
    "AsyncEndexFactsetGlobalPrices",
    "Client",
    "AsyncClient",
]


class EndexFactsetGlobalPrices(SyncAPIClient):
    prices: resources.PricesResource
    corporate_actions: resources.CorporateActionsResource
    annualized_dividends: resources.AnnualizedDividendsResource
    returns: resources.ReturnsResource
    security_shares: resources.SecuritySharesResource
    batch_processings: resources.BatchProcessingsResource
    with_raw_response: EndexFactsetGlobalPricesWithRawResponse
    with_streaming_response: EndexFactsetGlobalPricesWithStreamedResponse

    # client options
    access_token: str

    def __init__(
        self,
        *,
        access_token: str,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous endex-factset-global-prices client instance."""
        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("ENDEX_FACTSET_GLOBAL_PRICES_BASE_URL")
        if base_url is None:
            base_url = f"https://api.factset.com/content"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.prices = resources.PricesResource(self)
        self.corporate_actions = resources.CorporateActionsResource(self)
        self.annualized_dividends = resources.AnnualizedDividendsResource(self)
        self.returns = resources.ReturnsResource(self)
        self.security_shares = resources.SecuritySharesResource(self)
        self.batch_processings = resources.BatchProcessingsResource(self)
        self.with_raw_response = EndexFactsetGlobalPricesWithRawResponse(self)
        self.with_streaming_response = EndexFactsetGlobalPricesWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncEndexFactsetGlobalPrices(AsyncAPIClient):
    prices: resources.AsyncPricesResource
    corporate_actions: resources.AsyncCorporateActionsResource
    annualized_dividends: resources.AsyncAnnualizedDividendsResource
    returns: resources.AsyncReturnsResource
    security_shares: resources.AsyncSecuritySharesResource
    batch_processings: resources.AsyncBatchProcessingsResource
    with_raw_response: AsyncEndexFactsetGlobalPricesWithRawResponse
    with_streaming_response: AsyncEndexFactsetGlobalPricesWithStreamedResponse

    # client options
    access_token: str

    def __init__(
        self,
        *,
        access_token: str,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async endex-factset-global-prices client instance."""
        self.access_token = access_token

        if base_url is None:
            base_url = os.environ.get("ENDEX_FACTSET_GLOBAL_PRICES_BASE_URL")
        if base_url is None:
            base_url = f"https://api.factset.com/content"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.prices = resources.AsyncPricesResource(self)
        self.corporate_actions = resources.AsyncCorporateActionsResource(self)
        self.annualized_dividends = resources.AsyncAnnualizedDividendsResource(self)
        self.returns = resources.AsyncReturnsResource(self)
        self.security_shares = resources.AsyncSecuritySharesResource(self)
        self.batch_processings = resources.AsyncBatchProcessingsResource(self)
        self.with_raw_response = AsyncEndexFactsetGlobalPricesWithRawResponse(self)
        self.with_streaming_response = AsyncEndexFactsetGlobalPricesWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        access_token = self.access_token
        return {"Authorization": f"Bearer {access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            access_token=access_token or self.access_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class EndexFactsetGlobalPricesWithRawResponse:
    def __init__(self, client: EndexFactsetGlobalPrices) -> None:
        self.prices = resources.PricesResourceWithRawResponse(client.prices)
        self.corporate_actions = resources.CorporateActionsResourceWithRawResponse(client.corporate_actions)
        self.annualized_dividends = resources.AnnualizedDividendsResourceWithRawResponse(client.annualized_dividends)
        self.returns = resources.ReturnsResourceWithRawResponse(client.returns)
        self.security_shares = resources.SecuritySharesResourceWithRawResponse(client.security_shares)
        self.batch_processings = resources.BatchProcessingsResourceWithRawResponse(client.batch_processings)


class AsyncEndexFactsetGlobalPricesWithRawResponse:
    def __init__(self, client: AsyncEndexFactsetGlobalPrices) -> None:
        self.prices = resources.AsyncPricesResourceWithRawResponse(client.prices)
        self.corporate_actions = resources.AsyncCorporateActionsResourceWithRawResponse(client.corporate_actions)
        self.annualized_dividends = resources.AsyncAnnualizedDividendsResourceWithRawResponse(
            client.annualized_dividends
        )
        self.returns = resources.AsyncReturnsResourceWithRawResponse(client.returns)
        self.security_shares = resources.AsyncSecuritySharesResourceWithRawResponse(client.security_shares)
        self.batch_processings = resources.AsyncBatchProcessingsResourceWithRawResponse(client.batch_processings)


class EndexFactsetGlobalPricesWithStreamedResponse:
    def __init__(self, client: EndexFactsetGlobalPrices) -> None:
        self.prices = resources.PricesResourceWithStreamingResponse(client.prices)
        self.corporate_actions = resources.CorporateActionsResourceWithStreamingResponse(client.corporate_actions)
        self.annualized_dividends = resources.AnnualizedDividendsResourceWithStreamingResponse(
            client.annualized_dividends
        )
        self.returns = resources.ReturnsResourceWithStreamingResponse(client.returns)
        self.security_shares = resources.SecuritySharesResourceWithStreamingResponse(client.security_shares)
        self.batch_processings = resources.BatchProcessingsResourceWithStreamingResponse(client.batch_processings)


class AsyncEndexFactsetGlobalPricesWithStreamedResponse:
    def __init__(self, client: AsyncEndexFactsetGlobalPrices) -> None:
        self.prices = resources.AsyncPricesResourceWithStreamingResponse(client.prices)
        self.corporate_actions = resources.AsyncCorporateActionsResourceWithStreamingResponse(client.corporate_actions)
        self.annualized_dividends = resources.AsyncAnnualizedDividendsResourceWithStreamingResponse(
            client.annualized_dividends
        )
        self.returns = resources.AsyncReturnsResourceWithStreamingResponse(client.returns)
        self.security_shares = resources.AsyncSecuritySharesResourceWithStreamingResponse(client.security_shares)
        self.batch_processings = resources.AsyncBatchProcessingsResourceWithStreamingResponse(client.batch_processings)


Client = EndexFactsetGlobalPrices

AsyncClient = AsyncEndexFactsetGlobalPrices
