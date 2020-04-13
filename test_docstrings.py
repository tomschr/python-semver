import inspect
from itertools import chain
import pytest
import re

import semver


def getfunctions(module=semver, skip_private=True):
    """
    Yields a tuple of name and function object for a specific module.

    :param module: the module object
    :param skip_private: flag to include (=True) functions which the name
                         starts with an underscore, or to skip them (=False)
    :yield: tuple with function name and function object
    """
    def isok(obj):
        return inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isclass(obj)

    members = inspect.getmembers(module, isok)

    for name, obj in members:
        # Skip functions which starts with underscore:
        if skip_private and name.startswith("_"):
            continue

        if inspect.isclass(obj):
            for clsname, method in  inspect.getmembers(obj, isok):
                if clsname.startswith("_"):
                    continue
                yield method  # (clsname, method)
        # Make sure we only investigate functions from our modules:
        if obj.__module__.startswith(module.__name__):
            yield obj  # (name, obj)

    # yield from (func  for name, func in members if not func.__module__.startswith(semver.__name__))
