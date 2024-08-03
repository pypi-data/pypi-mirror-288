# Waylay Rules Service
The REST api to manage rule tasks and rule templates in the Waylay platform.

This Python package is automatically generated based on the 
Waylay Rules OpenAPI specification (API version: 6.5.0)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/rules.html).

It is considered an extension of the waylay-sdk-rules package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-rules`.

## Requirements.
This package requires Python 3.9+.

## Installation

Normally this package is installed together with support for other services using the [waylay-sdk](https://pypi.org/project/waylay-sdk/) umbrella package:
* `pip install waylay-sdk` will install `waylay-sdk-rules` together with the SDK api packages for other services.
* `pip install waylay-sdk[types-rules]` will additionally install the types package `waylay-sdk-rules-types`.
* `pip install waylay-sdk[types]` will install the types packages for this and all other services.

Alternatively, you can install support for this _rules_ service only, installing or extending an existing [waylay-sdk-core](https://pypi.org/project/waylay-sdk-core/):

- `pip install waylay-sdk-rules` to only install api support for _rules_.
- `pip install waylay-sdk-rules[types]` to additionally install type support for _rules_.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-rules-types` is installed
from waylay.services.rules.models.version_response import VersionResponse
try:
    # Get Service Information
    # calls `GET /rules/v1`
    api_response = await waylay_client.rules.about.get(
    )
    print("The response of rules.about.get:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling rules.about.get: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).
