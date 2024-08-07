#!/usr/bin/env python3

import argparse
from datetime import datetime
import json
import re
from typing import List, Dict, Any, TextIO, Optional

from jinja2 import Template


class TestResult:
    """Class to hold summary information for a test result."""

    def __init__(self, name: str) -> None:
        """
        Initialize a TestResult instance.

        Args:
            name: The name of the test.
        """
        self.name: str = name
        self.importance: str = "potential"
        self.outcome: str = "None"
        self.description: str = "None"
        self.long_descr: str = ""
        self.message: str = "None"
        self.assertion: str = ""
        self.duration: float = 0.0
        self.beamline: Optional[str] = None

    def __str__(self) -> str:
        """
        Return a string representation of the test result.

        Returns:
            A formatted string summarizing the test result.
        """
        s = f"{self.description} [{self.importance}/{self.outcome}]: "
        if self.assertion and self.message:
            s += f" Reason: {self.assertion}; Action: {self.message}"
        else:
            s += " ".join([self.message, self.assertion])
        return s


def make_taranta_links(text: str, beamline: str) -> str:
    """
    Search in text for device and attribute names and make links to the corresponding Taranta page.

    Args:
        text: The text to search for device and attribute names.
        beamline: The name of the beamline.

    Returns:
        The text with device and attribute names replaced by HTML links.
    """
    # use regular expressions from Achtung evaluator, modified to provide a group:
    ATTRIBUTE_PREFIX_RE = r"tango://[^:]+:\d+/"
    DEVICE_RE = rf"((?:{ATTRIBUTE_PREFIX_RE})?[\-\w.@_]+/[\-\w.@_]+/[\-\w.@_]+)"
    TEST_PATH_RE = (
        rf"((?:{ATTRIBUTE_PREFIX_RE})?[\-\w.@_]+/[\-\w.@_]+/test_[\-\w.@_]+\.py)"
    )

    def replace(var: re.Match) -> str:
        """
        Skipping paths to test files, return HTML links to matches.

        Args:
            var: The regex match object.

        Returns:
            The original match or an HTML link.
        """
        if re.fullmatch(TEST_PATH_RE, var.group()):
            # it is a test path, skip
            return var.group()
        return f"<a href='https://taranta.maxiv.lu.se/{beamline}/devices/{var.group(1)}/server'>{var.group(1)}</a>"

    # replace the devices with links to the device server
    # NOTE: this does not play well with URLs or repeated replacements
    text = re.sub(DEVICE_RE, replace, text, flags=re.IGNORECASE)
    return text


def get_failed_tests(data: List[Dict[str, Any]]) -> Dict[str, List[TestResult]]:
    """
    Parse the provided JSON file and extract failed tests sorted by importance.

    Args:
        data: The JSON data to parse.

    Returns:
        A dictionary of failed tests sorted by importance.
    """
    # data is stored in several records which need to be parsed individually
    tests: Dict[str, List[TestResult]] = {}
    for d in data:
        # find failed tests
        try:
            if d["outcome"] == "failed":
                nodeid = d["nodeid"]
            else:
                continue
        except KeyError:
            continue
        res = TestResult(nodeid)
        res.outcome = d["outcome"]
        # determine importance level
        if "critical" in d["keywords"]:
            res.importance = "critical"
        elif "major" in d["keywords"]:
            res.importance = "major"
        # retrieve description and remove empty lines
        description = [line for line in d["description"].splitlines() if line]
        # doc string of test (which makes up description) can have several
        # lines: only use the first
        res.description = description[0]
        if res.description == "None":
            res.description = nodeid
        # add remaining lines (if existing) to long_descr
        res.long_descr = "\n".join(description[1:])
        # retrieve message
        res.duration = d["duration"]
        try:
            msg = d["longrepr"]["reprcrash"]["message"]
        except (KeyError, TypeError):
            msg = f"Error: could not extract message for test {nodeid}"
            print(msg)
        # remove pytest prefixes
        if msg.startswith("AssertionError:"):
            assert_msg = msg.splitlines()[0][len("AssertionError:") :]
            compare_msg = msg.splitlines()[1]
            msg = compare_msg + assert_msg
            # msg = msg.removeprefix("AssertionError: ")
            msg = msg.removeprefix("assert ")
            # move trailing message appended by assert hook to beginning
            match = re.search("\nassert ", msg)
            if match:
                msg = f"{msg[match.end(0):]} {msg[0:match.start(0)]}"
        else:
            msg = msg.removeprefix("Failed: ")
        res.message = msg
        try:
            tests[res.importance].append(res)
        except KeyError:
            tests[res.importance] = [res]
        res.beamline = d.get("beamline")
    return tests


def get_log_date(data: List[Dict[str, Any]]) -> Optional[datetime]:
    """
    Parse the provided JSON file and extract the recorded date.

    Args:
        data: The JSON data to parse.

    Returns:
        The recorded date or None if not found.
    """
    # data is stored in several records which need to be parsed individually
    for d in data:
        try:
            return datetime.fromtimestamp(d["start"])
        except KeyError:
            continue
    return None


def build_report(jsonfile: TextIO, beamline: str, htmlout: str) -> str:
    """
    Build an HTML report from the provided JSON file.

    Args:
        jsonfile: The JSON log file to parse.
        beamline: The name of the beamline.
        htmlout: The name of the HTML file to write to.

    Returns:
        sThe path to the generated HTML report.
    """
    all_lines = [json.loads(line) for line in jsonfile.readlines()]
    tests = get_failed_tests(all_lines)
    date = get_log_date(all_lines)
    prios = list(tests.keys())
    beamline = beamline or tests[prios[0]][0].beamline or "unknown"
    prio = ["critical", "major", "potential"]
    print(f"Parsing {jsonfile.name} recorded on {date}")
    for p in prio:
        if p not in tests:
            tests[p] = []
            continue
        print(f"Priority: {p}")
        print("----------------------")
        for t in tests[p]:
            print(t)
        print("\n")

    # change texts to include links to devices in Taranta
    for p in prio:
        for t in tests[p]:
            for attr in ["description", "name", "long_descr", "assertion", "message"]:
                a = getattr(t, attr)
                text = make_taranta_links(a, beamline=beamline)
                setattr(t, attr, text)

    # HTML output
    print(f"Writing results to {htmlout}")
    checkup_path = __file__.rsplit("/", 1)[0]
    if date is not None:
        formatted_time = date.strftime("%c")
    else:
        formatted_time = "N/A"
    with open(checkup_path + "/templates/base.html") as f:
        tmpl = Template(f.read())
    with open(htmlout, "w") as f:
        f.write(
            tmpl.render(
                title=f"{beamline.capitalize()} Health Report",
                date=formatted_time,
                tests=tests,
            )
        )
    return htmlout


def main() -> None:
    """
    Main function to parse command-line arguments and build the report.

    This function sets up the argument parser, processes the arguments,
    and calls the build_report function with the specified options.
    """
    parser = argparse.ArgumentParser(
        description="Beamline health JSON log file parser."
    )

    parser.add_argument(
        "jsonfile", type=argparse.FileType("r"), help="The JSON log file to parse."
    )
    parser.add_argument(
        "htmlout", type=str, help="The name of the HTML file to write to."
    )
    parser.add_argument(
        "-b", "--beamline", type=str, help="The name of the beamline", default=""
    )

    args = parser.parse_args()

    build_report(args.jsonfile, args.beamline, args.htmlout)


if __name__ == "__main__":
    main()
