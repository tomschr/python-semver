#!/usr/bin/env python3
"""
Checks whether the Changelog file mentions the right version.

Currently it only uses 'CHANGELOG.rst' and tries to match
it with the environment variable "GITHUB_REF" (containing,
for example, "refs/heads/release/2.99.5-rc1").

The script expects to find something like this:

  Version 2.99.5-rc1
  ==================

It matches two consecutive lines where the first line starts
with "Version". The second line can start with "==", "--",
"~~", or "^^" which is a header in RST notation.

HINT:
  If your version strings end with "(WIP)" it will NOT match!

Author: Thomas Schraitle
Date:  November 2019
"""

import sys
import os

# Example:
# GITHUB_REF="refs/heads/release/2.9.1-rc1"
RELEASE = os.environ.get("GITHUB_REF", "").rsplit("/", 1)[-1]


def verify_changelog(filename="CHANGELOG.rst"):
    """Search in filename for version string

    :param str filename: the filename of the changelog
    :return: 0 if we found a match, 1 if not
    :rtype: bool
    """
    print("::debug::Verifying %r version..." % filename)

    if not os.path.exists(filename):
        print("::error::Filename %r not found!" % filename)
    print("::debug::Found %r" % filename)

    found = False
    with open(filename, "r") as fh:
        while True:
            line1 = fh.readline()
            line2 = fh.readline()
            if not (line1 or line2):
                break
            # We are only interested in lines which are a header and
            # start with "Version":
            if not (
                line1.startswith("Version") and line2[0:2] in ("==", "--", "~~", "^^")
            ):
                continue

            ver = line1.split("Version")[1].strip()
            if ver == RELEASE:
                found = True
                break
            else:
                print("::error::Released branch doesn't match with file", filename)
                print("::error::Found version %r, but expected %r" % (ver, RELEASE))
                return 1
    if found:
        return 0
    return 1


if __name__ == "__main__":
    if not RELEASE:
        print("::error::Environment variable GITHUB_REF doesn't exist or is empty")
        sys.exit(1)
    sys.exit(verify_changelog())
