from .builtin_module import *
#add traits to builtin types

inttype._addmdls(
    tool_traits['indicie'],
    *typecast_traits.values(),
    *arith_op_traits.values(),
    *math_op_traits.values(),
)

floattype._addmdls(
    *typecast_traits.values(),
    *arith_op_traits.values(),
    *math_op_traits.values(),
)

booltype._addmdls(
    *typecast_traits.values(),
    *arith_op_traits.values(),
    *math_op_traits.values(),
)

strtype._addmdls(
    math_op_traits['eqls_cmpable'],
    tool_traits['lengthed'],
    *typecast_traits.values(),
    *arith_op_traits.values(),
)

nonetype._addmdls(
    boolable,
    strable,
    math_op_traits['eqls_cmpable'],
)



# below was before func targer
#from . import inttype
#from . import floattype
#from . import booltype
#from . import strtype
#from . import nonetype
#from . import sometype
