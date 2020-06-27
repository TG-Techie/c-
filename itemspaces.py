import os
from dataclasses import dataclass

from lark.tree import Tree
from lark import Token

# fight me
NoneType = type(None)

class CMNSCompileTimeError(Exception):

    def __init__(self, location, message):
        assert isinstance(lineinfo, (int, Location, Tree)), f"argument 'lineinfo' must be one of types {', '.join([repr(typ.__name__) for typ in (int, Location)])}, or 'Tree', got type '{type(lineinfo).__name__}'"
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}'"

        linemsg = f"in file '{lineinfo.file}' on line {lineinfo.lineno}"

        self.location = location
        self.message = message

        super().__init__(f"{linemsg}, {message}")

class CMNSItemizationError(CMNSCompileTimeError):
    pass

class CMNSRedefinitionError(CMNSItemizationError):
    pass

class CMNSFeatureError(CMNSItemizationError):
    pass

class CMNSModelNotImplementedError(CMNSItemizationError):
    pass

class CMNSItemNotFound(CMNSItemizationError):
    pass

@dataclass
class Location():

    file    : str
    lineno  : int = None
    colno   : int = None

# TODO: switch to breadth first? not sure if is a good
def _extract_lineno(tree):
    for thing in tree.children:
        if isinstance(thing, Token):
            return thing.line
        else:
            try:
                return _extract_lineno(thing)
            except TypeError:
                continue
    else:
        raise TypeError('no Token found in tree')

def _extract_name(path, tree):
    assert isinstance(tree, Tree), f"argument 'tree' must be of type 'Tree', got type '{type(tree).__name__}'"

    if tree.data == 'typename':
        return str(tree.children[0])
    elif tree.data == 'varname':
        return str(tree.children[0])
    else:
        raise CMNSModelNotImplementedError(Location(path, _extract_lineno(tree)), f"unknown name of kind '{tree.data}'")

class Item():

    def __init__(self, location, name, outer):
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}' from value {location}"
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}' from {name} "
        assert isinstance(outer, (NameSpaceItem, NoneType)), f"argument 'outer' must be one of types {', '.join([repr(typ.__name__) for typ in (NameSpaceItem,)])}, or 'NoneType', got type '{type(tree).__name__}'"

        self.location = location
        self.name = name
        self.outer = outer

    def __str__(self):
        return f"<{type(self).__name__} '{self.name}'>"

    def __repr__(self):
        return str(self)

    def _layout(self, indent=0):
        return '    '*indent + str(self)

class NameSpaceItem(Item):

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

    def _add_items_from(self, tree):
        path = self.location.file

        location = Location(path, _extract_lineno(tree))

        for item_tree in tree.children:
            if isinstance(item_tree, Token):
                continue

            kind = item_tree.data

            if kind == 'classdef':
                cls_item = ClassItem.from_tree(path, item_tree, self)
                self[cls_item.name] = cls_item
            elif kind == 'funcdef':
                fn_item = FuncItem.from_tree(path, item_tree, self)
                self[fn_item.name] = fn_item
            elif kind == 'funcdec':
                fndec_item = FuncDecModel.from_tree(path, item_tree, self)
                self[fndec_item.name] = fndec_item
            elif kind in ('traitdef'):
                trt_item = TraitDefItem.from_tree(path, item_tree, self)
                self[trt_item.name] = trt_item
            elif kind in ('traitdec'):
                trtdec_item = TraitDecItem.from_tree(path, item_tree, self)
                self[trtdec_item.name] = trtdec_item
            elif kind == 'traitimpl':
                trt_impl = TraitImplItem.from_tree(path, item_tree, self)
                self[trt_impl.name] = trt_impl
            elif kind == 'pass_stmt':
                pass
            else:
                raise CMNSFeatureError(location, f"unsupported feature: '{kind}'")

class FuncItem(Item):

    def __init__(self, location, name, outer, ret_typeident, stmt_block_tree):

        super().__init__(location, name, outer)

        self._ret_typeident = ret_typeident
        self._stmt_block_tree = stmt_block_tree

    #def __str__(self):
    #    return super().__str__().replace('>', f"returns {self.ret_type}>")

    @classmethod
    def from_tree(cls, path, tree, outer):
        kind = tree.data
        children = list(tree.children)

        if isinstance(children[-1], Token):
            children.pop(-1)

        location = Location(path, _extract_lineno(tree))

        if children[0].data in ('get, set'):
            raise CMNSFeatureError(location, f"getters and setters not yet supported")
            prop_type =children.pop(0).data
        else:
            prop_type = None

        name = _extract_name(path, children.pop(0))

        if children[-1].data == 'typeident':
            ret_type = children.pop(-1)
        else:
            ret_type = None

        lineno = _extract_lineno(tree)
        return cls(Location(path, lineno), name, outer, ret_type, children[0])

class TraitDefItem(NameSpaceItem):

    @classmethod
    def from_tree(cls, path, tree, outer):
        # TODO: make traits more rigorous
        kind = tree.data
        children = list(tree.children)
        location = Location(path, _extract_lineno(tree))

        if len(children) == 1:
            name = children[0]
        elif len(children) == 2:
            name, block = children
        else:
            raise CMNSFeatureError(location, f"unsupported trait kind '{kind}'")

        name = _extract_name(path, children[0])

        trt_item = cls(location, name, outer)

        trt_item._add_items_from(block)

        return trt_item

class ClassItem(NameSpaceItem):

    def __init__(self, location, outer, name, superclass_typeident, typelist_tree): #, block_tree):

        super().__init__(location, name, outer)

        assert isinstance(outer, NameSpaceItem), f"argument 'outer' must be of type 'NameSpaceItem', got type '{type(outer).__name__}'"

        selfname = name
        self._superclass_typeident = superclass_typeident
        self._typelist_tree = typelist_tree
        #self._block_tree = block_tree

    @classmethod
    def from_tree(cls, path, tree, outer):
        children = tree.children
        location = Location(path, _extract_lineno(tree))
        if len(children) == 3:
            typename, something, class_block = children
            if something.data == 'typeident':
                typelist = None
                superclass_typeident = something
            else:
                typelist = something
                superclass_typeident = None
        elif len(children) == 4:
            typename, superclass_typeident, typelist, class_block = children
        else:
            raise CMNSFeatureError(location, "unsupported class feature found, currently only supporting plain classes and subclasses")

        #if base_typename is not None:
        #    superclass = _find_item_by_ident(location, outer, base_typename)
        #else:
        #    superclass = None

        name = _extract_name(path, typename)
        lineno = _extract_lineno(tree)
        #content_type = TypeList.from_tree(typelist)

        cls_item = cls(Location(path, lineno), outer, name, superclass_typeident, typelist)

        cls_item._add_items_from(class_block)

        return cls_item

class ModuleItem(NameSpaceItem):

    def __init__(self, name, location, outer=None):
        # if None then is the root module
        super().__init__(location, name, outer)

    @classmethod
    def from_tree(cls, path, tree, name, outer=None):

        location = Location(path, '')
        mod = cls(name, location, outer=outer)
        location.lineno = f"'{mod} @ '{path}''"
        # is root if none
        mod._add_items_from(tree)

        #if is a root module
        #if mod.outer is None:
        #    mod._model()

        return mod

class TraitImplItem(NameSpaceItem):

    def __init__(self, location, outer, trait_typeident):

        super().__init__(location, outer.name, outer)
        #assert isinstance(trait, TraitDefItem), f"argument 'trait' must be of type 'TraitDefItem', got type '{type(trait).__name__}'"
        self._trait_typeident = trait_typeident

    @classmethod
    def from_tree(cls, path, tree, outer):

        typeident, block = tree.children

        location = Location(path, _extract_lineno(typeident))

        #trt_item = _find_item_by_ident(location, outer, typeident)

        trt_impl = cls(location, outer, typeident)

        trt_impl._add_items_from(block)

        return trt_impl

class TraitDecItem(FuncItem):
    pass

class FuncDecModel(FuncItem):
    pass
