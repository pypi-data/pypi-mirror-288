# Lumos Connectors

[![PyPI - Version](https://img.shields.io/pypi/v/connector-py.svg)](https://pypi.org/project/connector-py)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/connector-py.svg)](https://pypi.org/project/connector-py)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install connector-py
```

## Usage

The package can be used in three ways:
1. A CLI to scaffold a custom connector with its own CLI to call commands
2. A library to create a custom connector
3. A library to convert your custom connector code to a FastAPI HTTP server

To get started, run `connector --help`

An example of running a command that accepts arguments
in an integration connector called `mock-connector`:

```shell
mock-connector info --json '{"a": 1}'
```

### Scaffold

To scaffold a custom connector, run `connector scaffold --help`

To scaffold the mock-connector, run
`connector scaffold mock-connector "projects/connectors/python/mock-connector"`

### Unasync

When developing this package, start off creating async functions and then
convert them to sync functions using `unasync`.

```console
connector hacking unasync
```

### FastAPI

To convert your custom connector to a FastAPI HTTP server, run `connector hacking http-server`

## Tips

#### The library I want to use is synchronous only

You can use a package called `asgiref`. This package converts I/O bound synchronous
calls into asyncio non-blocking calls. First, add asgiref to your dependencies list
in `pyproject.toml`. Then, in your async code, use `asgiref.sync_to_async` to convert
synchronous calls to asynchronous calls.

```python
from asgiref.sync import sync_to_async
import requests

async def async_get_data():
    response = await sync_to_async(requests.get)("url")
```

## License

`connector` is distributed under the terms of the [Apache 2.0](./LICENSE.txt) license.
