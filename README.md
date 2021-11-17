# oais-utilities

[![PyPI version](https://badge.fury.io/py/oais-utils.svg)](https://pypi.org/project/oais-utils/)

OAIS wide utilities

## Install

Install from PyPi

```bash
pip install oais-utils
```

For development, you can clone this repository and then install it with the `-e` flag:

```bash
# Clone the repository
git clone https://gitlab.cern.ch/digitalmemory/oais-utils
cd oais-utils
pip install -e .
```

## Features

- Validate AIP

## Use

```python
from oais_utils import validate
validate("../bagit-create/bagitexport::cds::2751237")
```
