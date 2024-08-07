import os

# Pytest config file.

## Environment variable used by the HTML report. Set it to e.g. the name of your beamline.
os.environ["PROJECT"] = "playground"

# Any other local configuration, fixtures etc could be added in this file.
# The rest is an example.


def pytest_configure(config):
    """
    Configure pytest settings and add custom markers.

    This function customizes the pytest configuration by adding custom markers
    for test categorization. These markers can be used to selectively run tests
    based on their category.

    Args:
        config: The pytest configuration object.
    """
    # Add a custom marker for tests related to branch A.
    config.addinivalue_line("markers", "branch_a: Stuff in A branch.")

    # Add a custom marker for tests related to branch B.
    config.addinivalue_line("markers", "branch_b: Stuff in B branch.")
