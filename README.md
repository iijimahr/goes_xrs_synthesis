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
python -m venv venv
. venv/bin/activate
pip install -U pip && pip install -e ".[dev,docs]"
```

### Task automation with Makefile

```shell
make test         # Run all tests
make docs         # Build documentation
make clean        # Clean up build artifacts
```
