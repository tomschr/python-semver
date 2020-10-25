"""
Module to support call with :file:`__main__.py`.

Used to support the following call::

    $ python3 -m semver ...
"""

import sys
from .cli import main


if __name__ == "__main__":
    sys.exit(main())
