import inspect
import pytest
import re
import sys

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
            for clsname, method in inspect.getmembers(obj, isok):
                if clsname.startswith("_"):
                    continue
                yield method  # (clsname, method)
        # Make sure we only investigate functions from our modules:
        if obj.__module__.startswith(module.__name__):
            yield obj  # (name, obj)

    # yield from (func  for name, func in members if not func.__module__.startswith(semver.__name__))


PARAMRE = re.compile(r":param\s+(?P<type>\w+\s+)?(?P<name>\w+)\s?:")
OBJECTS_IN_SEMVER = list(getfunctions())
if sys.version[0] == "3":
    IDS = ["{o.__module__ }.{o.__qualname__}".format(o=obj) for obj in OBJECTS_IN_SEMVER]
else:
    IDS = ["{o.__name__}".format(o=obj) for obj in OBJECTS_IN_SEMVER]


def extractparamsfromdoc(doc):
    """
    Extracts all described parameters found in a ':param <NAME>:' line.

    :param doc: the docstring
    """
    return set(name for _, name in PARAMRE.findall(doc))


def extractparamsfromfunc(obj):
    """
    Extracts all arguments from function, regardless if it's a "normal"
    argument, variable args or keyword arguments.

    :param obj: the function object
    """
    # Check if function/object is decorated.
    # If yes, use the original function instead
    if hasattr(obj, "__wrapped__"):
        obj = obj.__wrapped__

    source = inspect.getsource(obj)
    # source = source.split("\n")[0]
    # If we find a comment "# doctest: off" directly after the
    # function definition, we don't investigate it further:
    if re.search(r"#\s*doctest:\s*(off)", source):
        return set()

    spec = inspect.getfullargspec(obj)
    varargs = [] if spec.varargs is None else [spec.varargs]
    varkw = [] if spec.varkw is None else [spec.varkw]
    # Remove "self" as first argument:
    if spec.args.count("self") and "self" == spec.args[0]:
        spec.args.remove("self")
    if inspect.ismethod(obj) and spec.args.count("cls"):
        # Inside a classmethod, we don't document cls
        spec.args.remove("cls")
    return set(spec.args + varargs + varkw)


def find_missing_args(func):
    """
    Find the missing arguments in docstring of a function which is not
    documented.

    :param func: the function object
    :return: a set containing all missing arguments
    """
    allargs = extractparamsfromfunc(func)
    argsfromdoc = extractparamsfromdoc(func.__doc__)
    return argsfromdoc ^ allargs


## ------------------------------------


@pytest.mark.parametrize("func", OBJECTS_IN_SEMVER, ids=IDS)
def test_if_docstring_is_available(func):
    assert func.__doc__, "Need a docstring for function %r" % func.__name


@pytest.mark.parametrize("func", OBJECTS_IN_SEMVER, ids=IDS)
def test_find_missing_args_in_docstring(func):
    missing = find_missing_args(func)
    assert not missing, "Missing undocumented argument(s): {}".format(
        ", ".join(missing)
    )
