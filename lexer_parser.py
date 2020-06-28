import os
from dataclasses import dataclass

import lark
from lark import Lark
from lark.indenter import Indenter

from lark.tree import Tree
from lark import Token

@dataclass
class Location():

    file    : str
    lineno  : int = None
    colno   : int = None


class CMNSCompileTimeError(Exception):

    def __init__(self, location, message):
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}'"
        assert isinstance(message, str), f"argument 'message' must be of type 'str', got type '{type(message).__name__}'"

        if os.path.exists(location.file):
            with open(location.file, 'r') as file:
                lines = [line.strip('\n') for line in file.readlines()]

            lineno = location.lineno

            line_above      = f"{lineno-1}: {lines[lineno-2]}" if lineno-2 != -1 else '0: START OF FILE'
            line_of_concern = f"{lineno+0}: {lines[lineno-1]}"
            line_below      = f"{lineno+1}: {lines[lineno+0]}" if lineno+0 != len(lines) else '~: END OF FILE'

            code_show = '\n' + line_above\
                + '\n' + line_of_concern\
                + '\n' + line_below
        else:
            code_show = ''

        msg = f"\n\nError in file '{location.file}' on line {location.lineno}"\
            + f",\n\t{message}"\
            + code_show

        self.location = location
        self.message = message

        super().__init__(msg)

class CMNSModelNotImplementedError(CMNSCompileTimeError):
    pass

# TODO: switch to breadth first? not sure if is a good
def extract_lineno(tree):
    for thing in tree.children:
        if isinstance(thing, Token):
            #print(thing.line, tree)
            return thing.line
        else:
            try:
                return extract_lineno(thing)
            except TypeError:
                continue
    else:
        raise TypeError('no Token found in tree')

def extract_name(path, tree):

    assert isinstance(tree, Tree), f"argument 'tree' must be of type 'Tree', got type '{type(tree).__name__}'"

    if tree.data == 'typename':
        return str(tree.children[0])
    elif tree.data == 'varname':
        return str(tree.children[0])
    else:
        raise CMNSModelNotImplementedError(Location(path, extract_lineno(tree)), f"unknown name of kind '{tree.data}'")

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
    with open('./examples/uniop.c-') as file:
        print(parse(file.read()).pretty())
