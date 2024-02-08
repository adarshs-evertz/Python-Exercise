# Python Exercise

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Exercise on cookiecutter

---

## Features

...

## Usage

## Development

To set up a development environment for this project, you can run:

```bash
pipenv sync --dev
```

This will install the dependencies named in the `Pipfile.lock` file. If the
`Pipfile.lock` file doesn't exist, then run `pipenv install --dev` (see below).

If you update the dependencies in the `Pipfile`, then run:

```bash
pipenv install --dev
```

This will install all the dependencies specified in the Pipfile, and pin them by
creating a `Pipfile.lock` file. This will use the latest versions of the
transitive dependencies, and should only be used on the initial creation of a
project, or when dependencies are updated.

Tests are located under the `tests/` directory. The source directory is added to
the `PYTHONPATH` by Pipenv when it loads the `.env` file. pytest is configured
with `tests/unit` as the default test path.

```sh
pipenv run pytest
```

## Maintainers

This project is maintained by

-   Adarsh adarshs@evertz.com

---

Copyright © 2024 Evertz. All Rights Reserved
