#
#
#

from .parsing import parse
from .utils import _LAST_NUMBER
from .utils import format_version


def _increment_string(string):
    """
    Look for the last sequence of number(s) in a string and increment, from:
    http://code.activestate.com/recipes/442460-increment-numbers-in-a-string/#c1
    """
    match = _LAST_NUMBER.search(string)
    if match:
        next_ = str(int(match.group(1)) + 1)
        start, end = match.span(1)
        string = string[:max(end - len(next_), start)] + next_ + string[end:]
    return string


def bump_major(version):
    """Raise the major part of the version

    :param: version string
    :return: the raised version string
    :rtype: str

    >>> import semver
    >>> semver.bump_major("3.4.5")
    '4.0.0'
    """
    verinfo = parse(version)
    return format_version(verinfo['major'] + 1, 0, 0)


def bump_minor(version):
    """Raise the minor part of the version

    :param: version string
    :return: the raised version string
    :rtype: str

    >>> import semver
    >>> semver.bump_minor("3.4.5")
    '3.5.0'
    """
    verinfo = parse(version)
    return format_version(verinfo['major'], verinfo['minor'] + 1, 0)


def bump_patch(version):
    """Raise the patch part of the version

    :param: version string
    :return: the raised version string
    :rtype: str

    >>> import semver
    >>> semver.bump_patch("3.4.5")
    '3.4.6'
    """
    verinfo = parse(version)
    return format_version(verinfo['major'], verinfo['minor'],
                          verinfo['patch'] + 1)


def bump_prerelease(version, token='rc'):
    """Raise the prerelease part of the version

    :param version: version string
    :param token: defaults to 'rc'
    :return: the raised version string
    :rtype: str

    >>> bump_prerelease('3.4.5', 'dev')
    '3.4.5-dev.1'
    """
    verinfo = parse(version)
    verinfo['prerelease'] = _increment_string(
        verinfo['prerelease'] or (token or 'rc') + '.0'
    )
    return format_version(verinfo['major'], verinfo['minor'], verinfo['patch'],
                          verinfo['prerelease'])


def bump_build(version, token='build'):
    """Raise the build part of the version

    :param version: version string
    :param token: defaults to 'build'
    :return: the raised version string
    :rtype: str

    >>> bump_build('3.4.5-rc.1+build.9')
    '3.4.5-rc.1+build.10'
    """
    verinfo = parse(version)
    verinfo['build'] = _increment_string(
        verinfo['build'] or (token or 'build') + '.0'
    )
    return format_version(verinfo['major'], verinfo['minor'], verinfo['patch'],
                          verinfo['prerelease'], verinfo['build'])
