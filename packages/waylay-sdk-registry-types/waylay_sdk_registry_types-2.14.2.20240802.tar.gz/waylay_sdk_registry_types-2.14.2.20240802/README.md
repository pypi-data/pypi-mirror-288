# Waylay Registry Service
V2 API to build and deploy Waylay functions (plugs, webscripts, BYOML models).

This Python package is automatically generated based on the 
Waylay Registry OpenAPI specification (API version: 2.14.2)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/registry.html).

It is considered an extension of the waylay-sdk-registry package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-registry`.

## Requirements.
This package requires Python 3.9+.

## Installation

Normally this package is installed together with support for other services using the [waylay-sdk](https://pypi.org/project/waylay-sdk/) umbrella package:
* `pip install waylay-sdk` will install `waylay-sdk-registry` together with the SDK api packages for other services.
* `pip install waylay-sdk[types-registry]` will additionally install the types package `waylay-sdk-registry-types`.
* `pip install waylay-sdk[types]` will install the types packages for this and all other services.

Alternatively, you can install support for this _registry_ service only, installing or extending an existing [waylay-sdk-core](https://pypi.org/project/waylay-sdk-core/):

- `pip install waylay-sdk-registry` to only install api support for _registry_.
- `pip install waylay-sdk-registry[types]` to additionally install type support for _registry_.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-registry-types` is installed
from waylay.services.registry.models.root_page_response import RootPageResponse
try:
    # Get Service Status
    # calls `GET /registry/v2/`
    api_response = await waylay_client.registry.about.get(
    )
    print("The response of registry.about.get:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling registry.about.get: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).
