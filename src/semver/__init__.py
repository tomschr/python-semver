"""Python helper for Semantic Versioning (http://semver.org)"""

from .versioninfo import __all__ as _ver_all
from .versioninfo import *  # noqa: F401,F403
from .deprecated import __all__ as _dep_all
from .deprecated import *  # noqa: F401,F403
from .cli import __all__ as _cli_all
from .cli import *  # noqa: F401,F403
from .utils import __all__ as _util_all
from .utils import *  # noqa: F401,F403

__version__ = "3.0.0-dev.1"
__author__ = "Kostiantyn Rybnikov"
__author_email__ = "k-bx@k-bx.com"
__maintainer__ = ["Sebastien Celles", "Tom Schraitle"]
__maintainer_email__ = "s.celles@gmail.com"
__description__ = "Python helper for Semantic Versioning (http://semver.org)"

#: Our public interface
__all__ = ["SEMVER_SPEC_VERSION"]

__all__.extend(_ver_all)
__all__.extend(_dep_all)
__all__.extend(_cli_all)
__all__.extend(_util_all)

#: Contains the implemented semver.org version of the spec
SEMVER_SPEC_VERSION = "2.0.0"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
