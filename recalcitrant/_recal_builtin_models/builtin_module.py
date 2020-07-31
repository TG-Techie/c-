from typing import *
from dataclasses import dataclass

from lexer_parser import Location
import _models
from _models import *

builtin_location = _bltn_loc = Location('[builtin_module]', None)

builtin_module = ModuleModel(builtin_location, 'builtins', None)
_models._builtintypes_module_model = builtin_module

class BuiltinModelElement(ModelElement):

    def _addmdls(self, *mdls):
        for mdl in mdls:
            self[mdl.name] = mdl

@dataclass
class BuiltinClassModel(ClassModel, ModelElement):

    # shared with all builtins
    location = builtin_location
    superclass = None
    contents = {}

    def __init__(self, name, traits=None, funcs=None):

        if traits is None:
            traits = []
        if funcs is None:
            funcs = {}

        self.name = name
        self.traits = traits
        self.funcs = funcs

        builtin_module[name] = self


@dataclass
class BuiltinClassModel(ClassModel, BuiltinModelElement):

    _all = []

    # shared with all builtins
    location = builtin_location
    module = builtin_module
    superclass = None
    contents = {}

    def __init__(self, name, traits=None, items=None):

        if items is None:
            items = {}

        self.name = name
        self.traits = traits
        self.items = self._items =  items

        builtin_module[name] = self

        self._all.append(self)

@dataclass
class BuiltinTraitModel(TraitModel, BuiltinModelElement):

    _all = []

    # shared with all builtins
    location = builtin_location
    module = builtin_module

    def __init__(self, name):

        self.name = name
        self.items = self._items = {}

        builtin_module[name] = self

        self._all.append(self)

@dataclass
class BuiltinFuncModel(FuncModel, BuiltinModelElement):

    _all = []

    # shared with all builtins
    location = builtin_location
    module = builtin_module

    body_model = None

    def __init__(self, name, ret_type=None, typelist=None):

        if typelist is None:
            typelist = dict

        self.name = name
        self.ret_type = None
        self.typelist = {}
        self.targets = []

        builtin_module[name] = self

        self._all.append(self)


    def _addtrgs(self, *trgs):
        for trg in trgs:
            trg.basefunc = self
            self.targets.append(trg)

class BuiltinFuncTarget(FuncTarget):

    def __init__(
            ret_type     : Union[ClassModel, TraitModel],
            arg_typelist : dict, # [str, Union[ClassModel, TraitModel]]
            basefunc     : FuncModel = None,
        ):
        super().__init__(basefunc, ret_type, arg_typelist)




#base types
sometype     = BuiltinClassModel('SomeType')
inttype          = BuiltinClassModel('Int')
floattype        = BuiltinClassModel('Float')
booltype         = BuiltinClassModel('Bool')
strtype          = BuiltinClassModel('Str')
nonetype     = BuiltinClassModel('NoneType')

intable     = BuiltinTraitModel('Intable') # __to_int__
floatable   = BuiltinTraitModel('Floatable') # __to_float__
boolable    = BuiltinTraitModel('Boolable') # __to_bool__
strable     = BuiltinTraitModel('Strable') # __to_str__

# typecast traits
typecast_traits = dict(
    intable     = intable,
    floatable   = floatable,
    boolable    = boolable,
    strable     = strable,
)

# default tool traits
tool_traits = dict(
    magnitudinous   = BuiltinTraitModel('Magnitudinous'), # __mag__
    lengthed        = BuiltinTraitModel('Lengthed'), # __len__
    indicie         = BuiltinTraitModel('Indice'), # __index__
)

# arithmetic operator traits
arith_op_traits = dict(
    addable          = BuiltinTraitModel('_Addable_'), # __add__
    subtractable     = BuiltinTraitModel('_Subtractable_'), # __sub__
    multipliable     = BuiltinTraitModel('_Multipliable_'), # __mul__
    divisable        = BuiltinTraitModel('_Divisible_'), # __div__
    modulatable      = BuiltinTraitModel('_Modulatable_'), # __mod__
    exponentbase     = BuiltinTraitModel('_ExponentBase_'), # __pow__
    floordiv         = BuiltinTraitModel('_FloorDivisible_'), # __flr_div__
)


# math operator traits
math_op_traits = dict(
    eqls_cmpable            = BuiltinTraitModel('_EqualsComparable_'),#__
    lsth_cmpable            = BuiltinTraitModel('_LessThenComparable_'),
    grth_cmpable            = BuiltinTraitModel('_GreaterThanComparable_'),
    lstn_eqls_cmpable       = BuiltinTraitModel('_LessThanEqualComparable_'),
    grth_eqls_cmpable       = BuiltinTraitModel('_GreaterThanEqualComparable_'),
    contains                = BuiltinTraitModel('_Contains_'),
)

# typecast functions
typecast_funcs = dict(
    int     = BuiltinFuncModel('int'),
    float   = BuiltinFuncModel('float'),
    bool    = BuiltinFuncModel('bool'),
    str     = BuiltinFuncModel('str'),
)

# default tool funcs
tool_funcs = dict(
    len     = BuiltinFuncModel('len'),
    mag     = BuiltinFuncModel('mag'),
)
