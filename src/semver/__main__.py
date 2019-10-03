#
# This file is part of the semver module
#
"""
Entrypoint module, in case you use `python -m semver`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

if __name__ == "__main__":
    import sys
    from .cli import main
    sys.exit(main())  # pragma: no cover
