# Waylay Data Service
Data is ingested into the platform by the Waylay Broker.

This Python package is automatically generated based on the 
Waylay Data OpenAPI specification (API version: 2.14.0)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/data.html).

It consists of a plugin for the waylay-sdk-core package, and contains the Data api methods.
Note that the typed model classes for all path params, query params, body params and responses for each of the api methods are contained in a separate package called waylay-sdk-data-types.

## Requirements.
This package requires Python 3.9+.

## Installation

Normally this package is installed together with support for other services using the [waylay-sdk](https://pypi.org/project/waylay-sdk/) umbrella package:
* `pip install waylay-sdk` will install `waylay-sdk-data` together with the SDK api packages for other services.
* `pip install waylay-sdk[types-data]` will additionally install the types package `waylay-sdk-data-types`.
* `pip install waylay-sdk[types]` will install the types packages for this and all other services.

Alternatively, you can install support for this _data_ service only, installing or extending an existing [waylay-sdk-core](https://pypi.org/project/waylay-sdk-core/):

- `pip install waylay-sdk-data` to only install api support for _data_.
- `pip install waylay-sdk-data[types]` to additionally install type support for _data_.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-data-types` is installed
from waylay.services.data.models.version_response import VersionResponse
try:
    # Get Service Status
    # calls `GET /data/v1/`
    api_response = await waylay_client.data.about.get(
    )
    print("The response of data.about.get:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling data.about.get: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).