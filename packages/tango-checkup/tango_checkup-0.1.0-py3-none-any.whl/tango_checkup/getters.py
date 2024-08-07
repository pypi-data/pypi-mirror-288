from functools import cache

import tango
import pytest


class ComparingDevAttr(tango.DeviceAttribute):
    """Wrapper class for DeviceAttribute to allow comparisons."""

    def __init__(self, attrname: str) -> None:
        self._full_name = attrname
        try:
            proxy = tango.AttributeProxy(attrname)
            self._config = proxy.get_config()
            super().__init__(proxy.read())
        except tango.ConnectionFailed as e:
            pytest.fail(e.args[-1].desc)
        except tango.DevFailed as e:
            pytest.fail(e.args[0].desc)

    def __eq__(self, other: object) -> bool:
        return self.value == other

    def __ne__(self, other: object) -> bool:
        return self.value != other

    def __gt__(self, other: int | float | str) -> bool:
        return self.value > other

    def __ge__(self, other: int | float | str) -> bool:
        return self.value >= other

    def __lt__(self, other: int | float | str) -> bool:
        return self.value < other

    def __le__(self, other: int | float | str) -> bool:
        return self.value <= other


class ComparingDevProxy(tango.DeviceProxy):
    """Wrapper class for DeviceAttribute to allow comparisons."""

    def __str__(self) -> str:
        return self.dev_name()

    # def __eq__(self, other):
    #     if isinstance(other, str):
    #         return self.State() == getattr(tango.DevState, other)
    #     else:
    #         return self.State() == other

    # def __ne__(self, other):
    #     if isinstance(other, tango.DevState):
    #         return self.State() != getattr(tango.DevState, other)
    #     else:
    #         return self.State() != other

    # def State(self):
    #     state = super().State()
    #     state._device_name = self.dev_name()
    #     return state


@cache
def get_attribute(*args: str | tango.DeviceProxy) -> ComparingDevAttr:
    """
    Reads the given attribute and returns wrapper
    Accepts either a name e.g. "sys/tg_test/1/ampi"
    or a DeviceProxy and an attribute name.
    """
    if len(args) == 2 and isinstance(args[0], tango.DeviceProxy):
        device, attr = args
        return ComparingDevAttr(f"{device}/{attr}")
    attr = args[0]
    return ComparingDevAttr(attr)


@cache
def get_proxy(devname: str) -> ComparingDevProxy:
    "Return device proxy for the given device name"
    try:
        proxy = ComparingDevProxy(devname)
        proxy.ping()
        return proxy
    except tango.ConnectionFailed as e:
        pytest.fail(e.args[-1].desc)
    except tango.DevFailed as e:
        pytest.fail(e.args[0].desc)
