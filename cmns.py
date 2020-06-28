import os
import sys

sys.path.append(os.path.abspath('.'))

import lexer_parser
from itemspaces import ModuleItem
from models import ModuleModel

test_files = (
    "./sentences/assign_int_lit.c-",
    "./sentences/binop_add.c-",
    "./sentences/funcdef.c-",
    "./sentences/ifstmt.c-",
    "./sentences/nestedif.c-",
    "./sentences/whileloop.c-",
    "./sentences/methodcall.c-",
    "./sentences/printtest.c-",
    "./sentences/inputtest.c-",
    "./sentences/linecont_docs.c-",
    #"./sentences/classdef.c-", # has getters and setters
    "./sentences/traitdef.c-",
    "./sentences/itemized.c-",
    "./sentences/comptypes.c-",
    #'./sentences/imports.c-', # just not there yet
    "./sentences/inherit.c-",
    "./sentences/traitcast.c-",
)

test_files = (
    "./sentences/plainclass.c-",
    "./sentences/inherit.c-",
)

def test():
    """
    desc: a test of the transpiler on a bunch of sentences;
    returns NoneType;
    """

    global test_files

    # test each file
    for path in test_files:
        print(f"\ntesting: '{path}'")
        with open(path) as file:

            text = file.read()

            # creat target directory for test debug files
            folder = path.replace('.c-', '')
            if not os.path.exists(folder):
                    os.makedirs(folder)

            # parse the file
            try:
                tree = lexer_parser.parse(text)
                #print(tree.pretty())
            except:
                print(f"!parse error while parsing file: '{path}'")
                raise


            with open(folder+'/token_tree.txt', "w+") as file:
                file.truncate(0)
                file.write(tree.pretty())

            try:
                name = path.split('/')[-1][0:-3]
                module = ModuleItem.from_tree(path, tree, name)
            except:
                print(f"error modeling module {path}")
                raise

            with open(folder+'/item_model.txt', "w+") as file:
                file.truncate(0)
                file.write(module._layout())
                print(module._layout())

def test2():
    """
    desc: a test of the transpiler on a bunch of sentences;
    returns NoneType;
    """

    global test_files

    # test each file
    for path in test_files:
        print(f"\ntesting: '{path}'")
        with open(path) as file:

            text = file.read()

            # creat target directory for test debug files
            folder = path.replace('.c-', '')
            if not os.path.exists(folder):
                    os.makedirs(folder)

            print('Parsing...')
            tree = lexer_parser.parse(text)
            print('Parsing complete')

            with open(folder+'/token_tree.txt', "w+") as file:
                file.truncate(0)
                file.write(tree.pretty())

            name = path.split('/')[-1][0:-3]
            print('Itemizing...')
            mod_item = ModuleItem.from_tree(path, tree, name)
            print('itemization complete')

            with open(folder+'/item_model.txt', "w+") as file:
                file.truncate(0)
                file.write(mod_item._layout())

            print(mod_item._layout())

            print('Modeling...')
            mod_mdl = ModuleModel.from_item(mod_item)
            print('Modeling complete')

if __name__ == "__main__":
    test2()
