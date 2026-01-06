# `goes_xrs_synthesis`

[![Run tests](https://github.com/iijimahr/goes_xrs_synthesis/actions/workflows/ci.yml/badge.svg)](https://github.com/iijimahr/goes_xrs_synthesis/actions/workflows/ci.yml)

Synthesize GOES XRS flux from (differential) emission measure.

## Documentation

<https://iijimahr.github.io/goes_xrs_synthesis/>

## For developers

### Installation

```shell
git clone https://github.com/iijimahr/goes_xrs_synthesis.git
cd goes_xrs_synthesis
pip install ".[dev,doc]"
```

### Running unit tests with pytest

```shell
make pytest
```

### Running samples with doctests

```shell
make doctest
```

### Running all tests

```shell
make test
```

### Building documentation

```shell
make doc
```
