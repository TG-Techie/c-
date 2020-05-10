import lark
from lark import Lark
from lark.indenter import Indenter

#lark.tree.Tree.__repr__ = lambda self: str(self.data)

class PyStyleIndenter(Indenter):
    NL_type = 'NEWLINE'
    OPEN_PAREN_types  = ['LPAREN', 'LBRACK', 'LBRACE']
    CLOSE_PAREN_types = ['RPAREN', 'RBRACK', 'RBRACE']
    INDENT_type = 'INDENT'
    DEDENT_type = 'DEDENT'
    tab_len = 4

_cmns_parser = Lark.open('syntax.lark',
                        #parser='earley',
                        rel_to=__file__,
                        postlex=PyStyleIndenter(),
                        #ambiguity='resolve'
                        lexer='standard'
                        )

def parse(sourcestr):
    return _cmns_parser.parse(sourcestr)

if __name__ == '__main__':
    with open('./examples/binoptest.c-') as file:
        print(parse(file.read()).pretty())
