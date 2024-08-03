# Waylay Queries Service

Execute and store queries on the Waylay timeseries.

Protocol version: v1.

This Python package is automatically generated based on the 
Waylay Queries OpenAPI specification (API version: 0.5.0)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/queries.html).

It consists of a plugin for the waylay-sdk-core package, and contains the Queries api methods.
Note that the typed model classes for all path params, query params, body params and responses for each of the api methods are contained in a separate package called waylay-sdk-queries-types.

## Requirements.
This package requires Python 3.9+.

## Installation

Normally this package is installed together with support for other services using the [waylay-sdk](https://pypi.org/project/waylay-sdk/) umbrella package:
* `pip install waylay-sdk` will install `waylay-sdk-queries` together with the SDK api packages for other services.
* `pip install waylay-sdk[types-queries]` will additionally install the types package `waylay-sdk-queries-types`.
* `pip install waylay-sdk[types]` will install the types packages for this and all other services.

Alternatively, you can install support for this _queries_ service only, installing or extending an existing [waylay-sdk-core](https://pypi.org/project/waylay-sdk-core/):

- `pip install waylay-sdk-queries` to only install api support for _queries_.
- `pip install waylay-sdk-queries[types]` to additionally install type support for _queries_.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-queries-types` is installed
from waylay.services.queries.models.query_input import QueryInput
from waylay.services.queries.models.query_result import QueryResult
try:
    # Execute Query
    # calls `POST /queries/v1/queries/v1/data`
    api_response = await waylay_client.queries.execute.execute(
        # query parameters:
        query = {
            'resource': '13efb488-75ac-4dac-828a-d49c5c2ebbfc'
            'metric': 'temperature'
        },
        # json data: use a generated model or a json-serializable python data structure (dict, list)
        json = waylay.services.queries.QueryInput() # QueryInput | 
        headers = {
            'accept': 'accept_example',
        },
    )
    print("The response of queries.execute.execute:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling queries.execute.execute: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).