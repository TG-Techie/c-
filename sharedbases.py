from lexer_parser import *
from strictly import *

NoneType = type(None)

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

class TypeIdent():

    @strictly
    def __init__(self, path, tree: Tree, doc: str = 'no documentation provided'):
        #print(tree.data, path)
        assert tree.data == 'typeident'
        ident = tree.children[0]

        self.location = location = Location(path, extract_lineno(tree))
        self.doc = doc

        if ident.data == 'plain_type_ident':
            self.names = [extract_name('', child) for child in ident.children]
            self.plain = True
        elif ident.data == 'builtin_compound_type_ident':
            print('making new TypeIdent:', 'ident.data:', ident.data)



            #self.names = ['']
            self.kind = ident.children[0].data
            self.plain = False

            self.innertypes = [TypeIdent(path, child) for child in ident.children[0].children]
        else:
            raise CMNSFeatureError(location, f"unsupported type syntax '{ident.data}'")

    def __iter__(self):
        if self.plain:
            return iter(self.names)
        else:
            raise ValueError(f'compound types cannot be iterated, {self}')

    def __str__(self):
        if self.plain:
            return f"<{type(self).__name__} '{'.'.join(self.names)}'>"
        else:
            return f"<TypeIdent {repr(self.kind)} {self.innertypes}>"

    def __repr__(self):
        return self.__str__()

class Item():

    @strictly
    def __init__(self, location: Location, name: str, outer, root):
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}' from value {location}"
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}' from {name} "
        assert isinstance(outer, (NameSpaceItem, NoneType)), f"argument 'outer' must be one of types {', '.join([repr(typ.__name__) for typ in (NameSpaceItem,)])}, or 'NoneType', got type '{type(tree).__name__}'"

        self.location = location
        self.name = name
        self.outer = outer
        print(self, root)
        self.root = root
        self.modeled = False # flags if the model function has yet been run

    def model(self):
        raise CMNSModelNotImplementedError(Location('!transpiler'), f"modeling not yet finished for {type(self).__name__}")

    def __str__(self):
        return f"<{type(self).__name__} '{self.name}'>"

    def __repr__(self):
        return str(self)

    def _layout(self, indent: int = 0):
        return '    '*indent + str(self)

class NameSpaceItem(Item):

    def __init__(self, *args, items: dict = None):

        if items is None:
            items = {}

        super().__init__(*args)

        self._items = items

    def __iter__(self):
        return iter(self._items.values())

    def __getitem__(self, ident):
        #assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"
        if isinstance(ident, str):
            if ident in self._items:
                return self._items[ident]
            else:
                raise CMNSItemNotFound(Location(self.location.file), f"unable to find '{ident}' in item {self}")
        elif isinstance(ident, TypeIdent):
            item = self
            if ident.plain:
                for name in ident:
                    item = item[name]
                return item
            else:
                HALT_ADD_Compound_types_via_itemized_lookup
                return
        else:
            raise ValueError(f"an item must be fetch using a 'str' or 'TypeIdent', got a '{type(ident)}'")

    def __setitem__(self, name, value):
        assert isinstance(value, Item), f"argument 'value' must be of type 'Item', got type '{type(value).__name__}'"

        if name in self._items:
            raise CMNSRedefinitionError(value.lineno, f"cannot redefine {self[name]} as '{value}'")
        else:
            self._items[name] = value

    @strictly
    def _layout(self, indent: int = 0):
        string = '    '*indent + str(self) + '\n'
        for item in self._items.values():
            string += item._layout(indent=indent+1) + '\n'
        return string

class ModuleItem(NameSpaceItem):

    @strictly
    def __init__(self, name: str, location: Location, outer=None, root=None):
        # if None then is the root module
        super().__init__(location, name, outer, root)

class FuncItem(Item):

    def init(self, ret_type, call_types, stmt_block):
        # init completes the item, keep in mind it already has some info from the constructor

        self.targets =  {} # {call_types : FuncItem w/out SomeType or SelfType}

        self.ret_type = ret_type
        self.call_types = call_types
        self.stmt_block # if this is none targets must be added manually

    def call(self, call_exprs): # -> FuncCallExpr
        # callstack.push(self, location, blah blah)
        SHIT_TO_DO_HERE_IS_NOT_DONE
        # if it is a new call signature then make a target using the stmt_block

class ClassItem(NameSpaceItem):

    def init(self, superclass, contents):
        self.superclass = superclass
        self.contents = contents = {**superclass.contents, **contents} # 3.7 on maintains order

    @strictly
    def get_attribure(self, name:str):
        SHIT_TO_DO_HERE_IS_NOT_DONE

    def model(self):
        for item in self._items.values():
            item.model()
