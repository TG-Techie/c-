from typing import *
from itemspaces import *
import stmt

class CMNSModelTimeError(CMNSCompileTimeError):
    pass

_builtintypes_module_model = None # this will be set later by the builtintypes module

def find_item_by_ident(location, module, typeident, prev=None):
    assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}'"
    assert isinstance(module, ModuleModel), f"argument 'module' must be of type 'ModuleModel', got type '{type(module).__name__}'"
    assert isinstance(typeident, TypeIdent), f"argument 'typeident' must be of type 'TypeIdent', got type '{type(typeident).__name__}'"


    item = module
    for name in typeident:
        if name in item:
            item = item[name]
        elif module is _builtintypes_module_model: # cannot find it
            raise CMNSItemNotFound(location, f"unable to find {typeident} in {prev} or {_builtintypes_module_model}")
        else: # cannot find in either given or builtins
            return find_item_by_ident(location, _builtintypes_module_model, typeident, prev=module)
    else:
        return item


    '''
    try:
        item = module

        for name in typeident.names:
            print(f"searching in {item} for '{name}'")
            print(item._items)
            item = item.__getitem__(name, location=typeident.location)
            print(f"found {item}")

        return item
    except CMNSCompileTimeError as stdscope_error:
        THIS
        try:
            return find_item_by_ident(location, _builtintypes_module_model, typeident)
        except:
            raise stdscope_error
    '''


'''
class TypeList():

    def __init__(self, items):
        self._items = items

    def __iter__(self):
        return iter(self._items.values())

    def __getitem__(self, name):
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"

        return self._items[name]

    def __setitem__(self, name, value):
        assert isinstance(value, (ClassModel, TraitModel)), f"argument 'value' must be of type 'Item', got type '{type(value).__name__}'"

        if name in self._items:
            raise CMNSRedefinitionError(value.lineno, f"cannot redefine {self[name]} as '{value}'")
        else:
            self._items[name] = value
'''

class ModelElement():

    def __init__(self, location, name, module):
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"
        assert isinstance(location, Location), f"argument 'location' must be of type 'Location', got type '{type(location).__name__}'"
        assert isinstance(module, (ModuleModel, NoneType)), f"argument 'module' must be one of types {', '.join([repr(typ.__name__) for typ in (ModuleModel,)])}, or 'NoneType', got type '{type(module).__name__}'"

        self.module = module
        self.location = location
        self.name = name

    def __str__(self):
        return f"<{type(self).__name__.replace('Model', '')} '{self.name}'>"

    def __repr__(self):
        return str(self)

class NameSpaceModel(ModelElement):

    def __init__(self, *args):

        super().__init__(*args)

        self._items = {}

    def __iter__(self):
        return iter(self._items.values())

    def __getitem__(self, name, location=None):
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"

        if name in self._items:
            return self._items[name]
        else:
            if location is None:
                location = self.location
            raise CMNSItemNotFound(location, f"unable to find item '{name}' in {self}")

    def __setitem__(self, name, value):
        assert isinstance(value, ModelElement), f"argument 'value' must be of type 'ModelElement', got type '{type(value).__name__}'"

        if name in self._items:
            raise CMNSRedefinitionError(value.location, f"cannot redefine {self[name]} as '{value}'")
        else:
            self._items[name] = value

    def __contains__(self, value):
        if isinstance(value, Item):
            return value in self._items.items()
        else:
            return value in self._items

class FuncModel(ModelElement):
    """
    attrs:
        location    : Location
        name        : str
        module      : ModuleModel
        ret_type    : ClassModel
        typelist    : Dict[str, Union[ClassModel, TraitModel]]
    """

    def __init__(self, location, name, module, ret_type_typeident, arg_typelist):

        super().__init__(location, name, module)

        assert isinstance(ret_type_typeident, TypeIdent), f"argument 'ret_type_typeident' must be of type 'TypeIdent', got type '{type(ret_type_typeident).__name__}'"
        assert isinstance(ret_type_typeident, TypeIdent), f"argument 'ret_type_typeident' must be of type 'TypeIdent', got type '{type(ret_type_typeident).__name__}'"

        self._ret_type_typeident = ret_type_typeident
        self._arg_typelist = arg_typelist

        self.targets = {} # Dict[TypeList, FuncTarget]

    def _finish_model(self, ret_type, typelist, stmt_block):
        assert isinstance(ret_type, ClassModel), f"argument 'ret_type' must be of type 'ClassModel', got type '{type(ret_type).__name__}'"
        assert isinstance(typelist, TypeList), f"argument 'typelist' must be of type 'TypeList', got type '{type(typelist).__name__}'"
        assert isinstance(stmt_block, StmtBlock), f"argument 'stmt_block' must be of type 'StmtBlock', got type '{type(stmt_block).__name__}'"

        self.ret_type = ret_type
        self.typelist = typelist
        self.stmt_block = stmt_block



    def _model(self):
        pass


class TraitModel(NameSpaceModel):
    """
    attrs:
        location    : Location
        name        : str
        module      : ModuleModel
        traitdecs   : dicts
        funcdecs    : dict
    """

class ClassModel(NameSpaceModel):
    """
    attrs:
        location    : Location
        name        : str
        superclass  : ClassModel
        contents    : dict
        items       : dict
    """

    def __init__(self, location, name, module, superclass_ident, content_typelist, frontend_items):

        super().__init__(location, name, module)

        assert isinstance(superclass_ident, (TypeIdent, NoneType)), f"argument 'superclass_ident' must be one of types {', '.join([repr(typ.__name__) for typ in (TypeIdent,)])}, or 'NoneType', got type '{type(superclass_ident).__name__}'"
        assert isinstance(content_typelist, TypeIdentList), f"argument 'content_typelist' must be of type 'TypeIdentList', got type '{type(content_typelist).__name__}'"

        self._superclassident = superclass_ident
        self._content_typelist = content_typelist
        self._frontend_items = frontend_items

    def _finish_model(self, superclass, contents):
        assert isinstance(superclass, (ClassModel, NoneType)), f"argument 'superclass' must be one of types {', '.join([repr(typ.__name__) for typ in (ClassModel,)])}, or 'NoneType', got type '{type(superclass).__name__}'"
        #assert isinstance(contents, TypeList), f"argument 'contents' must be of type 'TypeList', got type '{type(contents).__name__}'"

        self.superclass = superclass
        self.contents = contents

        for item in self._items:
            print(self, item)
            item._model()

    '''
    def _model(self):
        if self._superclassident is not None:
            superclass = find_item_by_ident(self.location, self.module, self._superclassident)
            #print(f"{self} subclasses {self.superclass}")
        else:
            superclass = None
            #print(f"{self} has no superclass")

        if superclass is not None:
            base = superclass.contents
        else:
            base = {}

        ext = {}
        for name, typeident in self._content_typelist:
            ext[name] = find_item_by_ident(self.location, self.module, typeident)

        contents = {**base, **ext}

        for foo in contents.items():
            pass#print(foo)

        self._finish_model(superclass, contents)
        '''

class ModuleModel(NameSpaceModel):
    pass

@dataclass
class FuncTarget:

    basefunc     : FuncModel
    ret_type     : Union[ClassModel, TraitModel]
    arg_typelist : dict # [str, Union[ClassModel, TraitModel]]
