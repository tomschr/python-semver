from .utils import deprecated
from .types import String
from .versioninfo import VersionInfo


__all__ = (
    "bump_build",
    "bump_major",
    "bump_minor",
    "bump_patch",
    "bump_prerelease",
    "compare",
    "finalize_version",
    "format_version",
    "match",
    "max_ver",
    "min_ver",
    "parse",
    "parse_version_info",
    "replace",
)


@deprecated(version="2.10.0")
def parse(version):
    """
    Parse version to major, minor, patch, pre-release, build parts.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.parse` instead.

    :param version: version string
    :return: dictionary with the keys 'build', 'major', 'minor', 'patch',
             and 'prerelease'. The prerelease or build keys can be None
             if not provided

    >>> ver = semver.parse('3.4.5-pre.2+build.4')
    >>> ver['major']
    3
    >>> ver['minor']
    4
    >>> ver['patch']
    5
    >>> ver['prerelease']
    'pre.2'
    >>> ver['build']
    'build.4'
    """
    return VersionInfo.parse(version).to_dict()


@deprecated(replace="semver.VersionInfo.parse", version="2.10.0")
def parse_version_info(version):
    """
    Parse version string to a VersionInfo instance.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.parse` instead.

    .. versionadded:: 2.7.2
       Added :func:`semver.parse_version_info`

    :param version: version string
    :return: a :class:`VersionInfo` instance

    >>> version_info = semver.VersionInfo.parse("3.4.5-pre.2+build.4")
    >>> version_info.major
    3
    >>> version_info.minor
    4
    >>> version_info.patch
    5
    >>> version_info.prerelease
    'pre.2'
    >>> version_info.build
    'build.4'
    """
    return VersionInfo.parse(version)


@deprecated(version="2.10.0")
def compare(ver1, ver2):
    """
    Compare two versions strings.

    :param ver1: version string 1
    :param ver2: version string 2
    :return: The return value is negative if ver1 < ver2,
             zero if ver1 == ver2 and strictly positive if ver1 > ver2

    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0
    """
    v1 = VersionInfo.parse(ver1)
    return v1.compare(ver2)


@deprecated(version="2.10.0")
def match(version, match_expr):
    """
    Compare two versions strings through a comparison.

    :param version: a version string
    :param match_expr: operator and version; valid operators are
          <   smaller than
          >   greater than
          >=  greator or equal than
          <=  smaller or equal than
          ==  equal
          !=  not equal
    :return: True if the expression matches the version, otherwise False

    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False
    """
    ver = VersionInfo.parse(version)
    return ver.match(match_expr)


@deprecated(replace="max", version="2.10.2")
def max_ver(ver1, ver2):
    """
    Returns the greater version of two versions strings.

    :param ver1: version string 1
    :param ver2: version string 2
    :return: the greater version of the two

    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    """
    if isinstance(ver1, String.__args__):
        ver1 = VersionInfo.parse(ver1)
    elif not isinstance(ver1, VersionInfo):
        raise TypeError()
    cmp_res = ver1.compare(ver2)
    if cmp_res >= 0:
        return str(ver1)
    else:
        return ver2


@deprecated(replace="min", version="2.10.2")
def min_ver(ver1, ver2):
    """
    Returns the smaller version of two versions strings.

    :param ver1: version string 1
    :param ver2: version string 2
    :return: the smaller version of the two

    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'
    """
    ver1 = VersionInfo.parse(ver1)
    cmp_res = ver1.compare(ver2)
    if cmp_res <= 0:
        return str(ver1)
    else:
        return ver2


@deprecated(replace="str(versionobject)", version="2.10.0")
def format_version(major, minor, patch, prerelease=None, build=None):
    """
    Format a version string according to the Semantic Versioning specification.

    .. deprecated:: 2.10.0
       Use ``str(VersionInfo(VERSION)`` instead.

    :param major: the required major part of a version
    :param minor: the required minor part of a version
    :param patch: the required patch part of a version
    :param prerelease: the optional prerelease part of a version
    :param build: the optional build part of a version
    :return: the formatted string

    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'
    """
    return str(VersionInfo(major, minor, patch, prerelease, build))


@deprecated(version="2.10.0")
def bump_major(version):
    """
    Raise the major part of the version string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.bump_major` instead.

    :param: version string
    :return: the raised version string

    >>> semver.bump_major("3.4.5")
    '4.0.0'
    """
    return str(VersionInfo.parse(version).bump_major())


@deprecated(version="2.10.0")
def bump_minor(version):
    """
    Raise the minor part of the version string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.bump_minor` instead.

    :param: version string
    :return: the raised version string

    >>> semver.bump_minor("3.4.5")
    '3.5.0'
    """
    return str(VersionInfo.parse(version).bump_minor())


@deprecated(version="2.10.0")
def bump_patch(version):
    """
    Raise the patch part of the version string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.bump_patch` instead.

    :param: version string
    :return: the raised version string

    >>> semver.bump_patch("3.4.5")
    '3.4.6'
    """
    return str(VersionInfo.parse(version).bump_patch())


@deprecated(version="2.10.0")
def bump_prerelease(version, token="rc"):
    """
    Raise the prerelease part of the version string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.bump_prerelease` instead.

    :param version: version string
    :param token: defaults to 'rc'
    :return: the raised version string

    >>> semver.bump_prerelease('3.4.5', 'dev')
    '3.4.5-dev.1'
    """
    return str(VersionInfo.parse(version).bump_prerelease(token))


@deprecated(version="2.10.0")
def bump_build(version, token="build"):
    """
    Raise the build part of the version string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.bump_build` instead.

    :param version: version string
    :param token: defaults to 'build'
    :return: the raised version string

    >>> semver.bump_build('3.4.5-rc.1+build.9')
    '3.4.5-rc.1+build.10'
    """
    return str(VersionInfo.parse(version).bump_build(token))


@deprecated(version="2.10.0")
def finalize_version(version):
    """
    Remove any prerelease and build metadata from the version string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.finalize_version` instead.

    .. versionadded:: 2.7.9
       Added :func:`finalize_version`

    :param version: version string
    :return: the finalized version string

    >>> semver.finalize_version('1.2.3-rc.5')
    '1.2.3'
    """
    verinfo = VersionInfo.parse(version)
    return str(verinfo.finalize_version())


@deprecated(version="2.10.0")
def replace(version, **parts):
    """
    Replace one or more parts of a version and return the new string.

    .. deprecated:: 2.10.0
       Use :func:`semver.VersionInfo.replace` instead.

    .. versionadded:: 2.9.0
       Added :func:`replace`

    :param version: the version string to replace
    :param parts: the parts to be updated. Valid keys are:
      ``major``, ``minor``, ``patch``, ``prerelease``, or ``build``
    :return: the replaced version string
    :raises TypeError: if ``parts`` contains invalid keys

    >>> import semver
    >>> semver.replace("1.2.3", major=2, patch=10)
    '2.2.10'
    """
    return str(VersionInfo.parse(version).replace(**parts))
