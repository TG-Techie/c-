from cmns_parse import parse

class Variable():

    def __init__(self, type, name):
        assert isinstance(type, Type), "'type' must be of type 'Type'"
        assert isinstance(name, str), "'name' must be of type 'str'"
        self.type = type
        self.name = name

class Argument(Variable):
    pass

class Attribure(Variable):
    pass

class Type():

    def __init__(self, name, members, methods):
        self.name = name
        self.members = members
        self.methods = methods

class Function():

    def __init__(self, module, name, arguments, type, stmts):
        self.name = name
        self.type = type
        self.arguments = arguments
        self.stmts = stmts

def newfunction(module, contents):
    contents = contents.children
    name = Name()
    return Function(module, name, arguments, type, stmts)

class BuiltInFunction():

    def __init__(self, name, arguments, type):
        self.name = name
        self.type = type
        self.arguments = arguments

builtintypes = []

intmethods = []
intttype = Type('int', (), intmethods)
builtintypes.append(intttype)

strmethods = []
strtype = Type('str', (), strmethods)
builtintypes.append(strtype)

int___add__mthd = BuiltInFunction('__add__',
                    [Argument(intttype, 'self'), Argument(intttype, 'other')],
                    intttype)
intmethods.append(int___add__mthd)

int___str__mthd = BuiltInFunction('__str__',
                    [Argument(intttype, 'self')],
                    strtype)
intmethods.append(int___str__mthd)

str___add__mthd = BuiltInFunction('__str__',
                    [Argument(strtype, 'self'), Argument(strtype, 'other')],
                    strtype)
strmethods.append(str___add__mthd)

class Module():

    def __init__(self):
        global builtintypes
        self.functions = builtintypes + []
        self.classes = []
        self.globals = []

def translate(tree):
    if not tree.data == 'start':
        raise ValueError("invalid tree, 'tree.data' must be 'start'")
    else:
        module = Module()

        for child in tree.children:
            print(child, type(child))
            if child.data == 'funcdef':
                print('func')
                module.functions.append(newfunction(module, child))
            elif child.data == 'stmt':
                print('stmt')



def test():
    with open('./examples/emptyfunc.c-') as file:
        tree = parse(file.read())
        print(tree.pretty())
    print(translate(tree))
    return tree

if __name__ == '__main__':
    test()
