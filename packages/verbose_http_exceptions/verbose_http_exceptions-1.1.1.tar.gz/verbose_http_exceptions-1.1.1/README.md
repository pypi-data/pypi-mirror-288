
# Verbose HTTP exceptions

![coverage](./coverage.svg)

## For what?

I made this package to make my work with http exceptions more easier. In FastAPI I had problem
with HTTP exceptions - they are too simple. Only `detail` field and that is all. And other tools
that make http exceptions more verbose works not like I expect.

## Install

To install the package you need you run the following commands.

For pip:

```bash
pip install verbose_http_exceptions
```

For poetry:

```bash
poetry add verbose_http_exceptions
```

For PDM:

```bash
pdm add verbose_http_exceptions
```

## Usage

Verbose exceptions with single format. This utils was inspired by
[drf-exceptions-hog](https://github.com/PostHog/drf-exceptions-hog), but implemented for other
Web-frameworks.

Now only FastAPI extension is implemented.

### FastAPI implementation

To work with this util you must add exception handlers in your FastAPI project like this:

```python
from fastapi import FastAPI
from verbose_http_exceptions.fastapi.handlers import (
    apply_verbose_http_exception_handler,
    apply_all_handlers,
)

app = FastAPI()
apply_all_handlers(app)
# or
apply_verbose_http_exception_handler(app)
# See document-strings of functions for more information.
```

Then all (or some specific part of) your exceptions will be returned to users in JSON like this:

```json
{
    "code": "validation_error",
    "type": "literal_error",
    "message": "Input should be 1 or 2",
    "attr": "a",
    "location": "query",
}
```

or this (multiple exceptions supported too):

```json
{
    "code": "multiple",
    "type": "multiple",
    "message": "Multiple exceptions ocurred. Please check list for details.",
    "attr": null,
    "location": null,
    "nested_errors": [
        {
            "code": "validation_error",
            "type": "literal_error",
            "message": "Input should be 1 or 2",
            "attr": "a",
            "location": "query",
        },
        {
            "code": "validation_error",
            "type": "missing",
            "message": "Field required",
            "attr": "b",
            "location": "query",
        }
    ]
}
```

`apply_all_handler` function also has `override_422_openapi` param (default True). You can turn
it off to avoid overriding 422 errors in your application OpenAPI schema.
