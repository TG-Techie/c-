from ..builtin_module import *

addable = arith_op_traits['addable']

addable._addmdls(
    BuiltinFuncModel(
        '__add__', sometype,
        dict(self=sometype, other=sometype)
    )
)

# add targets for the builtin func targets
addable['__add__']._addtrgs(
    #inttype
    BuiltinFuncTarget(
        inttype, dict(self=inttype, other=inttype)
    ),
    BuiltinFuncTarget(
        floattype, dict(self=inttype, other=floattype)
    ),
    #floattype
    BuiltinFuncTarget(
        floattype, dict(self=floattype, other=inttype)
    ),
    BuiltinFuncTarget(
        floattype, dict(self=floattype, other=floattype)
    ),
    #booltype
    BuiltinFuncTarget(
        inttype, dict(self=booltype, other=inttype)
    ),
    BuiltinFuncTarget(
        floattype, dict(self=booltype, other=floattype)
    ),
    #strtype
    BuiltinFuncTarget(
        strtype, dict(self=strtype, other=strtype)
    ),
)
