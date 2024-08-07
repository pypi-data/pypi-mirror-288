# Checkup playground with examples
# Assumes that you have a local Tango setup with standard TangoTest device

from tango import DevState, AttrQuality
import pytest
from tango import DeviceProxy, DeviceAttribute

from tango_checkup.decorators import (
    with_devices,
    with_attributes,
    with_devices_matching,
)
from tango_checkup.decorators import critical
from tango_checkup.getters import get_attribute
from tango_checkup.checks import check_device_state, check_not_device_state
from tango_checkup.checks import check_tango_host  # noqa

# It's a good idea to put "check_tango_host" in your test suite.
# It prevents running in the wrong control system, which would be confusing.
# (Disabled here, so that this playground test suite is always runnable)
# check_tango_host("my-tango-host:10000")


# Test will run once for *each* listed device
@with_devices(["sys/tg_test/1", "sys/database/2", "sys/tg_test/17"])
def test_device_is_ok(device: DeviceProxy) -> None:
    """
    Test that the device is not in FAULT state.
    """
    check_not_device_state(
        device,
        DevState.FAULT,  # The undesired state
        "Try turning it on and off again.",  # A helpful message for when the test fails
    )


@with_devices(["sys/tg_test/1"])
def test_device_ping(device: DeviceProxy) -> None:
    """
    Test that the device responds to ping reasonably quickly.
    """
    # The device argument is a DeviceProxy instance, so you can also do stuff
    # 'manually' with it. But you won't get quite as nice output.
    assert device.ping() < 50, "Check network connection"


# Test will run on all listed attributes
# The "critical" decorator affects the test grouping in the report
@critical
@with_attributes(["sys/tg_test/1/ampli"])
def test_attr_is_ok(attribute: DeviceAttribute) -> None:
    """
    Test that the ampli attribute is tuned.
    """
    # Check that the attribute's value is in range
    assert 60 < attribute < 67, "Tune the Ampli!"


# Mark test as related to a specific part. This can be useful, since it's possible
# to filter the tests and e.g. only run tests for the operational branch.
@pytest.mark.branch_b
@with_attributes(["sys/tg_test/1/ampli"])
def test_attr_is_ok2(attribute: DeviceAttribute) -> None:
    """
    Test that the ampli attribute is tuned.
    """
    assert 160 < attribute < 167, "Ampli isn't well tuned!"


@with_attributes(["sys/tg_test/1/ampli"])
def test_attr_quality(attribute: DeviceAttribute) -> None:
    """
    Test the quality of the Ampli attribute.
    """
    # The attribute argument is a DeviceAttribute object, so you can also
    # access the usual things on it, if needed.
    assert attribute.quality == AttrQuality.ATTR_VALID, "Do something about it!"


# You don't have to use the decorators, they are for convenience
@pytest.mark.branch_a
def test_compare_attr2() -> None:
    """
    Test that the Ampli attribute is less than the float_scalar attribute.
    """
    ampli: DeviceAttribute = get_attribute("sys/tg_test/1/ampli")
    float_scalar: DeviceAttribute = get_attribute("sys/tg_test/1/float_scalar")
    assert ampli < float_scalar, "Devices aren't aligned!"


# This test will run on all devices of class TangoTest
@with_devices_matching(devclass="TangoTest")
def test_device_on(device: DeviceProxy) -> None:
    """
    Test that the device is in RUNNING state.
    """
    check_device_state(device, DevState.RUNNING, "Test device is not RUNNING!")


# It's also possible to parameterize with more complex data, which might
# be handy e.g. if you need to check pressures of many gauges. You can use
# any names for the variables apart from attribute (which uses the fixture).
@with_attributes(
    dict(attribute="sys/tg_test/1/ampli", threshold=3),
    dict(attribute="sys/tg_test/1/double_scalar", threshold=100),
)
def test_vacuum_gauge_pressure(attribute: DeviceAttribute, threshold: float) -> None:
    """
    Test that the vacuum gauge pressure is within the threshold.
    """
    assert attribute <= threshold, "Contact beamline manager."
