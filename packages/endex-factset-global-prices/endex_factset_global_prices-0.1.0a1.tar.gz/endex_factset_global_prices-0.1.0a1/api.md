# Prices

Types:

```python
from endex_factset_global_prices.types import GlobalPricesResponse
```

Methods:

- <code title="post /factset-global-prices/v1/prices">client.prices.<a href="./src/endex_factset_global_prices/resources/prices.py">create</a>(\*\*<a href="src/endex_factset_global_prices/types/price_create_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/global_prices_response.py">GlobalPricesResponse</a></code>
- <code title="get /factset-global-prices/v1/prices">client.prices.<a href="./src/endex_factset_global_prices/resources/prices.py">list</a>(\*\*<a href="src/endex_factset_global_prices/types/price_list_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/global_prices_response.py">GlobalPricesResponse</a></code>

# CorporateActions

Types:

```python
from endex_factset_global_prices.types import CorporateActionsResponse
```

Methods:

- <code title="post /factset-global-prices/v1/corporate-actions">client.corporate_actions.<a href="./src/endex_factset_global_prices/resources/corporate_actions.py">create</a>(\*\*<a href="src/endex_factset_global_prices/types/corporate_action_create_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/corporate_actions_response.py">CorporateActionsResponse</a></code>
- <code title="get /factset-global-prices/v1/corporate-actions">client.corporate_actions.<a href="./src/endex_factset_global_prices/resources/corporate_actions.py">list</a>(\*\*<a href="src/endex_factset_global_prices/types/corporate_action_list_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/corporate_actions_response.py">CorporateActionsResponse</a></code>

# AnnualizedDividends

Types:

```python
from endex_factset_global_prices.types import AnnualizedDividendResponse
```

Methods:

- <code title="post /factset-global-prices/v1/annualized-dividends">client.annualized_dividends.<a href="./src/endex_factset_global_prices/resources/annualized_dividends.py">create</a>(\*\*<a href="src/endex_factset_global_prices/types/annualized_dividend_create_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/annualized_dividend_response.py">AnnualizedDividendResponse</a></code>
- <code title="get /factset-global-prices/v1/annualized-dividends">client.annualized_dividends.<a href="./src/endex_factset_global_prices/resources/annualized_dividends.py">list</a>(\*\*<a href="src/endex_factset_global_prices/types/annualized_dividend_list_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/annualized_dividend_response.py">AnnualizedDividendResponse</a></code>

# Returns

Types:

```python
from endex_factset_global_prices.types import ReturnsResponse
```

Methods:

- <code title="post /factset-global-prices/v1/returns">client.returns.<a href="./src/endex_factset_global_prices/resources/returns.py">create</a>(\*\*<a href="src/endex_factset_global_prices/types/return_create_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/returns_response.py">ReturnsResponse</a></code>
- <code title="get /factset-global-prices/v1/returns">client.returns.<a href="./src/endex_factset_global_prices/resources/returns.py">list</a>(\*\*<a href="src/endex_factset_global_prices/types/return_list_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/returns_response.py">ReturnsResponse</a></code>

# SecurityShares

Types:

```python
from endex_factset_global_prices.types import SharesOutstandingResponse
```

Methods:

- <code title="post /factset-global-prices/v1/security-shares">client.security_shares.<a href="./src/endex_factset_global_prices/resources/security_shares.py">create</a>(\*\*<a href="src/endex_factset_global_prices/types/security_share_create_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/shares_outstanding_response.py">SharesOutstandingResponse</a></code>
- <code title="get /factset-global-prices/v1/security-shares">client.security_shares.<a href="./src/endex_factset_global_prices/resources/security_shares.py">list</a>(\*\*<a href="src/endex_factset_global_prices/types/security_share_list_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/shares_outstanding_response.py">SharesOutstandingResponse</a></code>

# BatchProcessings

## BatchStatus

Types:

```python
from endex_factset_global_prices.types.batch_processings import BatchStatusResponse
```

Methods:

- <code title="get /factset-global-prices/v1/batch-status">client.batch_processings.batch_status.<a href="./src/endex_factset_global_prices/resources/batch_processings/batch_status.py">retrieve</a>(\*\*<a href="src/endex_factset_global_prices/types/batch_processings/batch_status_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/batch_processings/batch_status_response.py">BatchStatusResponse</a></code>

## BatchResults

Types:

```python
from endex_factset_global_prices.types.batch_processings import BatchResultResponse
```

Methods:

- <code title="get /factset-global-prices/v1/batch-result">client.batch_processings.batch_results.<a href="./src/endex_factset_global_prices/resources/batch_processings/batch_results.py">retrieve</a>(\*\*<a href="src/endex_factset_global_prices/types/batch_processings/batch_result_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_global_prices/types/batch_processings/batch_result_response.py">BatchResultResponse</a></code>
