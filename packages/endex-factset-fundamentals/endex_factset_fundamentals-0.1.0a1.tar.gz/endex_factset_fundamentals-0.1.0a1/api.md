# Fundamentals

Types:

```python
from endex_factset_fundamentals.types import FundamentalsResponse
```

Methods:

- <code title="post /fundamentals">client.fundamentals.<a href="./src/endex_factset_fundamentals/resources/fundamentals.py">create</a>(\*\*<a href="src/endex_factset_fundamentals/types/fundamental_create_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/fundamentals_response.py">FundamentalsResponse</a></code>
- <code title="get /fundamentals">client.fundamentals.<a href="./src/endex_factset_fundamentals/resources/fundamentals.py">list</a>(\*\*<a href="src/endex_factset_fundamentals/types/fundamental_list_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/fundamentals_response.py">FundamentalsResponse</a></code>

# Segments

Types:

```python
from endex_factset_fundamentals.types import SegmentsResponse
```

Methods:

- <code title="post /segments">client.segments.<a href="./src/endex_factset_fundamentals/resources/segments.py">create</a>(\*\*<a href="src/endex_factset_fundamentals/types/segment_create_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/segments_response.py">SegmentsResponse</a></code>
- <code title="get /segments">client.segments.<a href="./src/endex_factset_fundamentals/resources/segments.py">list</a>(\*\*<a href="src/endex_factset_fundamentals/types/segment_list_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/segments_response.py">SegmentsResponse</a></code>

# CompanyReports

## FinancialStatement

Types:

```python
from endex_factset_fundamentals.types.company_reports import FinancialResponse
```

Methods:

- <code title="get /company-reports/financial-statement">client.company_reports.financial_statement.<a href="./src/endex_factset_fundamentals/resources/company_reports/financial_statement.py">retrieve</a>(\*\*<a href="src/endex_factset_fundamentals/types/company_reports/financial_statement_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/company_reports/financial_response.py">FinancialResponse</a></code>

## Profile

Types:

```python
from endex_factset_fundamentals.types.company_reports import ProfileResponse
```

Methods:

- <code title="get /company-reports/profile">client.company_reports.profile.<a href="./src/endex_factset_fundamentals/resources/company_reports/profile.py">retrieve</a>(\*\*<a href="src/endex_factset_fundamentals/types/company_reports/profile_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/company_reports/profile_response.py">ProfileResponse</a></code>

## Fundamentals

Types:

```python
from endex_factset_fundamentals.types.company_reports import CompanyFundamentalsResponse
```

Methods:

- <code title="get /company-reports/fundamentals">client.company_reports.fundamentals.<a href="./src/endex_factset_fundamentals/resources/company_reports/fundamentals.py">retrieve</a>(\*\*<a href="src/endex_factset_fundamentals/types/company_reports/fundamental_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/company_reports/company_fundamentals_response.py">CompanyFundamentalsResponse</a></code>

# Metrics

Types:

```python
from endex_factset_fundamentals.types import MetricsResponse
```

Methods:

- <code title="get /metrics">client.metrics.<a href="./src/endex_factset_fundamentals/resources/metrics.py">list</a>(\*\*<a href="src/endex_factset_fundamentals/types/metric_list_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/metrics_response.py">MetricsResponse</a></code>

# BatchProcessing

Types:

```python
from endex_factset_fundamentals.types import BatchResultResponse, BatchStatusResponse
```

Methods:

- <code title="get /batch-result">client.batch_processing.<a href="./src/endex_factset_fundamentals/resources/batch_processing.py">result</a>(\*\*<a href="src/endex_factset_fundamentals/types/batch_processing_result_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/batch_result_response.py">BatchResultResponse</a></code>
- <code title="get /batch-status">client.batch_processing.<a href="./src/endex_factset_fundamentals/resources/batch_processing.py">status</a>(\*\*<a href="src/endex_factset_fundamentals/types/batch_processing_status_params.py">params</a>) -> <a href="./src/endex_factset_fundamentals/types/batch_status_response.py">BatchStatusResponse</a></code>
