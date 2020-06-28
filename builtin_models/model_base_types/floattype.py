from ..builtin_module import *

floattype._addmdls(
    *typecast_traits.values(),
    *arith_op_traits.values(),
    *math_op_traits.values(),
)

'''

# numbers first
traits = []
# typecast traits
traits += typecast_traits.values()
floattype._addmdls(
    BuiltinFuncModel(
        '__to_int__', inttype,
        dict(self=floattype)
    ),
    BuiltinFuncModel(
        '__to_float__', floattype,
        dict(self=floattype)
    ),
    BuiltinFuncModel(
        '__to_bool__', booltype,
        dict(self=floattype)
    ),
    BuiltinFuncModel(
        '__to_str__', strtype,
        dict(self=floattype)
    ),
)

# arithmetic operator traits
traits += arith_op_traits.values()
floattype._addmdls(
    BuiltinFuncModel(
        '__add__', inttype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__sub__', inttype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__mul__', inttype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__div__', floattype,
        dict(self=floattype, other=floatable)
    ),
    BuiltinFuncModel(
        '__mod__', inttype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__pow__', float,
        dict(self=floattype, other=floatable)
    ),
    BuiltinFuncModel(
        '__flr_div__', inttype,
        dict(self=floattype, other=intable)
    ),
)

# math operator traits
traits += math_op_traits.values()
floattype._addmdls(
    BuiltinFuncModel(
        '__eqls__', booltype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__less_than__', booltype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__grtr_than__', booltype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__less_eqls__', booltype,
        dict(self=floattype, other=intable)
    ),
    BuiltinFuncModel(
        '__grtr_eqls__', booltype,
        dict(self=floattype, other=intable)
    ),
)


# load in traits
floattype._addmdls(*traits)
'''

# bool

#bool_traits = []
