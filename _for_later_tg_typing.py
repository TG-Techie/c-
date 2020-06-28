import inspect as _inspect
from typing import *

from types import BuiltinFunctionType, BuiltinMethodType, FunctionType,\
    GeneratorType, LambdaType, MethodType, ModuleType

NoneType = type(None)

function_types = (
    FunctionType,
    LambdaType,
    MethodType
)

def strictlytyped(func):
    assert isinstance(func, (FunctionType, MethodType)), f"argument 'func' must be one of types {', '.join([repr(typ.__name__) for typ in (FunctionType, MethodType,)])}, or 'LambdaType', got type '{type(func).__name__}'"

    hints = func.__annotations__

    if 'return' in hints:
        has_ret_hint = True
        return_type = hints.pop('return')
        if not isinstance(return_type, (tuple, type)):
            return_type = type(return_type)
    else:
        has_ret_hint = False

    '''
    sig = _inspect.signature(func)
    print(dir(sig))
    print('parameters', sig.parameters)
    print('return_annotation', sig.return_annotation)

    args_match = []
    kwargs_match = {}

    for param in sig.parameters:'''


    def _stictly_typed_version(*args, **kwargs):

        ret = func(*args, **kwargs)

        if not sig.empty:
            if not _matches_type(ret, return_type):
                raise TypeError("")

        return ret

    return func

if __name__ == '__main__':
    @strictlytyped
    def foo(
        x : str,
        y : Union[str, int],
        kw : bool = False
            ) -> None:
        pass
