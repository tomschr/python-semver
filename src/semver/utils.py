import inspect
from functools import partial, wraps
from types import FrameType
from typing import Callable, Union, cast
import warnings

from .types import F, String

__all__ = ("cmp", "deprecated", "ensure_str")


def deprecated(
    func: F = None,
    replace: str = None,
    version: str = None,
    category=DeprecationWarning,
) -> Union[Callable[..., F], partial]:
    """
    Decorates a function to output a deprecation warning.

    :param func: the function to decorate
    :param replace: the function to replace (use the full qualified
        name like ``semver.VersionInfo.bump_major``.
    :param version: the first version when this function was deprecated.
    :param category: allow you to specify the deprecation warning class
        of your choice. By default, it's  :class:`DeprecationWarning`, but
        you can choose :class:`PendingDeprecationWarning` or a custom class.
    :return: decorated function which is marked as deprecated
    """

    if func is None:
        return partial(deprecated, replace=replace, version=version, category=category)

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable[..., F]:
        msg_list = ["Function '{m}.{f}' is deprecated."]

        if version:
            msg_list.append("Deprecated since version {v}. ")
        msg_list.append("This function will be removed in semver 3.")
        if replace:
            msg_list.append("Use {r!r} instead.")
        else:
            msg_list.append("Use the respective 'semver.VersionInfo.{r}' instead.")

        f = cast(F, func).__qualname__
        r = replace or f

        frame = cast(FrameType, cast(FrameType, inspect.currentframe()).f_back)

        msg = " ".join(msg_list)
        warnings.warn_explicit(
            msg.format(m=func.__module__.split(".")[0], f=f, r=r, v=version),
            category=category,
            filename=inspect.getfile(frame.f_code),
            lineno=frame.f_lineno,
        )
        # As recommended in the Python documentation
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        # better remove the interpreter stack:
        del frame
        return func(*args, **kwargs)  # type: ignore

    return wrapper


def cmp(a, b):
    """Return negative if a<b, zero if a==b, positive if a>b."""
    return (a > b) - (a < b)


def ensure_str(s: String, encoding="utf-8", errors="strict") -> str:
    # Taken from six project
    """
    Coerce *s* to `str`.

    * `str` -> `str`
    * `bytes` -> decoded to `str`

    :param s: the string to convert
    :type s: str | bytes
    :param encoding: the encoding to apply, defaults to "utf-8"
    :type encoding: str
    :param errors: set a different error handling scheme,
       defaults to "strict".
       Other possible values are `ignore`, `replace`, and
       `xmlcharrefreplace` as well as any other name
       registered with :func:`codecs.register_error`.
    :type errors: str
    :raises TypeError: if ``s`` is not str or bytes type
    :return: the converted string
    :rtype: str
    """
    if isinstance(s, bytes):
        s = s.decode(encoding, errors)
    elif not isinstance(s, String.__args__):  # type: ignore
        raise TypeError("not expecting type '%s'" % type(s))
    return s
