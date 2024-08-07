import pytest
import tango


from .hooks import *  # noqa
from .getters import ComparingDevAttr, ComparingDevProxy, get_attribute, get_proxy


# Fixtures


@pytest.fixture
def device(request: pytest.FixtureRequest) -> ComparingDevProxy:
    """Fixture to connect to a parameterized Tango device.

    Args:
        request: The pytest request object containing the parameter.

    Returns:
        The proxy object for the specified Tango device.
    """
    devname = request.param
    return get_proxy(devname)


@pytest.fixture
def state(request: pytest.FixtureRequest) -> tango.DevState:
    """Fixture to get the state of a parameterized Tango device.

    Args:
        request: The pytest request object containing the parameter.

    Returns:
        The state of the specified Tango device.
    """
    devname = request.param
    proxy = get_proxy(devname)
    return proxy.State()


@pytest.fixture
def attribute(
    request: pytest.FixtureRequest,
) -> ComparingDevAttr | list[ComparingDevAttr]:
    """Fixture to connect to a parameterized Tango attribute.

    Args:
        request: The pytest request object containing the parameter.

    Returns:
        The attribute object for the specified Tango attribute.
    """
    attrname = request.param
    if isinstance(attrname, list):
        return [get_attribute(a) for a in attrname]
    return get_attribute(attrname)


# Functions to customize failed assert output
def get_op_fail_str(op: str, reverse: bool = False) -> str:
    """Get the failure description for an operator.

    Args:
        op: The operator used in the comparison.
        reverse: If True, the equation is read backwards. Defaults to False.

    Returns:
        The failure description for the operator.
    """
    if op == "==":
        opfail = "not equal to"
    elif op == "!=":
        opfail = "equal to"
    elif ("<" in op and not reverse) or (">" in op and reverse):
        opfail = "greater than (or equal to)"
    elif (">" in op and not reverse) or ("<" in op and reverse):
        opfail = "less than (or equal to)"
    else:
        opfail = f"not '{op}'"
    return opfail


def format_attr_value(attr: ComparingDevAttr) -> str:
    """Parse an attribute config and return format and unit.

    Args:
        attr: The attribute to format.

    Returns:
        The formatted attribute value with its unit.
    """
    val = attr.value
    conf = attr._config
    fmt = conf.format
    if fmt.startswith("%") and (fmt.endswith("f") or fmt.endswith("d")):
        val = format(val, fmt[1:])
    return f"{val}{conf.unit}".strip()


def pytest_assertrepr_compare(op: str, left: object, right: object) -> list[str]:
    """Define a custom explanation for failed assumptions.

    Args:
        op: The operator used in the comparison.
        left: The left-hand side of the comparison.
        right: The right-hand side of the comparison.

    Returns:
        A list containing the custom explanation for the failed assertion.
    """
    if isinstance(left, ComparingDevAttr) ^ isinstance(right, ComparingDevAttr):
        # only ONE side is a Tango attribute
        if isinstance(left, ComparingDevAttr):
            attr = left
            aval = format_attr_value(attr)
            val = right
            opfail = get_op_fail_str(op)
        elif isinstance(right, ComparingDevAttr):
            attr = right
            aval = format_attr_value(attr)
            val = left
            opfail = get_op_fail_str(op, reverse=True)
        return [
            f"The value of {attr.name} ({attr._full_name}) is {aval} which is {opfail} the expected {val}!",
        ]
    if isinstance(left, ComparingDevAttr) and isinstance(right, ComparingDevAttr):
        # BOTH sides are Tango attributes
        opfail = get_op_fail_str(op)
        lval = format_attr_value(left)
        rval = format_attr_value(right)
        return [
            f"The value of {left.name} ({left._full_name}) is {lval} "
            + f"which is {opfail} the expected {rval} of "
            + f"{right.name} ({right._full_name})!",
        ]
    if isinstance(left, ComparingDevProxy) and (
        isinstance(right, str)
        or isinstance(right, tango.DevState)
        or isinstance(right, tango._tango.DevState)
    ):
        # checking state of DS
        if isinstance(right, str):
            str_right = str
        else:
            str_right = tango.DevState.values[right].name
        if op == "==":
            return [
                f"The state of the device {left.dev_name()} is {left.State()} "
                + f"and not the expected state {str_right}!",
            ]
        elif op != "":
            return [
                f"The state of the device {left.dev_name()} is {left.State()} "
                + "which it is not supposed to be!",
            ]
        else:
            print(f"Operator {op} was not expected for state comparisons!")
            return [f"{left} {get_op_fail_str(op)} {right}."]

    else:
        print(
            f"Did not match any hook criteria! type(left): {type(left)}, type(right): {type(right)}"
        )
        return [f"{left} {get_op_fail_str(op)} {right}."]
