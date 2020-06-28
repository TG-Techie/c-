from ..builtin_module import *

# numbers first
traits = []


# typecast traits
traits += typecast_traits.values()
intcls._addmdls(
    BuiltinFuncModel(
        '__to_int__', intcls,
        dict(self=intcls)
    ),
    BuiltinFuncModel(
        '__to_float__', floatcls,
        dict(self=intcls)
    ),
    BuiltinFuncModel(
        '__to_bool__', boolcls,
        dict(self=intcls)
    ),
    BuiltinFuncModel(
        '__to_str__', strcls,
        dict(self=intcls)
    ),
)

# arithmetic operator traits
traits += arith_op_traits.values()
intcls._addmdls(
    BuiltinFuncModel(
        '__add__', intcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__sub__', intcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__mul__', intcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__div__', floatcls,
        dict(self=intcls, other=floatable)
    ),
    BuiltinFuncModel(
        '__mod__', intcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__pow__', float,
        dict(self=intcls, other=floatable)
    ),
    BuiltinFuncModel(
        '__flr_div__', intcls,
        dict(self=intcls, other=intable)
    ),
)

# math operator traits
traits += math_op_traits.values()
intcls._addmdls(
    BuiltinFuncModel(
        '__eqls__', boolcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__less_than__', boolcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__grtr_than__', boolcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__less_eqls__', boolcls,
        dict(self=intcls, other=intable)
    ),
    BuiltinFuncModel(
        '__grtr_eqls__', boolcls,
        dict(self=intcls, other=intable)
    ),
)

# default tool traits
traits.append(tool_traits['indicie'])
intcls._addmdls(
    BuiltinFuncModel(
        '__index__', intcls,
        dict(self=intcls)
    ),
)


# load in traits
intcls._addmdls(*traits)


# bool

#bool_traits = []
