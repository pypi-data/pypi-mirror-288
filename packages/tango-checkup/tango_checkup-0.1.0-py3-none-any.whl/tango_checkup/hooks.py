import os
import pwd
import socket
from datetime import datetime
import shutil
from typing import Generator, Any

import pytest
from pytest_metadata.plugin import metadata_key
import tango
import webbrowser

from .report import build_report


# pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest settings and environment details.

    This function customizes the HTML report by removing unnecessary metadata
    and adding specific environment details such as beamline, username, and hostname.
    It also adds custom markers for test importance grouping.

    Args:
        config: The pytest configuration object.
    """
    # Customizing HTML report
    del config.stash[metadata_key]["Packages"]
    del config.stash[metadata_key]["Plugins"]
    config.stash[metadata_key]["beamline"] = "dummymax"
    config.stash[metadata_key]["username"] = pwd.getpwuid(os.getuid()).pw_name
    config.stash[metadata_key]["hostname"] = socket.gethostname()

    # Customize marker for importance grouping
    config.addinivalue_line(
        "markers", "critical: Tests that must succeed for experiments to be possible."
    )
    config.addinivalue_line(
        "markers", "major: Tests that relate to important beamline equipment."
    )
    config.addinivalue_line(
        "markers", "info: Tests that are more informational, and could be ignored."
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[Any]
) -> Generator[None, None, None]:
    """
    Enhance the pytest report data with additional information.

    This hook wrapper enhances the test report by adding a description,
    the TANGO_HOST environment variable, and the project name.

    Args:
        item: The test item object.
        call: The test call object.
    """
    outcome = yield
    if outcome is not None:
        report: Any = outcome.get_result()
        report.description = str(item.function.__doc__)
    report.tango_host = tango.ApiUtil.get_env_var("TANGO_HOST")
    report.project = os.environ.get("PROJECT", "Unknown")


def pytest_load_initial_conftests(args):
    # Make sure we generate a JSON test report to be used
    # by the HTML report
    if not any(arg.startswith("--report-log=") for arg in args):
        args.append("--report-log=/tmp/report_log.json")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    html_report = session.config.getoption("--html-report")
    if html_report:
        # Create the HTML report
        report_dir = session.config.getoption("--report-dir")
        report_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now()
        report_basename = f"checkup_report_{now.strftime('%Y%m%dT%H%M%S')}"
        report_json_orig = session.config.getoption("--report-log")
        report_log = report_dir / f"{report_basename}.json"
        shutil.copyfile(report_json_orig, report_log)
        html_report = build_report(
            report_log.open(),
            os.environ.get("PROJECT", "Unknown"),
            str(report_dir / report_basename) + ".html",
        )

        # Try to open a web browser to the report file
        try:
            webbrowser.open(html_report)
        except webbrowser.Error:
            pass
