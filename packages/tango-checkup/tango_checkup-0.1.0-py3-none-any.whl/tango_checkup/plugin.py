from pathlib import Path

from .decorators import *  # noqa
from .checks import *  # noqa
from .fixtures import *  # noqa
from .getters import *  # noqa
from .hooks import *  # noqa


DEFAULT_LOG_DIR = Path("reports")


def pytest_addoption(parser):
    group = parser.getgroup("tango-checkup")
    group.addoption(
        "--report-dir",
        type=Path,
        default=DEFAULT_LOG_DIR,
        help="Directory to store the report files in",
    )
    group.addoption(
        "--html-report", action="store_true", help="Generate an HTML report after tests"
    )
