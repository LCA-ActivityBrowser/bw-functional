# bw-functional

[![PyPI](https://img.shields.io/pypi/v/bw-functional.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/bw-functional.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/bw-functional)][pypi status]
[![License](https://img.shields.io/pypi/l/bw-functional)][license]

[![Read the documentation at https://multifunctional.readthedocs.io/](https://img.shields.io/readthedocs/multifunctional/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/mrvisscher/bw-functional/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/brightway-lca/multifunctional/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/bw-functional/
[read the docs]: https://multifunctional.readthedocs.io/
[tests]: https://github.com/brightway-lca/multifunctional/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/brightway-lca/multifunctional
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

Adding functions to Brightway processes

## Installation

You can install _bw-functional_ via [pip] from [PyPI]:

```console
$ pip install bw-functional
```

The intended conda install is from [conda-forge](https://conda-forge.org/) (pending acceptance of the feedstock PR):

```console
$ conda install -c conda-forge bw-functional
```

The package remains available for now on the private LCA Anaconda channel, but that
channel is **deprecated** in favor of conda-forge. Prefer conda-forge once the
package appears there.

## Usage

Multifunctional activities can lead to linear algebra problems which don't have exactly one solution. Therefore, we commonly need to apply a handling function to either partition such activities, or otherwise manipulate their data such that they allow for the creation of a square and non-singular technosphere matrix.

This library is designed around the following workflow:

Users create and register a `bw_functional.FunctionalSQLiteDatabase`. Registering this database must include the database metadata key `default_allocation`, which refers to an allocation strategy function present in `bw_functional.allocation_strategies`.

```python
import bw_functional
mf_db = bw_functional.FunctionalSQLiteDatabase("emojis FTW")
mf_db.register()
```

Multifunctional process(es) are created and written to the `FunctionalSQLiteDatabase`. A multifunctional process is any process with multiple "functions", either outputs (products) and/or input (reducts).

```python
mf_data = {
    ("emojis FTW", "😼"): {
        "type": "product",
        "name": "meow",
        "unit": "kg",
        "processor": ("emojis FTW", "1"),
        "properties": {
            "price": {'unit': 'EUR', 'amount': 7, 'normalize': True},
            "mass": {'unit': 'kg', 'amount': 1, 'normalize': True},
        },
    },
    ("emojis FTW", "🐶"): {
        "type": "product",
        "name": "woof",
        "unit": "kg",
        "processor": ("emojis FTW", "1"),
        "properties": {
            "price": {'unit': 'EUR', 'amount': 12, 'normalize': True},
            "mass": {'unit': 'kg', 'amount': 4, 'normalize': True},
        },
    },
    ("emojis FTW", "1"): {
        "name": "process - 1",
        "location": "somewhere",
        "exchanges": [
            {
                "type": "production",
                "input": ("emojis FTW", "😼"),
                "amount": 4,
            },
            {
                "type": "production",
                "input": ("emojis FTW", "🐶"),
                "amount": 6,
            },
        ],
    }
}
```
LCA calculations can then be done as normal. See `dev/basic_example.ipynb` for a simple example.

### Substitution

_WORK IN PROGRESS_

### Built-in allocation functions

`bw-functional` includes the following built-in allocation functions:

* `manual_allocation`: Does allocation based on the "allocation" field of the Product. Doesn't normalize by amount of production exchange.
* `equal`: Splits burdens equally among all functional edges.

You can also do property-based allocation by specifying the property label in the `allocation` field of the Process.

## Technical notes

### Process-specific allocation strategies

Individual processes can override the default database allocation by specifying their own `allocation`:

```python
import bw2data as bd
node = bd.get_activity(database="emojis FTW", code="1")
node["allocation"] = "mass"
node.save()
```

## How does it work?

Recent Brightway versions allow users to specify which graph nodes types should be used when building matrices, and which types can be ignored. We create a multifunctional process node with the type `multifunctional`, which will be ignored when creating processed datapackages. However, in our database class `FunctionalSQLiteDatabase` we change the function which creates these processed datapackages to load the multifunctional processes, perform whatever strategy is needed to handle multifunctionality, and then use the results of those handling strategies (e.g. monofunctional processes) in the processed datapackage.

We also tell `MultifunctionalDatabase` to load a new `ReadOnlyProcess` process class instead of the standard `Activity` class when interacting with the database. This new class is read only because the data is generated from the multifunctional process itself - if updates are needed, either that input process or the allocation function should be modified.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [BSD 3 Clause license][License],
_multifunctional_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://multifunctional.readthedocs.io/en/latest/usage.html
[License]: https://github.com/brightway-lca/multifunctional/blob/main/LICENSE
[Contributor Guide]: https://github.com/brightway-lca/multifunctional/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/brightway-lca/multifunctional/issues


## Building the Documentation

You can build the documentation locally by installing the documentation Conda environment:

```bash
conda env create -f docs/environment.yml
```

activating the environment

```bash
conda activate sphinx_multifunctional
```

and [running the build command](https://www.sphinx-doc.org/en/master/man/sphinx-build.html#sphinx-build):

```bash
sphinx-build docs _build/html --builder=html --jobs=auto --write-all; open _build/html/index.html
```
