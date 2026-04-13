import os

import uuid
import setuptools


VERSION = "0.0.6"

test_requirements = ["pytest==9.0.3", "pytest-cov==2.0.0", "flake8"]

setup = dict(
    author="Cera Davies",
    author_email="ceralena.davies@learnosity.com",
    url="https://github.com/ceralena/salt-state-graph",
    version=VERSION,
    name="salt_state_graph",
    description="a tool to represent salt states and their dependencies as an acyclic graph",
    packages=[
        "salt_state_graph",
    ],
    scripts=["bin/salt_state_graph"],
    tests_require=test_requirements,
    install_requires=["pydot"],
    include_package_data=True,
)

setuptools.setup(**setup)
