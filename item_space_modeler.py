import os
from dataclasses import dataclass

from lark.tree import Tree
from lark import Token

# fight me
NoneType = type(None)

@dataclass
class Location():

    file    : str
    lineno  : int = None
    colno   : int = None

class CMNSModelTimeError(Exception):

    def __init__(self, lineinfo, message):
        assert isinstance(lineinfo, (int, Location, Tree)), f"argument 'lineinfo' must be one of types {', '.join([repr(typ.__name__) for typ in (int, Location)])}, or 'Tree', got type '{type(lineinfo).__name__}'"

        if isinstance(lineinfo, Tree):
            lineinfo = extract_lineno(line_info)

        if lineinfo is None:
            linemsg = 'UNKNOWN/UNDEFINED'
        elif isinstance(lineinfo, Location):
            linemsg = f"in file '{lineinfo.file}' on line {lineinfo.lineno}"

        else:
            linemsg = f"on line {lineinfo}"

        self.lineinfo = lineinfo
        self.message = message

        super().__init__(f"{linemsg}, {message}")

class CMNSRedefinitionError(CMNSModelTimeError):
    pass

class CMNSFeatureError(CMNSModelTimeError):
    pass

class CMNSModelNotImplementedError(CMNSModelTimeError):
    pass

class CMNSItemNotFound(CMNSModelTimeError):
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

def find_item_by_ident(location, outer, typeident):

    # find the root module surounding the given outer item
    # TODO: rename variables to make more clean
    mod = outer
    while mod.outer is not None:
        mod = mod.outer
    if not isinstance(mod, Module):
        raise CMNSItemNotFound(location, f"found a non-module root, {mod}")

    ident_names = [extract_name(tree) for tree in typeident.children]

    item = mod
    for name in ident_names:
        item = item[name]

    return item

def model_func(path, tree, outer):
    kind = tree.data
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

    if kind == 'funcdef':
        model_to_make = Func
    elif kind == 'funcdec':
        model_to_make = FuncDec
    else:
        raise CMNSModelNotImplementedError(location, f"'{tree.data}' support not yet added")

    lineno = extract_lineno(tree)
    return model_to_make(Location(path, lineno), name, outer, ret_type, children[0])

def model_trait(path, tree, outer):
    # TODO: make traits more rigorous
    kind = tree.data
    children = list(tree.children)
    location = Location(path, extract_lineno(tree))

    if len(children) == 1:
        name = children[0]
    elif len(children) == 2:
        name, block = children
    else:
        raise CMNSFeatureError(location, f"unsupported trait kind '{kind}'")

    name = extract_name(children[0])

    trt_mdl = Trait(location, name, outer, block)

    if kind == 'traitdef':
        model_item_block_into(path, block, trt_mdl)
    elif kind == 'traitdec':
        raise CMNSModelNotImplementedError(location, f"trait decs not yet implemented")

    return trt_mdl

def model_class(path, tree, outer):
    children = tree.children
    location = Location(path, extract_lineno(tree))
    if len(children) == 3:
        typename, something, class_block = children
        if something.data == 'typeident':
            typelist = None
            base_typename = something
        else:
            typelist = something
            base_typename = None
    elif len(children) == 4:
        typename, base_typename, typelist, class_block = children
    else:
        raise CMNSFeatureError(location, "unsupported class feature found, currently only supporting plain classes w/out subclassing")

    if base_typename is not None:
        superclass = find_item_by_ident(location, outer, base_typename)
    else:
        superclass = None

    name = extract_name(typename)
    lineno = extract_lineno(tree)
    #content_type = TypeList.from_tree(typelist)

    cls_mdl = CMNSClass(Location(path, lineno), outer, name, superclass, typelist)

    model_item_block_into(path, class_block, cls_mdl)

    return cls_mdl

def model_trait_impl(path, tree, outer):

    typeident, block = tree.children

    location = Location(path, extract_lineno(typeident))

    model_item_block_into(path, block, outer)

    trt_mdl = find_item_by_ident(location, outer, typeident)

    trt_impl = TraitImpl(location, outer, trt_mdl)

    return trt_impl


def model_item_block_into(path, tree, into):
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
            trt_impl = model_trait_impl(path, item, into)
            into[trt_impl.name] = trt_impl
        elif kind == 'pass_stmt':
            pass
        else:
            raise CMNSFeatureError(location, f"unsupported feature: '{kind}'")


def model_module(path, tree, name, outer=None):

    location = Location(path, '')
    mod = Module(name, location, outer=outer)
    location.lineno = "'{mod}'"
    # is root if none
    model_item_block_into(path, tree, mod)

    #if is a root module
    if mod.outer is None:


    return mod

class Item():

    def __init__(self, location, name, outer):
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}' from value {location}"
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}' from {name} "
        assert isinstance(outer, (NameSpace, NoneType)), f"argument 'outer' must be one of types {', '.join([repr(typ.__name__) for typ in (NameSpace,)])}, or 'NoneType', got type '{type(tree).__name__}'"

        self.location = location
        self.name = name
        self.outer = outer

    def __str__(self):
        return f"<{type(self).__name__} item '{self.name}'>"

    def _layout(self, indent=0):
        return '    '*indent + str(self)

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

    def _layout(self, indent=0):
        string = '    '*indent + str(self) + '\n'
        for item in self._items.values():
            string += item._layout(indent=indent+1) + '\n'
        return string

    #def __str__(self):
        #return f"<{type(self).__name__} '{self.name}'>"#": {repr(tuple(self._items.keys()))[1:-1]}"

class Func(Item):

    def __init__(self, location, name, outer, ret_type_tree, stmt_block_tree):

        super().__init__(location, name, outer)

        self._ret_type_tree = ret_type_tree
        self._stmt_block_tree = stmt_block_tree


    def call(self, params):
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

    def __init__(self, name, location, outer=None):
        # if None then is the root module
        super().__init__(location, name, outer)

class TraitImpl(Item):

    def __init__(self, location, outer, trait):
        super().__init__(location, outer.name, outer)
        assert isinstance(trait, Trait), f"argument 'trait' must be of type 'Trait', got type '{type(trait).__name__}'"
        self._spec = trait

class Declaration(Item):
    pass

class FuncDec(Func, Declaration):
    pass
