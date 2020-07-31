import os
from dataclasses import dataclass

from lexer_parser import *
from sharedbases import *

from cmns_builtin_items import cmns_builtin_module

# fight me
NoneType = type(None)

'''
#https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
class _clicolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'
    BOLD    = '\033[1m'
    UNDERLINE = '\033[4m'
'''

class TypeIdentList():

    def __init__(self, items=None):
        if items is None:
            items = {}
        self._items = dict(items)

    def __iter__(self):
        return iter(self._items.items())

    def extend(self, tree):
        cls = type(self)
        return cls(tree, items=dict(self._items))

    @classmethod
    def from_tree(cls, path, tree):
        assert tree.data == 'typelist'

        trees = [child for child in tree.children if isinstance(child, Tree) and child.data in ('typeident','varname')]

        items = {}

        while len(trees):
            ident = TypeIdent(path, trees.pop(0))
            name = extract_name(path, trees.pop(0))

            items[name] = ident

        return cls(items)

def _add_items_into_from(dest, tree):
    path = dest.location.file

    location = Location(path, extract_lineno(tree))

    for item_tree in tree.children:
        if isinstance(item_tree, Token):
            continue

        kind = item_tree.data

        if kind == 'classdef':
            cls_item = SourceClassItem.from_tree(path, item_tree, dest, dest.root)
            dest[cls_item.name] = cls_item
        elif kind == 'funcdef':
            fn_item = SourceFuncItem.from_tree(path, item_tree, dest, dest.root)
            dest[fn_item.name] = fn_item
        elif kind == 'pass_stmt':
            pass
        else:
            raise CMNSFeatureError(location, f"unsupported feature: '{kind}'")

class SourceFuncItem(FuncItem):

    def __init__(self, location, name, outer, root, ret_typeident, arg_typelist, stmt_block_tree):

        super().__init__(location, name, outer, root)

        # intermediate values to be stored for later during tree construction
        self._ret_typeident = ret_typeident
        self._stmt_block_tree = stmt_block_tree
        self._arg_typeidentlist = arg_typelist

    def model(self):
        #print(self, self.outer)
        ret_typeident = self._ret_typeident
        if ret_typeident is None:
            ret_typeident = 'SomeType'

        print(self, self.root)
        self.ret_type = ret_type = self.root[ret_typeident]

        #print(self, ret_type, self.root)

    @classmethod
    def from_tree(cls, path, tree, outer, root):
        kind = tree.data
        children = list(tree.children)

        if isinstance(children[-1], Token):
            children.pop(-1)

        location = Location(path, extract_lineno(tree))

        if children[0].data in ('get, set'):
            raise CMNSFeatureError(location, f"getters and setters not yet supported")
            prop_type =children.pop(0).data
        else:
            prop_type = None

        name = extract_name(path, children.pop(0))

        #print([child.data for child in children])

        if len(children) == 3:
            arg_typelist, ret_typeident_tree, stmt_block = children
            ret_typeident = TypeIdent(path, ret_typeident_tree)
            TypeIdent
        elif len(children) == 2:
            arg_typelist, stmt_block = children
            ret_typeident = None
        else:
            SHIT

        lineno = extract_lineno(tree)
        return cls(Location(path, lineno), name, outer, root, ret_typeident, arg_typelist, stmt_block)

class SourceClassItem(ClassItem):

    def __init__(self, location, outer, root, name, superclass_typeident, content_typeidents): #, block_tree):

        super().__init__(location, name, outer, root)

        assert isinstance(superclass_typeident, (TypeIdent, NoneType)), f"argument 'superclass_typeident' must be one of types {', '.join([repr(typ.__name__) for typ in (TypeIdent,)])}, or 'NoneType', got type '{type(superclass_typeident).__name__}'"

        self._superclass_typeident = superclass_typeident
        self._content_typeidents = content_typeidents

    @classmethod
    def from_tree(cls, path, tree, outer, root):
        children = tree.children
        location = Location(path, extract_lineno(tree))
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

        name = extract_name(path, typename)
        lineno = extract_lineno(tree)
        #content_type = TypeIdentList.from_tree(typelist)

        if superclass_typeident is not None:
            superident = TypeIdent(path, superclass_typeident)
        else:
            superident = None

        if typelist is not None:
            contentlist = TypeIdentList.from_tree(path, typelist)
        else:
            contentlist = TypeIdentList({})

        cls_item = cls(location, outer, root, name, superident, contentlist)

        _add_items_into_from(cls_item, class_block)

        return cls_item


class SourceModuleItem(ModuleItem):

    def __init__(self, name, location, outer=None, root=None):
        if root is None:
            root = cmns_builtin_module.builtin_module
        super().__init__(name, location, outer, root)


    @classmethod
    def from_tree(cls, path, tree, name, outer=None):
        location = Location(path, '')

        mod = cls(name, location, outer=outer)
        location.lineno = f"'{mod} @ '{path}''"

        _add_items_into_from(mod, tree)
        return mod

    def model(self):
        for item in self:
            item.model()
