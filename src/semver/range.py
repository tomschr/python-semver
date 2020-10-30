"""
Version ranges

# Grammar

range-set  ::= range ( logical-or range ) *
logical-or ::= ( ' ' ) * '||' ( ' ' ) *
range      ::= hyphen | simple ( ' ' simple ) * | ''
hyphen     ::= partial ' - ' partial
simple     ::= primitive | partial | tilde | caret
primitive  ::= ( '<' | '>' | '>=' | '<=' | '=' ) partial
partial    ::= xr ( '.' xr ( '.' xr qualifier ? )? )?
xr         ::= 'x' | 'X' | '*' | nr
nr         ::= '0' | ['1'-'9'] ( ['0'-'9'] ) *
tilde      ::= '~' partial
caret      ::= '^' partial
qualifier  ::= ( '-' pre )? ( '+' build )?
pre        ::= parts
build      ::= parts
parts      ::= part ( '.' part ) *
part       ::= nr | [-0-9A-Za-z]+
"""

import re


class Comparator:
    pass


class ExpressionParser:

    _NUMBERS = re.compile(r"[-0-9A-Za-z]+")
    # nr         ::= '0' | ['1'-'9'] ( ['0'-'9'] ) *
    _NR = re.compile(r"(?P<NR>0(?!\d)|[1-9]\d*)")
    #
    _XR = ""

    def __init__(self):
        self.ast = []

    def parser(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None      # last symbol consumed
        self.nexttok = None  # Next symbol tokenized
        self._ast = []       # our AST
        self._advance()

    def _advance(self):
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        if self.nexttoke and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        if not self._accept(toktype):
            raise SyntaxError(f"Expected {toktype}")

    # Grammar rules:
    def _range_set(self):
        # range-set  ::= range ( logical-or range ) *
        # if self._range():
        self.ast.append(self._range())
        while expr:
            lor = self._logical_or()
            if lor:
                self.ast.append(lor)
                r = self._range()
                self.ast.append(r)
            else:
                raise SyntaxError("Expected logical-or and range")

    def _logical_or(self):
        # logical-or ::= ( ' ' ) * '||' ( ' ' ) *
        if text.strip() == "||":
            self.ast.append("||")
        else:
            raise SyntaxError("Expected ||")

    def _range(self):
        # range      ::= hyphen | simple ( ' ' simple ) * | ''
        hyphen = self._hyphen()
        simple = self._simple()
        if hyphen:
            self.ast.append(hyphen)
        elif simple:
            while simple:
                self.ast.append(self._simple())
        else:
            raise SyntaxError("Expected ")

    def _hyphen(self):
        # hyphen     ::= partial ' - ' partial
        partial = self._partial()
        if partial:
            self.ast.append(partial)
            if self.nexttok == " - ":
                partial = self._partial()
                if partial:
                    self.ast.append(partial)
                    return

        raise SyntaxError("Expected a partial")

    def _simple(self):
        # simple     ::= primitive | partial | tilde | caret
        pass

    def _primitive(self):
        # primitive  ::= ( '<' | '>' | '>=' | '<=' | '=' ) partial
        pass

    def _partial(self):
        # partial    ::= xr ( '.' xr ( '.' xr qualifier ? )? )?
        pass

    def _xr(self):
        # xr         ::= 'x' | 'X' | '*' | nr
        pass

    def _nr(self):
        # nr         ::= '0' | ['1'-'9'] ( ['0'-'9'] ) *
        pass

    def _tilde(self):
        # tilde      ::= '~' partial
        pass

    def _caret(self):
        # caret      ::= '^' partial
        pass

    def _qualifier(self):
        # qualifier  ::= ( '-' pre )? ( '+' build )?
        pass

    def _pre(self):
        # pre        ::= parts
        pass

    def _build(self):
        # build      ::= parts
        pass

    def _parts(self):
        # parts      ::= part ( '.' part ) *
        pass

    def _part(self):
        # part       ::= nr | [-0-9A-Za-z]+
        if self._nr():
            pass
        elif expr:
            pass
        else:
            raise SyntaxError("Expected number or ")


class Range:
    def __init__(self, vrange, options):
        if isinstance(vrange, Range):
            # ...
            pass
        elif isinstance(vrange, Comparator):
            pass

        self.raw = vrange
        self.set =

    def __repr__(self):
        return "TBD"

    def parse(self, vrange):
        #

