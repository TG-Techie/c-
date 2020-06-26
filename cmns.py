import os

import cmns_parse as parser
import cmns_model as space_modelr


def test():
    """
    desc: a test of the transpiler on a bunch of sentences;
    returns NoneType;
    """
    paths = (
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
    #paths = ("./sentences/plainclass.c-",)
    #error_paths = ("./sentences/casterror.c-",)


    # test each file
    for path in paths:
        print(f"\ntesting: '{path}'")
        with open(path) as file:

            text = file.read()

            # creat target directory for test debug files
            folder = path.replace('.c-', '')
            if not os.path.exists(folder):
                    os.makedirs(folder)

            # parse the file
            try:
                tree = parser.parse(text)
                #print(tree.pretty())
            except:
                print(f"!parse error while parsing file: '{path}'")
                raise


            with open(folder+'/token_tree.txt', "w+") as file:
                file.truncate(0)
                file.write(tree.pretty())

            try:
                name = path.split('/')[-1][0:-3]
                module = space_modelr.model_module(path, tree, name)
            except:
                print(f"error modeling module {path}")
                raise

            with open(folder+'/item_model.txt', "w+") as file:
                file.truncate(0)
                file.write(module._layout())
                print(module._layout())

if __name__ == "__main__":
    test()
