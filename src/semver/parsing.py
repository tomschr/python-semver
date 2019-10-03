#
#
#

from .utils import format_version, _REGEX, _compare_by_keys


def parse(version):
    """Parse version to major, minor, patch, pre-release, build parts.

    :param version: version string
    :return: dictionary with the keys 'build', 'major', 'minor', 'patch',
             and 'prerelease'. The prerelease or build keys can be None
             if not provided
    :rtype: dict

    >>> import semver
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
    match = _REGEX.match(version)
    if match is None:
        raise ValueError('%s is not valid SemVer string' % version)

    version_parts = match.groupdict()

    version_parts['major'] = int(version_parts['major'])
    version_parts['minor'] = int(version_parts['minor'])
    version_parts['patch'] = int(version_parts['patch'])

    return version_parts


def parse_version_info(version):
    """Parse version string to a VersionInfo instance.

    :param version: version string
    :return: a :class:`VersionInfo` instance
    :rtype: :class:`VersionInfo`

    >>> import semver
    >>> version_info = semver.parse_version_info("3.4.5-pre.2+build.4")
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
    from .version import VersionInfo

    parts = parse(version)
    version_info = VersionInfo(
            parts['major'], parts['minor'], parts['patch'],
            parts['prerelease'], parts['build'])

    return version_info


def compare(ver1, ver2):
    """Compare two versions

    :param ver1: version string 1
    :param ver2: version string 2
    :return: The return value is negative if ver1 < ver2,
             zero if ver1 == ver2 and strictly positive if ver1 > ver2
    :rtype: int

    >>> import semver
    >>> semver.compare("1.0.0", "2.0.0")
    -1
    >>> semver.compare("2.0.0", "1.0.0")
    1
    >>> semver.compare("2.0.0", "2.0.0")
    0
    """

    v1, v2 = parse(ver1), parse(ver2)

    return _compare_by_keys(v1, v2)


def match(version, match_expr):
    """Compare two versions through a comparison

    :param str version: a version string
    :param str match_expr: operator and version; valid operators are
          <   smaller than
          >   greater than
          >=  greator or equal than
          <=  smaller or equal than
          ==  equal
          !=  not equal
    :return: True if the expression matches the version, otherwise False
    :rtype: bool

    >>> import semver
    >>> semver.match("2.0.0", ">=1.0.0")
    True
    >>> semver.match("1.0.0", ">1.0.0")
    False
    """
    prefix = match_expr[:2]
    if prefix in ('>=', '<=', '==', '!='):
        match_version = match_expr[2:]
    elif prefix and prefix[0] in ('>', '<'):
        prefix = prefix[0]
        match_version = match_expr[1:]
    else:
        raise ValueError("match_expr parameter should be in format <op><ver>, "
                         "where <op> is one of "
                         "['<', '>', '==', '<=', '>=', '!=']. "
                         "You provided: %r" % match_expr)

    possibilities_dict = {
        '>': (1,),
        '<': (-1,),
        '==': (0,),
        '!=': (-1, 1),
        '>=': (0, 1),
        '<=': (-1, 0)
    }

    possibilities = possibilities_dict[prefix]
    cmp_res = compare(version, match_version)

    return cmp_res in possibilities


def max_ver(ver1, ver2):
    """Returns the greater version of two versions

    :param ver1: version string 1
    :param ver2: version string 2
    :return: the greater version of the two
    :rtype: :class:`VersionInfo`

    >>> import semver
    >>> semver.max_ver("1.0.0", "2.0.0")
    '2.0.0'
    """
    cmp_res = compare(ver1, ver2)
    if cmp_res == 0 or cmp_res == 1:
        return ver1
    else:
        return ver2


def min_ver(ver1, ver2):
    """Returns the smaller version of two versions

    :param ver1: version string 1
    :param ver2: version string 2
    :return: the smaller version of the two
    :rtype: :class:`VersionInfo`

    >>> import semver
    >>> semver.min_ver("1.0.0", "2.0.0")
    '1.0.0'
    """
    cmp_res = compare(ver1, ver2)
    if cmp_res == 0 or cmp_res == -1:
        return ver1
    else:
        return ver2


def finalize_version(version):
    """Remove any prerelease and build metadata from the version

    :param version: version string
    :return: the finalized version string
    :rtype: str

    >>> finalize_version('1.2.3-rc.5')
    '1.2.3'
    """
    verinfo = parse(version)
    return format_version(verinfo['major'], verinfo['minor'], verinfo['patch'])
