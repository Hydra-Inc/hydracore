import pytest

import os
import sys



def pytest_addoption(parser):
    parser.addoption(
        "-E",
        action="store",
        metavar="NAME",
        help="only run tests matching the environment NAME.",
    )


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )

    THIS = os.path.dirname(os.path.abspath(sys.argv[0]))
    sys.path.append(os.path.join(THIS,'lib','src'))
