# TANGO Checkup

**Checkup**: a general examination of someone's or something's condition.

This repository contains resources for writing "health check" tests for TANGO control systems. The idea is to encode knowledge about what conditions are good for experiments in a format that can be checked automatically against reality. This can save time, reduce the risk of mistakes, and serve as a form of "living" documentation.

It's implemented as a small `pytest` plugin. "Tests" are just regular test functions, enhanced by importing and using the various fixtures, decorators, and helper functions from `tango_checkup`.


## Installation

> **Note**: tango-checkup uses `pytango` and is only useful when run on a machine with access to a TANGO control system.

To install `tango_checkup`, run:

```sh
pip install tango-checkup
```

Now you can import and use any of the decorators, fixtures, and helper functions from `tango_checkup`. See `examples/test_playground.py` for some concrete examples!

## Running Tests

Assuming you are in a directory containing some test modules, and the control system is available, you can run your tests with:

```sh
pytest
```

Since tango-checkup is just a pytest plugin, all the usual features of the pytest test runner are available.

For example, to run tests in a specific file, filter on test function names, and get more verbose output:

```sh
pytest tests/test_b_branch.py -k gauge -vv
```

If you use "marks" on your tests, you can also select tests with particular marks:

```sh
pytest -m branch_a
```

Running only the tests that failed last time:

```sh
pytest --lf
```

`pytest` has a lot of facilities for running tests; see the documentation for more details.


## HTML Reports

To generate a nice HTML report of the results:

```sh
checkup --html-report
```

A web browser should open automatically (if available).


## Writing Checkup Tests

There are some example tests in `examples/test_playground.py` that can be used as examples. If you have a basic TANGO system available, you can run them with:

```sh
checkup examples/test_playground.py
```

It all builds on `pytest` and `pytango`; see their documentation for more details. Generally, the same rules apply as for writing tests in other contexts.

### Summary of How (py)tests Work:

- A test is a function whose name begins with `test_`. Tests should be written to check a particular desirable situation, e.g., a pressure being good.

- A test fails if any `assert` fails, or if `pytest.fail` is called. This indicates that the situation is not as desired. Any other exception is considered an error, preventing the test from doing its checks. Otherwise, the test passes; things are looking fine.

- Tests should be expected to succeed. A test that usually fails tends to get ignored and eventually becomes useless.

- Test arguments (e.g., `device`) are "fixtures" that are supplied by decorators, like `@with_devices()`. This allows a single test function to run across many devices, for example.

- Tests should have a "docstring" where the first line is a concise title for the test, explaining its purpose. Further details can be given on subsequent lines. This information is used when reporting the test results.

- Checks and asserts should include a message to be shown if the test fails. It should focus on what the consequences are and what to do about it. The purpose of the test is already described in the docstring.

- Using helper functions (e.g., `check_device_state`, `get_attribute`) is not mandatory but provides extra features like exception handling and improved report output.

- It's good practice to write tests that don't change the control system in any way. This way, they should be safe to run at any time. If you do have to make changes, try to leave the control system as it was before. Also, make sure to document which tests are not always safe to run, probably best to put them in a separate file that is not run by default.

- You can structure your test suite as you like; e.g., it could be split up across different modules, putting common stuff in a separate module and importing tests from there, etc.


## Further Configuration

Since `tango_checkup` is built on `pytest`, you can use all features of `pytest` to enhance your test suite. Default config options can be tweaked in `pytest.ini`, and you can create a `conftest.py` file with your own fixtures. See `pytest` docs for more info and ideas.

## Examples

Here are some example tests demonstrating how to use the provided fixtures, decorators, and checks.

### Example 1: Checking Device State

```python
from tango import DevState
from tango_checkup.decorators import with_devices
from tango_checkup.checks import check_not_device_state

@with_devices("sys/tg_test/1", "sys/database/2", "sys/tg_test/17")
def test_device_is_ok(device):
    """
    Test that the device is not in FAULT state.
    """
    check_not_device_state(
        device,
        DevState.FAULT,  # The undesired state
        "Try turning it on and off again."  # A helpful message for when the test fails
    )
```

### Example 2: Checking Attribute Quality

```python
from tango import AttrQuality
from tango_checkup.decorators import with_attributes

@with_attributes("sys/tg_test/1/ampli")
def test_attr_quality(attribute):
    """
    Test the quality of the Ampli attribute.
    """
    assert attribute.quality == AttrQuality.ATTR_VALID, "Do something about it!"
```

### Example 3: Using Custom Fixtures

```python
import pytest
from tango_checkup.getters import get_proxy

@pytest.fixture
def custom_device():
    """Custom fixture to get a specific TANGO device proxy."""
    return get_proxy("sys/tg_test/1")

def test_custom_device_state(custom_device):
    """Test that the custom device is not in FAULT state."""
    # Here we don't need to decorate the function anymore
    # which might be convenient if you're writing many tests
    assert custom_device.State() != DevState.FAULT, "Device is in FAULT state!"
```

An example test suite is available in the `examples/` folder. Assuming that you have a Tango control system available, you can run it with

    pytest examples/
