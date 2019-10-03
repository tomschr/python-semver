#
#
#

"""
Semantic Versioning Command Line Interface
"""

from __future__ import print_function

import argparse
import sys

from semver import compare, parse_version_info


def parsecli(cliargs=None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result and parser instance
    :rtype: tuple(:class:`argparse.Namespace`, :class:`argparse.ArgumentParser`)
    """
    parser = argparse.ArgumentParser(prog=__package__,
                                     description=__doc__)
    s = parser.add_subparsers(help="commands")

    # create compare subcommand
    parser_compare = s.add_parser("compare",
                                  help="Compares two versions"
                                  )
    parser_compare.set_defaults(which="compare")
    parser_compare.add_argument("version1",
                                help="First version"
                                )
    parser_compare.add_argument("version2",
                                help="First version"
                                )

    # create bump subcommand
    parser_bump = s.add_parser("bump",
                               help="Bumps a version"
                               )
    parser_bump.set_defaults(which="bump")
    sb = parser_bump.add_subparsers(title="Bump commands",
                                    dest="bump")

    # Create subparsers for the bump subparser:
    for p in (sb.add_parser("major",
                            help="Bump the major part of the version"),
              sb.add_parser("minor",
                            help="Bump the minor part of the version"),
              sb.add_parser("patch",
                            help="Bump the patch part of the version"),
              sb.add_parser("prerelease",
                            help="Bump the prerelease part of the version"),
              sb.add_parser("build",
                            help="Bump the build part of the version")):
        p.add_argument("version",
                       help="Version to raise"
                       )

    args = parser.parse_args(args=cliargs)
    return args, parser


def process(args, parser):
    """Process the input from the CLI

    :param args: The parsed arguments
    :type args: :class:`argparse.Namespace`
    :param parser: the instantiated parser
    :type parser: :class:`argparse.ArgumentParser`
    """
    print("args:", args)
    if args.which == "bump":
        maptable = {'major': 'bump_major',
                    'minor': 'bump_minor',
                    'patch': 'bump_patch',
                    'prerelease': 'bump_prerelease',
                    'build': 'bump_build',
                    }
        ver = parse_version_info(args.version)
        # get the respective method and call it
        func = getattr(ver, maptable[args.bump])
        print(func())

    elif args.which == "compare":
        res = compare(args.version1, args.version2)
        print(res)

    return 0


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: error code
    :rtype: int
    """
    try:
        return process(*parsecli(cliargs))

    except ValueError as err:
        print("ERROR", err, file=sys.stderr)
        return 2
