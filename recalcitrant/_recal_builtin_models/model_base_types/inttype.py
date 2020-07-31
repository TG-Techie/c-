from ..builtin_module import *

inttype._addmdls(
    tool_traits['indicie'],
    *typecast_traits.values(),
    *arith_op_traits.values(),
    *math_op_traits.values(),
)

'''
# numbers first
traits = []


# typecast traits
traits += typecast_traits.values()
inttype._addmdls(
    BuiltinFuncModel(
        '__to_int__', inttype,
        dict(self=inttype)
    ),
    BuiltinFuncModel(
        '__to_float__', floattype,
        dict(self=inttype)
    ),
    BuiltinFuncModel(
        '__to_bool__', booltype,
        dict(self=inttype)
    ),
    BuiltinFuncModel(
        '__to_str__', strtype,
        dict(self=inttype)
    ),
)

# arithmetic operator traits
traits += arith_op_traits.values()
inttype._addmdls(
    BuiltinFuncModel(
        '__add__', inttype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__sub__', inttype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__mul__', inttype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__div__', floattype,
        dict(self=inttype, other=floatable)
    ),
    BuiltinFuncModel(
        '__mod__', inttype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__pow__', float,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__flr_div__', inttype,
        dict(self=inttype, other=inttype)
    ),
)

# math operator traits
traits += math_op_traits.values()
inttype._addmdls(
    BuiltinFuncModel(
        '__eqls__', booltype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__less_than__', booltype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__grtr_than__', booltype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__less_eqls__', booltype,
        dict(self=inttype, other=inttype)
    ),
    BuiltinFuncModel(
        '__grtr_eqls__', booltype,
        dict(self=inttype, other=inttype)
    ),
)

# default tool traits
traits.append(tool_traits['indicie'])
inttype._addmdls(
    BuiltinFuncModel(
        '__index__', inttype,
        dict(self=inttype)
    ),
)


# load in traits
inttype._addmdls(*traits)
'''

# bool

#bool_traits = []
