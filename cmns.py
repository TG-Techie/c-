import os

import lexer_parser
import item_space_modeler


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
                module = item_space_modeler.model_module(path, tree, name)
            except:
                print(f"error modeling module {path}")
                raise

            with open(folder+'/item_model.txt', "w+") as file:
                file.truncate(0)
                file.write(module._layout())
                print(module._layout())

if __name__ == "__main__":
    test()
