#
#
#

import collections
from functools import wraps

from .bumping import (bump_major, bump_minor, bump_patch,
                      bump_prerelease, bump_build)
from .parsing import parse_version_info
from .utils import format_version, _compare_by_keys


def comparator(operator):
    """ Wrap a VersionInfo binary op method in a type-check """
    @wraps(operator)
    def wrapper(self, other):
        comparable_types = (VersionInfo, dict, tuple)
        if not isinstance(other, comparable_types):
            raise TypeError("other type %r must be in %r"
                            % (type(other), comparable_types))
        return operator(self, other)
    return wrapper


def _to_dict(obj):
    if isinstance(obj, VersionInfo):
        return obj._asdict()
    elif isinstance(obj, tuple):
        return VersionInfo(*obj)._asdict()
    return obj


class VersionInfo(object):
    """
    :param int major: version when you make incompatible API changes.
    :param int minor: version when you add functionality in
                      a backwards-compatible manner.
    :param int patch: version when you make backwards-compatible bug fixes.
    :param str prerelease: an optional prerelease string
    :param str build: an optional build string
    """
    __slots__ = ('_major', '_minor', '_patch', '_prerelease', '_build')

    def __init__(self, major, minor=0, patch=0, prerelease=None, build=None):
        self._major = int(major)
        self._minor = int(minor)
        self._patch = int(patch)
        self._prerelease = None if prerelease is None else str(prerelease)
        self._build = None if build is None else str(build)

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        raise AttributeError("attribute 'major' is readonly")

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        raise AttributeError("attribute 'minor' is readonly")

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        raise AttributeError("attribute 'patch' is readonly")

    @property
    def prerelease(self):
        return self._prerelease

    @prerelease.setter
    def prerelease(self, value):
        raise AttributeError("attribute 'prerelease' is readonly")

    @property
    def build(self):
        return self._build

    @build.setter
    def build(self, value):
        raise AttributeError("attribute 'build' is readonly")

    def _astuple(self):
        return (self.major, self.minor, self.patch,
                self.prerelease, self.build)

    def _asdict(self):
        return collections.OrderedDict((
            ("major", self.major),
            ("minor", self.minor),
            ("patch", self.patch),
            ("prerelease", self.prerelease),
            ("build", self.build)
        ))

    def __iter__(self):
        """Implement iter(self)."""
        # As long as we support Py2.7, we can't use the "yield from" syntax
        for v in self._astuple():
            yield v

    def bump_major(self):
        """Raise the major part of the version, return a new object
           but leave self untouched

        :return: new object with the raised major part
        :rtype: VersionInfo

        >>> import semver
        >>> ver = semver.parse_version_info("3.4.5")
        >>> ver.bump_major()
        VersionInfo(major=4, minor=0, patch=0, prerelease=None, build=None)
        """
        return parse_version_info(bump_major(str(self)))

    def bump_minor(self):
        """Raise the minor part of the version, return a new object
           but leave self untouched

        :return: new object with the raised minor part
        :rtype: VersionInfo

        >>> import semver
        >>> ver = semver.parse_version_info("3.4.5")
        >>> ver.bump_minor()
        VersionInfo(major=3, minor=5, patch=0, prerelease=None, build=None)
        """
        return parse_version_info(bump_minor(str(self)))

    def bump_patch(self):
        """Raise the patch part of the version, return a new object
           but leave self untouched

        :return: new object with the raised patch part
        :rtype: VersionInfo

        >>> import semver
        >>> ver = semver.parse_version_info("3.4.5")
        >>> ver.bump_patch()
        VersionInfo(major=3, minor=4, patch=6, prerelease=None, build=None)
        """
        return parse_version_info(bump_patch(str(self)))

    def bump_prerelease(self, token='rc'):
        """Raise the prerelease part of the version, return a new object
           but leave self untouched

        :param token: defaults to 'rc'
        :return: new object with the raised prerelease part
        :rtype: str

        >>> import semver
        >>> ver = semver.parse_version_info("3.4.5-rc.1")
        >>> ver.bump_prerelease()
        VersionInfo(major=3, minor=4, patch=5, prerelease='rc.2', \
build=None)
        """
        return parse_version_info(bump_prerelease(str(self), token))

    def bump_build(self, token='build'):
        """Raise the build part of the version, return a new object
           but leave self untouched

        :param token: defaults to 'build'
        :return: new object with the raised build part
        :rtype: str

        >>> import semver
        >>> ver = semver.parse_version_info("3.4.5-rc.1+build.9")
        >>> ver.bump_build()
        VersionInfo(major=3, minor=4, patch=5, prerelease='rc.1', \
build='build.10')
        """
        return parse_version_info(bump_build(str(self), token))

    @comparator
    def __eq__(self, other):
        return _compare_by_keys(self._asdict(), _to_dict(other)) == 0

    @comparator
    def __ne__(self, other):
        return _compare_by_keys(self._asdict(), _to_dict(other)) != 0

    @comparator
    def __lt__(self, other):
        return _compare_by_keys(self._asdict(), _to_dict(other)) < 0

    @comparator
    def __le__(self, other):
        return _compare_by_keys(self._asdict(), _to_dict(other)) <= 0

    @comparator
    def __gt__(self, other):
        return _compare_by_keys(self._asdict(), _to_dict(other)) > 0

    @comparator
    def __ge__(self, other):
        return _compare_by_keys(self._asdict(), _to_dict(other)) >= 0

    def __repr__(self):
        s = ", ".join("%s=%r" % (key, val)
                      for key, val in self._asdict().items())
        return "%s(%s)" % (type(self).__name__, s)

    def __str__(self):
        return format_version(*(self._astuple()))

    def __hash__(self):
        return hash(self._astuple())

    @staticmethod
    def parse(version):
        """Parse version string to a VersionInfo instance.

        >>> from semver import VersionInfo
        >>> VersionInfo.parse('3.4.5-pre.2+build.4')
        VersionInfo(major=3, minor=4, patch=5, \
prerelease='pre.2', build='build.4')

        :param version: version string
        :return: a :class:`VersionInfo` instance
        :rtype: :class:`VersionInfo`
        """
        return parse_version_info(version)
