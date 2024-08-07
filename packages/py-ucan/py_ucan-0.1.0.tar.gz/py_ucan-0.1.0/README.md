# py-ucan

[![pypi](https://img.shields.io/pypi/v/py-ucan.svg?color=4B8BBE)](https://pypi.org/project/py-ucan/)

This is a Python library to help the web applications make use
of UCANs in their authorization flows. To learn more about UCANs and how you
might use them in your application, visit [ucan website](https://ucan.xyz) or
read the [spec](https://github.com/ucan-wg/spec).


<a id="contents"></a>

# **Contents**

- [Installation](#installation)
- [Usage](#usage)
    - [Ucan Objects](#ucan-objects)
        - [ucan.ResourcePointer](#ucan-objects-resource-pointer)
        - [ucan.Ability](#ucan-objects-ability)
        - [ucan.Capability](#ucan-objects-capability)
    - [Parsing UCAN Tokens](#parsing-ucan-tokens)
    - [Validating UCAN Tokens](#validating-ucan-tokens)
    - [Verifying UCAN Invocations](#verifying-ucan-invocations)

<a id="installation"></a>

## Installation [`⇧`](#contents)

```
pip install -U py-ucan
```

<a id="usage"></a>

## Usage [`⇧`](#contents)

<a id="ucan-objects"></a>

### Ucan objects [`⇧`](#contents)

All the objects are based on [Pydantic v2](https://docs.pydantic.dev/latest/) models. Ideally you would only need to use [`model_validate`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate), [`model_validate_json`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate_json) and [`model_dump`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump) from the pydantic model API, but please go through their docs for advanced usage.

NOTE: Ojects can be instantiated with field names in camel case, but to access those fields, you need to use their snake case names.


<a id="ucan-objects-resource-pointer"></a>

#### ucan.ResourcePointer

```py

from ucan import ResourcePointer

# -- from encoded value
resource = ResourcePointer.decode("fileverse://solo.fileverse.io")

# -- from kwargs: snake case
resource = ResourcePointer(scheme="fileverse", hier_part="//solo.fileverse.io")

# -- from kwargs: camel case
resource = ResourcePointer(scheme="fileverse", hierPart="//solo.fileverse.io")

# -- from dict: snake case
resource = ResourcePointer.model_validate({"scheme": "fileverse", "hier_part": "//solo.fileverse.io"})

# -- from dict: camel case
resource = ResourcePointer.model_validate({"scheme": "fileverse", "hierPart": "//solo.fileverse.io"})

# -- from json: snake case
resource = ResourcePointer.model_validate_json('{"scheme": "fileverse", "hier_part": "//solo.fileverse.io"}')

# -- from json: camel case
resource = ResourcePointer.model_validate_json('{"scheme": "fileverse", "hierPart": "//solo.fileverse.io"}')

# access values
print(resource.scheme, resource.hier_part)
# output: fileverse //solo.fileverse.io

# dump to python dict
# all the objects above will dump to a dict with camel case fields
print(resource.model_dump()) 
# output: {'scheme': 'fileverse', 'hierPart': '//solo.fileverse.io'}

# encode as string
print(resource.encode()) 
# or 
print(str(resource)) 
# output: fileverse://solo.fileverse.io

```


<a id="ucan-objects-ability"></a>

#### ucan.Ability

```py

from ucan import Ability

# -- from encoded value
ability = Ability.decode("crud/edit")

# -- from kwargs
ability = Ability(namespace="crud", segments=["edit"])

# -- from dict
ability = Ability.model_validate({"namespace": "crud", "segments": ["edit"]})

# -- from json
ability = Ability.model_validate_json('{"namespace": "crud", "segments": ["edit"]}')

# access values
print(ability.namespace, ability.segments)
# output: crud ['edit']

# dump to python dict
# all the objects above will dump to a dict
print(ability.model_dump()) 
# output: {'namespace': 'crud', 'segments': ['edit']}

# encode as string
print(ability.encode()) 
# or 
print(str(ability)) 
# output: crud/edit

```


<a id="ucan-objects-capability"></a>

#### ucan.Capability

NOTE: since `with` is a reserved keyword in python, the `with` field in `Capability` is accessible via `with_` attribute, but the `Capability` model supports loading values having `with` field name using a python dict or a JSON string (see examples below).

```py

import json

from ucan import Ability, Capability, ResourcePointer


# --- load `with` value

# loaded from kwargs
resource = ResourcePointer(scheme="https", hier_part="//app.example.com") 
# or loaded from string
resource = ResourcePointer.decode("https:////app.example.com")
# or an encoded string
resource = "https://app.example.com"  # encoded value
# or a dict with snake case field names
resource = {"scheme": "https", "hier_part": "//app.example.com"}
# or a dict with camel case field names
resource = {"scheme": "https", "hierPart": "//app.example.com"}


# --- load `can` value

# loaded from kwargs
ability = Ability(namespace="crud", segments=["view"]) 
# or loaded from string
ability = Ability.decode("crud/view")
# or an encoded string
ability = "crud/view"  # encoded value
# or a dict with snake case field names
ability = {"namespace": "crud", "segments": ["view"]}


# --- load `capability` value
# note: all the above variations of `resource` and `ability` are supported.

# -- from kwargs
capability = Capability(with_=resource, can=ability)
# -- or by spreading the dict as kwargs
capability = Capability(**{"with": resource, "can": ability})

# -- from dict
capability = Capability.model_validate({"with": resource, "can": ability})
# or
capability = Capability.model_validate({"with_": resource, "can": ability})

# -- from json
capability = Capability.model_validate_json(
    json.dumps({"with": resource, "can": ability})
)
# or
capability = Capability.model_validate_json(
    json.dumps({"with_": resource, "can": ability})
)

# access values
# note: `with` field cannot be accessed with the name `with`, use `with_` instead.
# note: print function outputs the str representation of the models
# and since `ResourcePointer` and `Ability` models implement their 
# respective `__str__` callbacks, the output is simply their encoded values.
print(capability.with_, capability.can)
# output: https://app.example.com crud/view

# dump to python dict
# all the objects above will dump to a dict
print(capability.model_dump()) 
"""
output:
{
    'with': {'scheme': 'https', 'hierPart': '//app.example.com'},
    'can': {'namespace': 'crud', 'segments': ['view']}
}
"""

# encode all capability parts
print(capability.encode()) 
# output: {'with': 'https://app.example.com', 'can': 'crud/view'}


```


<a id="parsing-ucan-tokens"></a>

### Parsing UCAN Tokens [`⇧`](#contents)

To parse a token without validating its signature or expiry, you need to use the `parse` function or `Ucan.decode` model function.

```py

import ucan

# receive the token from user request.
encoded_token = "eyJhbG..."  # request.headers.get("Authorization") or similar

# using `ucan.parse`

try:
    # here `parsed_token` is an instance of `ucan.Ucan`.
    parsed_token = ucan.parse(encoded_token)

except ValueError as e:
    # Invalid token
    pass

# or, using `ucan.Ucan.decode` model function

try:
    # here `parsed_token` is an instance of `ucan.Ucan`.
    parsed_token = ucan.Ucan.decode(encoded_token)

except ValueError as e:
    # Invalid token
    pass

```


<a id="validating-ucan-tokens"></a>

### Validating UCAN Tokens [`⇧`](#contents)

To validate a token, you need to use the `validate` function.

```py

import ucan

# receive the token from user request.
encoded_token = "eyJhbG..."  # request.headers.get("Authorization") or similar

# parse and validate the token
try:
    # here `parsed_token` is an instance of `ucan.Ucan`.
    parsed_token = await ucan.validate(encoded_token)

except Exception as e:
    # Invalid token
    pass

```


<a id="verifying-ucan-invocations"></a>

### Verifying UCAN Invocations [`⇧`](#contents)

Using a UCAN to authorize an action is called "invocation".

To verify invocations, you need to use the `verify` function.

```py

import ucan

# receive the token from user request.
encoded_token = "eyJhbG..."  # request.headers.get("Authorization") or similar

# generate service keypair
service_key = ucan.EdKeypair.generate()
service_did = service_key.did()  # will return "did:key:zabcde..."

# known resource and user to validate against
doc_id = "some-id"
user_did = "did:key:z6Mk..."

result = await ucan.verify(
    encoded_token,
    # to make sure we're the intended recipient of this UCAN
    audience=service_did,
    # capabilities required for this invocation & which owner we expect for each capability
    required_capabilities=[
        ucan.RequiredCapability(
            capability=ucan.Capability(
                with_=ucan.ResourcePointer(
                    scheme="fileverse", hier_part="//portal.fileverse.io"
                ),
                can=ucan.Ability(namespace=doc_id, segments=["EDIT", "VIEW"]),
            ),
            # check against a known owner of the `doc_id` resource
            root_issuer=user_did,
        ),
    ],
)

# result will be one of the following:
# error: ucan.VerifyResultError(ok=False, errors=[Exception("...")]
# success: ucan.VerifyResultOk(ok=True, value=[ucan.Verification(..)])

if isinstance(result, ucan.VerifyResultOk):
    # The UCAN authorized the user
    pass

else:
    # Unauthorized
    pass
```
