#
#
#

import re


_REGEX = re.compile(
        r"""
        ^
        (?P<major>(?:0|[1-9][0-9]*))
        \.
        (?P<minor>(?:0|[1-9][0-9]*))
        \.
        (?P<patch>(?:0|[1-9][0-9]*))
        (\-(?P<prerelease>
            (?:0|[1-9A-Za-z-][0-9A-Za-z-]*)
            (\.(?:0|[1-9A-Za-z-][0-9A-Za-z-]*))*
        ))?
        (\+(?P<build>
            [0-9A-Za-z-]+
            (\.[0-9A-Za-z-]+)*
        ))?
        $
        """, re.VERBOSE)

_LAST_NUMBER = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')


if not hasattr(__builtins__, 'cmp'):
    def cmp(a, b):
        return (a > b) - (a < b)


def _nat_cmp(a, b):
    def convert(text):
        return int(text) if re.match('^[0-9]+$', text) else text

    def split_key(key):
        return [convert(c) for c in key.split('.')]

    def cmp_prerelease_tag(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return cmp(a, b)
        elif isinstance(a, int):
            return -1
        elif isinstance(b, int):
            return 1
        else:
            return cmp(a, b)

    a, b = a or '', b or ''
    a_parts, b_parts = split_key(a), split_key(b)
    for sub_a, sub_b in zip(a_parts, b_parts):
        cmp_result = cmp_prerelease_tag(sub_a, sub_b)
        if cmp_result != 0:
            return cmp_result
    else:
        return cmp(len(a), len(b))


def _compare_by_keys(d1, d2):
    for key in ['major', 'minor', 'patch']:
        v = cmp(d1.get(key), d2.get(key))
        if v:
            return v

    rc1, rc2 = d1.get('prerelease'), d2.get('prerelease')
    rccmp = _nat_cmp(rc1, rc2)

    if not rccmp:
        return 0
    if not rc1:
        return 1
    elif not rc2:
        return -1

    return rccmp


def format_version(major, minor, patch, prerelease=None, build=None):
    """Format a version according to the Semantic Versioning specification

    :param int major: the required major part of a version
    :param int minor: the required minor part of a version
    :param int patch: the required patch part of a version
    :param str prerelease: the optional prerelease part of a version
    :param str build: the optional build part of a version
    :return: the formatted string
    :rtype: str

    >>> import semver
    >>> semver.format_version(3, 4, 5, 'pre.2', 'build.4')
    '3.4.5-pre.2+build.4'
    """
    version = "%d.%d.%d" % (major, minor, patch)
    if prerelease is not None:
        version = version + "-%s" % prerelease

    if build is not None:
        version = version + "+%s" % build

    return version
