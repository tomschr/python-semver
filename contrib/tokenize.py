"""
Parser for version range

range_set  = range, { logical_or, range };
logical_or = {' '}, '||', { ' ' };
range      = hyphen | simple, { ' ', simple } | '';
hyphen     = partial, ' - ', partial;
simple     = primitive | partial | tilde | caret;

primitive  = ( '<' | '>' | '>=' | '<=' | '=' ), partial;
partial    = xr, ( '.', xr ( '.', xr, qualifier ? )? )?;
xr         = 'x' | 'X' | '*' | nr;

nr         = '0' | ['1'-'9'] { ['0'-'9'] };
tilde      = '~', partial;
caret      = '^', partial;
qualifier  = ( '-', pre )?, ( '+', build )?;
pre        = parts;
build      = parts;
parts      = part, { '.', part };
part       = nr | [-0-9A-Za-z]+;
"""

# Links
# https://craftinginterpreters.com/parsing-expressions.html
# https://www.booleanworld.com/building-recursive-descent-parsers-definitive-guide/
# https://vey.ie/2018/10/04/RecursiveDescent.html
# https://www.programcreek.com/python/example/53972/re.Scanner
# https://www.programcreek.com/python/?code=wendlers%2Fmpfshell%2Fmpfshell-master%2Fmp%2Ftokenizer.py
# https://deplinenoise.wordpress.com/2012/01/04/python-tip-regex-based-tokenizer/
# https://jayconrod.com/posts/65/how-to-build-a-parser-by-hand
# https://www.jayconrod.com/posts/38/a-simple-interpreter-from-scratch-in-python--part-2-
# https://stackoverflow.com/q/36953
# https://web.archive.org/web/20120525103427/http://www.evanfosmark.com/2009/02/sexy-lexing-with-python
# https://www.booleanworld.com/building-recursive-descent-parsers-definitive-guide/
# https://github.com/dephell/dephell_specifier/blob/master/dephell_specifier/range_specifier.py
#


import collections
import re

Token = collections.namedtuple("Token", ["type", "value"])

LOGICAL_OR = re.compile(r"\s*\|\|\s*")
TILDE = re.compile(r"~")
CARET = re.compile(r"^")
HYPEN = re.compile(r"-")

NR_STR = r"0|[1-9]\d*"
NR = re.compile(rf"(?P<num>{NR_STR})")

OP_STR = r"<|>|>=|<=|="
OPERATORS = re.compile(rf"(?P<op>{OP_STR})")

NAME_STR = r"[0-9A-Za-z]+"
NAME = re.compile(rf"(?P<name>{NAME_STR})")

PART_STR = rf"{NR_STR} | {NAME_STR}"
PART = re.compile(rf"(?P<part>{PART_STR})", re.VERBOSE)

# parts      = part, { '.', part };
PARTS_STR = rf"{PART_STR} (\.{PART_STR})+"
PARTS = re.compile(rf"(?P<parts>{PARTS_STR})", re.VERBOSE)

PRE_STR = PARTS_STR
PRE = re.compile(rf"(?P<pre>{PRE_STR})")

BUILD_STR = PARTS_STR
BUILD = re.compile(rf"(?P<build>{BUILD_STR})")

# qualifier  = ( '-', pre )?, ( '+', build )?;
QUALIFIER_STR = rf"(\-{PRE_STR})? (\+{BUILD_STR})?"
QUALIFIER = re.compile(rf"(?P<qualifier>{QUALIFIER_STR})")
