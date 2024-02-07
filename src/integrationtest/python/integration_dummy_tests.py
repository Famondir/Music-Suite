import inspect
import os
import sys

import pytest

from accordion import (
    integration_test_dummy_fct
)


def test_some_function_for_testing():
    assert integration_test_dummy_fct == True


if __name__ == "__main__":
    ret = pytest.main([os.path.abspath((inspect.stack()[0])[1]), '-s', '-vv'])
    if ret:
        sys.exit(1)