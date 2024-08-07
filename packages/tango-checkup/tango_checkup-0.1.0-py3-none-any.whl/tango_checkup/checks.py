import tango
import pytest


# ==== Check functions ====
# Some convenient ways to do specific asserts


def check_tango_host(tango_host: str) -> None:
    """
    Check the TANGO_HOST env variable.

    This test should be at the top of each test file! It prevents the whole suite from
    running if it's run in the wrong environment.
    This can be overridden by setting the TANGO_HOST, if really needed.

    Args:
        tango_host: The expected TANGO_HOST environment variable.
    """
    current_tango_host = tango.ApiUtil.get_env_var("TANGO_HOST")
    if current_tango_host.lower() != tango_host.lower():
        pytest.exit(
            f"Wrong tango host! Expected '{tango_host}', got '{current_tango_host}'!",
            returncode=10,
        )


def check_device_state(
    device: tango.DeviceProxy,
    expected_state: tango.DevState | set[tango.DevState],
    comment: str | None = None,
) -> None:
    """
    Check that the given device is in the given state or set of states.
    Includes status message on failure, and gives special error for FAULT state.

    Example: check_device_state(device, {DevState.ON, DevState.RUNNING})

    Args:
        device: The Tango device proxy to check.
        expected_state: The expected state or set of states.
        comment: Additional comment to include in the failure message.
    """
    if isinstance(expected_state, tango.DevState):
        expected_states = set([expected_state])
    else:
        expected_states = expected_state
    current_state = device.State()
    if (
        tango.DevState.FAULT not in expected_states
        and current_state == tango.DevState.FAULT
    ):
        status = device.Status()
        pytest.fail(
            f"Device {device.dev_name()} is in FAULT state! Its status is:\n{status}"
        )
    if current_state not in expected_states:
        if len(expected_states) == 1:
            (expected_state,) = expected_states
            pytest.fail(
                f"Device {device.dev_name()} is in state {current_state}, expected {expected_state}."
                + (" " + comment if comment else "")
            )
        else:
            pytest.fail(
                f"Device {device.dev_name()} is in state {current_state}, expected one of {', '.join(expected_states)}."
                + (" " + comment if comment else "")
            )


def check_not_device_state(
    device: tango.DeviceProxy,
    unexpected_state: tango.DevState,
    comment: str | None = None,
) -> None:
    """
    Check that the given device is not in the given unexpected state.
    Includes status message on failure.

    Args:
        device: The Tango device proxy to check.
        unexpected_state: The state that the device should not be in.
        comment: Additional comment to include in the failure message.
    """
    current_state = device.State()
    if current_state == unexpected_state:
        status = device.Status()
        if status:
            status = status.splitlines()[0]  # Just take the first line
        pytest.fail(
            f"Device {device.dev_name()} is in undesired state {unexpected_state}. Status message: '{status}'."
            + (" " + comment if comment else "")
        )
