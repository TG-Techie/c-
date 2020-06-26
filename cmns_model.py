from dataclasses import dataclass

from lark.tree import Tree
from lark import Token
from cmns_parse import parse

# fight me
NoneType = type(None)

@dataclass
class Location():

    file    : str
    lineno  : int = None
    colno   : int = None

class CMNSModelTimeError(Exception):

    def __init__(self, line_info, message):
        assert isinstance(line_info, (int, Location, Tree)), f"argument 'line_info' must be one of types {', '.join([repr(typ.__name__) for typ in (int, Location)])}, or 'Tree', got type '{type(line_info).__name__}'"

        if isinstance(line_info, Tree):
            line_info = extract_lineno(line_info)

        if line_info is None:
            line_msg = 'UNKNOW/UNDEFINED'

        elif isinstance(line_info, Location):
            line_msg = f"in file '{line_info.file}' on line {line_info.lineno}"

        else:
            line_msg = f"on line {line_info}"

        super().__init__(f"{line_msg}, {message}")

class CMNSRedefinitionError(CMNSModelTimeError):
    pass

class CMNSFeatureError(CMNSModelTimeError):
    pass

class CMNSModelNotImplementedError(CMNSModelTimeError):
    pass

# TODO: switch to breadth first? not sure if is a good
def extract_lineno(tree):
    for thing in tree.children:
        if isinstance(thing, Token):
            return thing.line
        else:
            try:
                return extract_lineno(thing)
            except TypeError:
                continue
    else:
        raise TypeError('no Token found in tree')

def extract_name(tree):
    assert isinstance(tree, Tree), f"argument 'tree' must be of type 'Tree', got type '{type(tree).__name__}'"

    if tree.data == 'typename':
        return str(tree.children[0])
    elif tree.data == 'varname':
        return str(tree.children[0])
    else:
        raise CMNSModelNotImplementedError(location, f"unknown name of kind '{tree.data}'")


def model_func(path, tree, outer):
    children = list(tree.children)

    location = Location(path, extract_lineno(tree))
    #print([foo.data for foo in children])

    if children[0].data in ('get, set'):
        raise CMNSFeatureError(location, f"getters and setters not yet supported")
        # otherwise:
        prop_type =children.pop(0).data
    else:
        prop_type = None

    #print([foo.data for foo in children])
    name = extract_name(children.pop(0))

    if children[0].data == 'typeident':
        ret_type = children.pop(0)
    else:
        ret_type = None

    if tree.data == 'funcdef':
        lineno = extract_lineno(tree)
        return Func(Location(path, lineno), name, outer, ret_type, children[0])
    else:
        raise CMNSModelNotImplementedError(location, f"'{tree.data}' support not yet added")
    SHIT

def model_trait(path, tree, outer):
    # TODO: make traits more rigorous
    kind = tree.data
    children = list(tree.children)
    location = Location(path, extract_lineno(tree))

    if len(children) == 1:
        name = childen[0]
    elif len(children) == 2:
        name, block = children
    else:
        raise CMNSFeatureError(location, f"unsupported trait kind '{kind}'")

    name = extract_name(children[0])

    trt_mdl = Trait(location, name, outer, block)

    if kind == 'traitdef':
        model_item_block(path, block, trt_mdl)
    elif kind == 'traitdec':
        raise CMNSModelNotImplementedError(location, f"trait decs not yet implemented")

    return trt_mdl

def model_class(path, tree, outer):
    children = tree.children
    if len(children) == 3:
        typename, typelist, class_block = children
        superclass = None
    # TODO: add subclassing to model
    #elif len(children) == 4:
    #    typename, base_typename, typelist, class_block = children
    #    is_subclass = True
    else:
        raise CMNSFeatureError(location, "unsupported class feature found, currently only supporting plain classes w/out subclassing")

    name = extract_name(typename)
    lineno = extract_lineno(tree)
    #content_type = TypeList.from_tree(typelist)

    cls_mdl = CMNSClass(Location(path, lineno), outer, name, superclass, typelist)

    model_item_block(class_block, cls_mdl)

    return cls_mdl

def model_item_block(path, tree, into):
    location = Location(path, extract_lineno(tree))

    for item in tree.children:
        if isinstance(item, Token):
            continue

        kind = item.data

        if kind == 'classdef':
            cls_mdl = model_class(path, item, into)
            into[cls_mdl.name] = cls_mdl
        elif kind in ('funcdef', 'funcdec'):
            fn_mdl = model_func(path, item, into)
            into[fn_mdl.name] = fn_mdl
        elif kind in ('traitdef', 'traitdec'):
            trt_mdl = model_trait(path, item, into)
            into[trt_mdl.name] = trt_mdl
        # func and trait should deferentiate between decs and defs
            '''
        elif kind == 'funcdec':
            fn_dec = model_func_dec(item, into)
            into[fn_dec.name] = fn_dec
        elif kind == 'traitdec':
            trt_dec = model_trait_dec(item, into)
            into[trt_dec.name] = trt_dec
        '''
        elif kind == 'traitimpl':
            trt_impl = model_trait_impl(item, into)
            into[trt_impl.name] = trt_impl
        elif kind == 'pass_stmt':
            pass
        else:
            raise CMNSFeatureError(location, f"unsupported feature: '{kind}'")

def model_module(path, tree, name):

    location = Location(path, '')
    mod = Module(name, location)
    location.lineno = "'{mod}'"

    model_item_block(path, tree, mod)

    print(mod)

class Pair():

    def __init__(self, name, type):
        assert isinstance(name, str)
        assert isinstance(type, Type)
        self.name = name
        self.type = type

    def __iter__(self):
        return iter((self.name, self.type))

class Var(Pair):

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)
        self.outstr = self.name+'_var'


class Arg(Pair):

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)
        self.outstr = self.name+'_var'


class Attr(Pair):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outstr = self.name+'_attr'

class Expr():

    def __init__(self, lineno, type):
        self.lineno = lineno
        self.type = type

    def get_attr(self, name):
        '''
        gets either an expression or a bound method w/ self in it
        '''
        pass

    def iscallable(self):
        return '__call__' in self.type

    def call(self):
        pass

class Litrl(Expr):

    def __init__(self, lineno, prefix, outstr):
        super().__init__(lineno, prefix)
        self.outstr = outstr

class TypeList():

    def __init__(self, pairs=None):

        if pairs is None:
            pairs = {}
        else:
            # TODO: ass assert for dict contents
            assert isinstance(pairs, esc), f"argument 'pairs' must be of type 'esc', got type '{type(pairs).__name__}'"

        self._pairs = pairs # dicts are ordered

    def __iter__(self):
        return iter(self._pairs.values())

    def __contains__(self, target):
        if isinstance(target, str):
            return target in self._pairs
        elif isinstance(target, pair):
            tup = tuple(target)
            return tup in [tuple(pair) for pait in self._pairs]
        else:
            raise ValueError("can only check if 'TypeList' contains a variable by c-name")

    def __getitem__(self, name):
        return self._pairs[name]

    def __setitem__(self, name, var):
        if name != var.name:
            raise ValueError(f"key '{name}' does not match the name in the given variable, '{name}' != '{var.name}'")
        else:
            self._pairs[name] = var

    def __len__(self):
        return len(self._pairs)

class Item():

    def __init__(self, location, name, outer):
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}'"
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"
        assert isinstance(outer, (NameSpace, NoneType)), f"argument 'outer' must be one of types {', '.join([repr(typ.__name__) for typ in (NameSpace,)])}, or 'NoneType', got type '{type(tree).__name__}'"

        self.location = location
        self.name = name
        self.outer = outer

    def __str__(self):
        return f"<{type(self).__name__} '{self.name}'>"

class NameSpace(Item):

    def __init__(self, *args, items=None):

        super().__init__(*args)

        if items is None:
            items = {}
        else:
            assert isinstance(items, dict), f"argument 'items' must be of type 'dict', got type '{type(items).__name__}'"

        self._items = items

    def __getitem__(self, name):
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"

        return self._items[name]

    def __setitem__(self, name, value):
        assert isinstance(value, Item), f"argument 'value' must be of type 'Item', got type '{type(value).__name__}'"

        if name in self._items:
            raise CMNSRedefinitionError(value.lineno, f"cannot redefine {self[name]} as '{value}'")
        else:
            self._items[name] = value

    def __contains__(self, value):
        if isinstance(value, Item):
            return value in self._items.items()
        else:
            return value in self._items

    #def __str__(self):
        #return f"<{type(self).__name__} '{self.name}'>"#": {repr(tuple(self._items.keys()))[1:-1]}"

class Func(Item):

    def __init__(self, location, name, outer, ret_type_tree, stmt_block_tree):

        super().__init__(location, name, outer)

        self._ret_type_tree = ret_type_tree
        self._stmt_block_tree = stmt_block_tree


    def call(self, params : TypeList):
        pass

class BoundMethod(Func):
    pass

class Trait(NameSpace):

    def __init__(self, location, name, outer, stmt_block_tree):

        super().__init__(location, name, outer)

        self._stmt_block_tree = stmt_block_tree

class CMNSClass(NameSpace):

    def __init__(self, location, outer, name, superclass, typelist_tree): #, block_tree):

        super().__init__(location, name, outer)

        assert isinstance(outer, NameSpace), f"argument 'outer' must be of type 'NameSpace', got type '{type(outer).__name__}'"
        assert isinstance(superclass, (CMNSClass, NoneType)), f"argument 'superclass' must be one of types {', '.join([repr(typ.__name__) for typ in (CMNSClass,)])}, or 'NoneType', got type '{type(superclass).__name__}'"

        selfname = name
        self.superclass = superclass
        self._typelist_tree = typelist_tree
        #self._block_tree = block_tree

    def fillout(self):
        pass

class Module(NameSpace):

    def __init__(self, name, location):

        super().__init__(location, name, None)



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
        #"./sentences/classdef.c-",
        #"./sentences/traitdef.c-",
        #"./sentences/itemized.c-",
        "./sentences/comptypes.c-",
        #'./sentences/imports.c-',
    )
    #paths = ("./sentences/plainclass.c-",)
    error_paths = ("./sentences/casterror.c-",)
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

            with open(path.replace(".c-", "_tree.txt"), "w") as file:
                file.truncate(0)
                file.write(tree.pretty())
                try:
                    name = path.split('/')[-1][0:-3]
                    model_module(path, tree, name)
                except:
                    print(f"error modeling module {path}")
                    raise

if __name__ == "__main__":
    test()
