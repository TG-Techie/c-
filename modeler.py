from lark.tree import Tree
from lark import Token
from cmns_parse import parse

def test():
    """
    desc: a test of the transpiler on a bunch of sentences;
    returns NoneType;
    """
    paths =    ('./sentences/assign_int_lit.c-',
                './sentences/binop_add.c-',
                './sentences/funcdef.c-',
                './sentences/ifstmt.c-',
                './sentences/nestedif.c-',
                './sentences/whileloop.c-',
                './sentences/methodcall.c-',
                './sentences/printtest.c-',
                './sentences/inputtest.c-',
                './sentences/linecont_docs.c-',
                './sentences/classdef.c-',
                './sentences/traitdef.c-',
                )
    error_paths =  ('./sentences/casterror.c-',
                    )
    for path in paths:
        print(f"\ntesting: '{path}'")
        with open(path) as file:
            text = file.read()
            print(text)

            try:
                tree = parse(text)
                print(tree.pretty())
            except:
                print(f"!parse error while parsing file: '{path}'")
                raise

            with open(path.replace('.c-', '_tree.txt'), 'w') as file:
                file.truncate(0)
                file.write(tree.pretty())


if __name__ == '__main__':
    test()
