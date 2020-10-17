import pytest
from semver import VersionInfo


@pytest.fixture
def version():
    """
    Creates a version

    :return: a version type
    :rtype: VersionInfo
    """
    return VersionInfo(
        major=1, minor=2, patch=3, prerelease="alpha.1.2", build="build.11.e0f985a"
    )
