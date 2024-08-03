#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import re
import os
import sys

# In this way, we are sure we are getting
# the installer's version of the library
# not the system's one
setup_dir = os.path.dirname(__file__)
sys.path.insert(0, setup_dir)

from RWFileLock import (
    __version__ as RWFileLock_version,
    __official_name__ as RWFileLock_official_name,
    __author__ as RWFileLock_author,
    __url__ as RWFileLock_url,
)

# Populating the long description
with open(os.path.join(setup_dir, "README.md"), mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

# Populating the install requirements
requirements = []
requirements_file = os.path.join(setup_dir, "requirements.txt")
if os.path.exists(requirements_file):
    with open(requirements_file, mode="r", encoding="iso-8859-1") as f:
        egg = re.compile(r"#[^#]*egg=([^=&]+)")
        for line in f.read().splitlines():
            m = egg.search(line)
            requirements.append(line if m is None else m.group(1))

repo_url = RWFileLock_url
setuptools.setup(
    name=RWFileLock_official_name,
    version=RWFileLock_version,
    author=RWFileLock_author,
    author_email="jose.m.fernandez@bsc.es",
    description="Readers / writers file lock helper class",
    license="LGPLv2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=repo_url,
    project_urls={"Source": repo_url, "Bug Tracker": f"{repo_url}/issues"},
    packages=setuptools.find_packages(),
    package_data={
        "RWFileLock": [
            "py.typed",
        ]
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
