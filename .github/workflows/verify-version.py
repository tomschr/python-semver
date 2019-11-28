#!/usr/bin/env python3
"""
Compares semver version with the release branch

A release branch needs to be in the form "release/<RELEASE>" whereas
the placeholder <RELEASE> can be any string. However, this string is
currently not checked against a valid semver version.

Author: Thomas Schraitle
Date:  November 2019
"""

import sys
import os

# This adds the search path for Python packages; we assume the current
# dir and additional directories where to find the semver package:
searchpaths = [".", "src", "source"]
[sys.path.insert(0, p) for p in reversed(searchpaths)]

import semver
SEMVER = semver.__version__

# Example:
# GITHUB_REF="refs/heads/release/2.9.1-rc1"
RELEASE = os.environ.get('GITHUB_REF', '').rsplit("/", 1)[-1]


def verify():
    print("::debug::pwd={}".format(os.environ["PWD"]))

    if not RELEASE:
        print("::error::Environment variable GITHUB_REF "
              "doesn't exist or is empty")
        return 1

    if SEMVER == RELEASE:
        print("::debug::Good, semver version and branch are the same")
        return 0
    else:
        print("::error::The semver version and the release branch differ")
        print(("::error::Release branch is "
               "{!r}, but semver is {!r}".format(RELEASE, SEMVER)))
        print("::error::Adapt the version in semver.__version__ to match "
              "the release branch")
        return 2


if __name__ == "__main__":
    sys.exit(verify())
