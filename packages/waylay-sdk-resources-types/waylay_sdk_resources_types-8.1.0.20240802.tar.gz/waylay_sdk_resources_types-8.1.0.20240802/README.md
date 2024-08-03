# Waylay Resources Service
This service manages 
[Waylay Resources](/#/features/resources/?id=resource) and related entities.

A _Waylay Resource_ models a real-world device or abstract entity of your IoT solution,
and provides a context when processing data in the Rule Engine.

You'll interact with the _Waylay Resources_ API to create this _Digital Twin_ model, 
a process that's also called _resource provisioning_.

This Python package is automatically generated based on the 
Waylay Resources OpenAPI specification (API version: 8.1.0)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/resources.html).

It is considered an extension of the waylay-sdk-resources package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-resources`.

## Requirements.
This package requires Python 3.9+.

## Installation

Normally this package is installed together with support for other services using the [waylay-sdk](https://pypi.org/project/waylay-sdk/) umbrella package:
* `pip install waylay-sdk` will install `waylay-sdk-resources` together with the SDK api packages for other services.
* `pip install waylay-sdk[types-resources]` will additionally install the types package `waylay-sdk-resources-types`.
* `pip install waylay-sdk[types]` will install the types packages for this and all other services.

Alternatively, you can install support for this _resources_ service only, installing or extending an existing [waylay-sdk-core](https://pypi.org/project/waylay-sdk-core/):

- `pip install waylay-sdk-resources` to only install api support for _resources_.
- `pip install waylay-sdk-resources[types]` to additionally install type support for _resources_.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-resources-types` is installed
from waylay.services.resources.models.version_response import VersionResponse
try:
    # Get Service Information
    # calls `GET /resources/v1/`
    api_response = await waylay_client.resources.about.get(
    )
    print("The response of resources.about.get:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling resources.about.get: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).
