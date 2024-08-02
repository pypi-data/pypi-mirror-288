pytest-autofixture
======
Simplify pytest fixtures by making them automagically available.  Tests can reference fixtures without needing to reference them as function parameters.


### Install
```pip install pytest-autofixture```


### Usage
```python
# conftest.py
import pytest

@pytest.fixture
def one():
    return 1


# test_one.py
def test_one():
  assert one == 1
```

----
[![Coverage Status](https://coveralls.io/repos/github/dpep/pytest-autofixture/badge.svg?branch=main)](https://coveralls.io/github/dpep/pytest-autofixture?branch=main)
[![installs](https://img.shields.io/pypi/dm/pytest-autofixture?label=installs)](https://pypi.org/project/pytest-autofixture)
