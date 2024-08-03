# Waylay Storage Service

Manage storage buckets and subscriptions.


This Python package is automatically generated based on the 
Waylay Storage OpenAPI specification (API version: 0.4.4)
For more information, please visit [the openapi specification](https://docs.waylay.io/openapi/public/redocly/storage.html).

It is considered an extension of the waylay-sdk-storage package, and it consists of the typed model classes for all path params, query params, body params and responses for each of the api methods in `waylay-sdk-storage`.

## Requirements.
This package requires Python 3.9+.

## Installation

Normally this package is installed together with support for other services using the [waylay-sdk](https://pypi.org/project/waylay-sdk/) umbrella package:
* `pip install waylay-sdk` will install `waylay-sdk-storage` together with the SDK api packages for other services.
* `pip install waylay-sdk[types-storage]` will additionally install the types package `waylay-sdk-storage-types`.
* `pip install waylay-sdk[types]` will install the types packages for this and all other services.

Alternatively, you can install support for this _storage_ service only, installing or extending an existing [waylay-sdk-core](https://pypi.org/project/waylay-sdk-core/):

- `pip install waylay-sdk-storage` to only install api support for _storage_.
- `pip install waylay-sdk-storage[types]` to additionally install type support for _storage_.

## Usage

```python
from pprint import pprint

# Import the waylay-client from the waylay-sdk-core package
from waylay.sdk.client import WaylayClient
from waylay.sdk.api.api_exceptions import ApiError

# Intialize a waylay client instance
waylay_client = WaylayClient.from_profile()

# Note that the typed model classes for responses/parameters/... are only available when `waylay-sdk-storage-types` is installed
from waylay.services.storage.models.tenant_status_report import TenantStatusReport
try:
    # Status
    # calls `GET /storage/v1/status`
    api_response = await waylay_client.storage.about.status(
        # query parameters:
        query = {
            'include_buckets': True
            'include_queues': True
            'include_disk_usage': False
        },
    )
    print("The response of storage.about.status:\n")
    pprint(api_response)
except ApiError as e:
    print("Exception when calling storage.about.status: %s\n" % e)
```


For more information, please visit the [Waylay API documentation](https://docs.waylay.io/#/api/?id=software-development-kits).
