from functools import wraps
import re
from typing import Callable, Any

import pytest
import tango


# ==== Test parametrization decorators ====


def with_attributes(
    *attributes: str | dict,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Test decorator runs test for the given attributes.

    Takes either attribute names or dicts of the form
    {"attribute": "my/attr/1/name", <argument>: <value>, ...}
    In the latter case, the test will be passed all arguments.

    Example: test that a list of gauges are all below individual
    pressure thresholds.

    @with_attributes({"attribute": "my/gauge/1/pressure", "threshold": 10-9}, ...)
    def test_gauge_pressure(attribute, threshold):
        assert attribute < threshold, "Check pressure!"
    """
    if len(attributes) == 1 and isinstance(attributes[0], (list, tuple)):
        attributes = attributes[0]

    # Handle different kinds of arguments for parametrization
    first = attributes[0]
    if isinstance(first, str):

        def inner(f: Callable[..., Any]) -> Callable[..., Any]:
            """
            Inner function to parametrize test with attribute names.
            """
            return pytest.mark.parametrize("attribute", attributes, indirect=True)(f)

        return inner
    # if isinstance(first, Sequence):
    #     def inner(f):
    #         return pytest.mark.parametrize("device,value", devices, indirect=["device"])(f)
    #     return inner
    elif isinstance(first, dict):
        if "attribute" not in first:
            raise ValueError(
                f"You must provide an 'attribute' key in the parameters! Got {first}"
            )
        names = list(first.keys())
        params = [
            pytest.param(*a.values(), id=a["attribute"])
            for a in attributes
            if isinstance(a, dict)
        ]

        def inner(f: Callable[..., Any]) -> Callable[..., Any]:
            """
            Inner function to parametrize test with attribute dicts.
            """
            return pytest.mark.parametrize(
                ",".join(names), params, indirect=["attribute"]
            )(f)

        return inner
    else:
        raise RuntimeError(
            "'with_attributes' expects either attribute names or dicts of form"
            + "'{attribute: 'a/b/c/d', '<argument>': <value>}"
        )


def with_devices_of_class(
    devclass: str, pattern: str = "*"
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that runs test for all devices of given device class.

    Args:
        devclass: The device class to filter by.
        pattern: The pattern to match device names. Defaults to "*".
    """

    def inner(f: Callable[..., Any]) -> Callable[..., Any]:
        """
        Inner function to parametrize test with devices of a given class.
        """
        # AFAIK the only way to get all devices of a class, including
        # un-exported ones.
        assert re.match(r"\w+", devclass)  # Sanity check
        db = tango.Database()
        _, devs = db.command_inout(
            "DbMySqlSelect",
            f"SELECT name FROM device WHERE class = '{devclass}' AND name LIKE '{pattern}'",
        )
        return pytest.mark.parametrize("device", devs, indirect=True)(f)

    return inner


def with_devices_matching(
    name: str = "*", devclass: str | None = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that runs tests for all devices with names matching given pattern.
    The pattern string may contain * characters, which will match anything.

    Args:
        name: The pattern to match device names. Defaults to "*".
        devclass: The device class to filter by. Defaults to None.
    """
    name = name.replace("*", "%")

    def inner(f: Callable[..., Any]) -> Callable[..., Any]:
        """
        Inner function to parametrize test with devices matching the given pattern.
        """
        if devclass:
            assert re.match(r"\w+", devclass)  # Sanity check
            db = tango.Database()
            _, devs = db.command_inout(
                "DbMySqlSelect",
                f"""
                SELECT name FROM device
                WHERE class = '{devclass}'
                AND name LIKE '{name}'
                ORDER BY name, class
                """,
            )
            return pytest.mark.parametrize("device", devs, indirect=True)(f)
        devs = db.command_inout("DbGetDeviceWideList", name)
        return pytest.mark.parametrize("device", devs, indirect=True)(f)

    return inner


def with_devices(
    *devices: str | dict,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A "smart" parametrization decorator.
    In the simplest case, it takes one or more device names.
    If you need further device specific parameters to your test, e.g.
    pressure threshold for each gauge, instead pass dicts, e.g

    @with_devices({"device": "my/pump/1", "pressure_threshold": 1e-9}, ...)
    def test_pressure_ok(device, pressure_threshold):
        ...

    Any number of parameters can be passed.
    """
    # Allow giving either a list of devices as a single argument, or
    # multiple device arguments.
    if len(devices) == 1 and isinstance(devices[0], (list, tuple)):
        devices = devices[0]

    # Handle different kinds of arguments for parametrization
    first = devices[0]
    if isinstance(first, str):

        def inner(f: Callable[..., Any]) -> Callable[..., Any]:
            """
            Inner function to parametrize test with device names.
            """
            return pytest.mark.parametrize("device", devices, indirect=True)(f)

        return inner
    # if isinstance(first, Sequence):
    #     def inner(f):
    #         return pytest.mark.parametrize("device,value", devices, indirect=["device"])(f)
    #     return inner
    elif isinstance(first, dict):
        if "device" not in first:
            raise ValueError(
                f"You must provide a 'device' key in the parameters! Got {first}"
            )
        names = list(first.keys())
        params = [
            pytest.param(*d.values(), id=d["device"])
            for d in devices
            if isinstance(d, dict)
        ]

        def inner(f: Callable[..., Any]) -> Callable[..., Any]:
            """
            Inner function to parametrize test with device dicts.
            """
            return pytest.mark.parametrize(
                ",".join(names), params, indirect=["device"]
            )(f)

        return inner
    else:
        raise RuntimeError(
            "'with_devices' expects either device names or dicts of form"
            + "'{device: 'a/b/c', '<argument>': <value>}"
        )


def with_device_states(
    *devices: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Test decorator that injects the states of the given devices.

    Args:
        devices: The devices to get states for.
    """

    def inner(f: Callable[..., Any]) -> Callable[..., Any]:
        """
        Inner function to parametrize test with device states.
        """
        return pytest.mark.parametrize("state", devices, indirect=True)(f)

    return inner


# ==== Test importance decorators ====


def major(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to mark a test as major.

    Args:
        func: The test function to decorate.
    """

    @pytest.mark.major
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def critical(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to mark a test as critical.

    Args:
        func: The test function to decorate.
    """

    @pytest.mark.critical
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def info(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to mark a test as informational.

    Args:
        func: The test function to decorate.
    """

    @pytest.mark.info
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper
