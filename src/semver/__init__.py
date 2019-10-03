#
#
#

"""
Python helper for Semantic Versioning (http://semver.org/)
"""

__version__ = '2.8.2'
__author__ = 'Kostiantyn Rybnikov'
__author_email__ = 'k-bx@k-bx.com'
__maintainer__ = 'Sebastien Celles'
__maintainer_email__ = "s.celles@gmail.com"


from .bumping import *  # noqa: F401,F403
from .parsing import *  # noqa: F401,F403
from .version import *  # noqa: F401,F403
