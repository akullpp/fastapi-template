# fastapi-template

Template for [FastAPI](https://fastapi.tiangolo.com/) services.

The choice of state-of-the-art libraries balance simplicity and ease of use but you can switch them out if you want.

Please find some nice workspace defaults in `.vscode` if you use [VSCode](https://code.visualstudio.com/).

## Recommended Stack

### Infrastructure

- 3.12 <= [Python](https://docs.python.org) < 3.13

- [PostgreSQL](https://www.postgresql.org/docs/current/index.html)

Additionally I provide some shell scripts in `bin` to get you started with your deployment with:

- [Docker](https://docs.docker.com/)

- [Kubernetes](https://kubernetes.io/docs/home/)

- [AWS](https://docs.aws.amazon.com/)

### Libraries

- [asyncpg](https://magicstack.github.io/asyncpg/current/)

- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

- [fastapi](https://fastapi.tiangolo.com/)

- [httpx](https://www.python-httpx.org/)

- [loguru](https://github.com/Delgan/loguru)

- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)

- [pandas](https://pandas.pydata.org/)

- [pip-tools](https://github.com/jazzband/pip-tools)

- [pydantic](https://pydantic-docs.helpmanual.io/)

- [ruff](https://docs.astral.sh/ruff/)

- [SQLAlchemy](https://docs.sqlalchemy.org/)

### Decisions

- Against `black` since it's not configurable and leads to less readable code

- Against `psycopg2` which is great for synchronous code but 5x slower than `asyncpg` in most use cases

- Against `requests` since it's not async and `httpx` is basically a drop-in replacement

- Against `poetry` since breaks every now and then, doesn't follow standards and most features are not needed

## Setup

Use [asdf](https://github.com/asdf-vm/asdf) to switch between Python versions.

```shell
make
```

## Guidelines

Get [ruff](https://github.com/astral-sh/ruff) up and running in your IDE.

### Structure

- Flat, based on features, not layers

- Use technical suffixes

- Don't start with Pydantic schemas or SQLAlchemy models but evolve into them

### Tests

For each router, add an `http` file which contains at least one happy path request for each endpoint.

### Exceptions

There's only one type of exception you should raise, `CustomError` and it **must** look like this:

```py
CustomError(
    code: int,
    key: str,
    message: str | None
    details: dict | None,
)
```

Dump everything you want in `details`.
