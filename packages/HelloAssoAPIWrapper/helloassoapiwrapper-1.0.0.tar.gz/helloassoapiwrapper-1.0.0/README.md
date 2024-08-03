# HelloAsso API Wrapper

[![versions](https://img.shields.io/pypi/pyversions/HelloAssoAPIWrapper)](https://github.com/aeecleclair/HelloAssoAPIWrapper)
[![license](https://img.shields.io/github/license/aeecleclair/HelloAssoAPIWrapper)](https://github.com/aeecleclair/HelloAssoAPIWrapper/blob/main/LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

A fully typed Python wrapper for _HelloAsso_ API. You will find information about _HelloAsso_ on their [website](https://www.helloasso.com/) and their [API swagger documentation](https://api.helloasso.com/v5/swagger/ui/index).

The module is based on [Pydantic](https://docs.pydantic.dev/latest/) for models validation and on HelloAsso's [HaApiV5](https://github.com/HelloAsso/HaApiV5) for API calls.

# Installation

```bash
pip install HelloAssoAPIWrapper
```

# Usage

```python
# Import the wrapper
from helloasso_api_wrapper import HelloAssoAPIWrapper

# Create an instance of `HelloAssoAPIWrapper`
hello_asso = HelloAssoAPIWrapper(
 api_base=settings.HELLOASSO_API_BASE,
 client_id=settings.HELLOASSO_CLIENT_ID,
 client_secret=settings.HELLOASSO_CLIENT_SECRET,
 timeout=60,
)
```

## Usage example to init a checkout

```python
from helloasso_api_wrapper import HelloAssoAPIWrapper
from helloasso_api_wrapper.exceptions import ApiV5BadRequest

from helloasso_api_wrapper.models.carts import (
 CheckoutPayer,
 InitCheckoutBody,
 InitCheckoutResponse,
)

# First create an instance of `HelloAssoAPIWrapper` with the previous snippet
hello_asso = HelloAssoAPIWrapper(
 api_base=settings.HELLOASSO_API_BASE,
 client_id=settings.HELLOASSO_CLIENT_ID,
 client_secret=settings.HELLOASSO_CLIENT_SECRET,
 timeout=60,
)

# Then use the wrapper to init a checkout
init_checkout_body = InitCheckoutBody(
 totalAmount=100, # The total amount of the checkout in cents
 initialAmount=100,
 itemName="Our first checkout",
 backUrl="https://yourwebsite.com/callback", # The url must use https
 errorUrl="https://yourwebsite.com/callback",,
 returnUrl="https://yourwebsite.com/callback",,
 containsDonation=False,
 payer=CheckoutPayer(
 firstName="Fabristpp",
 lastName="John",
 email="fabristpp@email.fr",
 ),
)

response: InitCheckoutResponse
try:
 response = self.hello_asso.checkout_intents_management.init_a_checkout(
 helloasso_slug,
 init_checkout_body,
 )
except ApiV5BadRequest as error:
 print("Failed to init a checkout")
 raise error
```

# Structure of the module

Authentication is done on the background using HelloAsso's `HaApiV5` module.

The module is organized around a class [`HelloAssoAPIWrapper`](./helloasso_api_wrapper/__init__.py) containing all the methods to interact with the HelloAsso API.

This class expose multiple clients, allowing to interact with different parts of the API. All clients are located in the [`clients`](./helloasso_api_wrapper/clients) folder.

Pydantic models are located in the [`models`](./helloasso_api_wrapper/models) folder. Models are usually really permissive, typing all fields as Nullable. This is because the API is not always clear about the fields that are required or not. _Some assumptions are made to make the models more strict._

We expose exceptions from `HaApiV5`. You can import them directly: `from helloasso_api_wrapper.exceptions import *`

# Documentation about HelloAsso API

You will find documentation about HelloAsso API endpoints on:

- [HelloAsso API swagger documentation](https://api.helloasso.com/v5/swagger/ui/index)
- [HelloAsso API documentation](https://www.helloasso.com/public-documents/documents_api/guide_utilisation_api.pdf)
- [HelloAsso Checkout documentation](https://www.helloasso.com/public-documents/documents_api/documentation_checkout.pdf)

## HelloAsso sandbox

HelloAsso provide a sandbox: api.helloasso-sandbox.com to test your integration.

# Notification result webhooks

You should configure a webhook to receive the notification results.
HelloAsso will make a POST request to the URL you provided with a JSON payload corresponding to a `NotificationResultContent` object.

# Development

Models where first generated using HelloAsso swagger documentation, and then adapted to include additional models, use stricter types and add documentation. _Some assumptions are made to make the models more strict._

## Add new methods

Currently, most endpoints are not implemented. To add a new method, you simply need to create a new method in the corresponding client. The method should use the `self.api.callAndSerialize` method to make the API call.

Example for [checkout_intents_management `init_a_checkout` method](./helloasso_api_wrapper/clients/checkout_intents_management.py):

```python
def init_a_checkout(
 self,
 organization_slug: str,
 init_checkout_body: InitCheckoutBody,
) -> InitCheckoutResponse:
 return self.api.callAndSerialize(
 f"/organizations/{organization_slug}/checkout-intents", # API endpoint
 InitCheckoutResponse, # Model to serialize the response
 body=init_checkout_body, # Body of the request
 method="POST", # Request method
 )
```

## Models auto-generation

> This was used to generate the first version of the models. It should not be necessary to do it again.

Download the swagger file from the HelloAsso API documentation. It uses an old swagger 2 version. You need to convert it to OpenAPI 3.0.0 version. You can use the online tool [Swagger Editor](https://editor.swagger.io/).

Then you can use the [datamodel-codegen](https://docs.pydantic.dev/latest/integrations/datamodel_code_generator/) tool to generate the models:

```bash
datamodel-codegen --input HelloAssoV5OpenAPI.json --output HelloAssoAPIWrapper
```

# Make a release on Pypi

You need to edit HelloAssoAPIWrapper version in [helloasso_api_wrapper/\_\_about\_\_.py](./helloasso_api_wrapper/__about__.py). Then make a release on GitHub and add a tag. The tag should match v\*.\*.\*.


