from . elements import *

class CMNSTypeError(CMNSCompileTimeError):
    pass

class literalExpr(Expr):

    def __init__(self, scope, lineno, type, value):
        super().__init__(scope, lineno, type)
        self.value = value

class NewExpr(Expr):

    def __init__(self, scope, lineno, type, args):
        assert isinstance(type, Type), "'type' must be of type 'Type'"
        super().__init__(scope, lineno, type)
        #FIXME: implement constructors
        for index, arg_params in enumerate(zip(args, type.attrs.values())):
            arg, attr = arg_params
            if arg.type != attr.type:
                raise CMNSTypeError(lineno, f"incompatible type for argument"\
                    f"number {index+1}.  expects {attr.type}, got {arg.type}")
        else:
            self.args = args

class FuncCallExpr(Expr):

    def __init__(self, scope, lineno, func, args):
        assert isinstance(func, Function), "'func' must be of type 'Function'"
        self.func = func
        super().__init__(scope, lineno, func.type)
        for index, arg_params in enumerate(zip(args, func.args.values())):
            arg, param = arg_params
            if arg.type != param.type:
                raise CMNSTypeError(lineno, f"incompatible type for argument"\
                    f"number {index+1}.  expects {param.type}, got {arg.type}")
        else:
            self.args = args

class MethodCallExpr(FuncCallExpr):

    def __init__(self, scope, lineno, inst, func, args):
        super().__init__(self, scope, lineno, func, (inst, *args))
        self.inst = inst

class VarExpr(Expr):

    def __init__(self, scope, lineno, type, var):
        super().__init__(scope, lineno, type)
        self.var = var

class BinopExpr(Expr):

    def __init__(self, scope, lineno, type, kind, expr_a, expr_b):
        super().__init__(scope, lineno, type)
        self.kind = kind
        self.expr_a = expr_a
        self.expr_b = expr_b

class WrapperExpr(Expr):

    def __init__(self, scope, lineno, type, kind, expr):
        super().__init__(scope, lineno, type)
        self.kind = kind
        self.expr = expr


binop_method_names = {
    # artihmetic
    'add':'__add__',
    'sub':'__sub__',
    'mul':'__mul__',
    'div':'__div__',
    'mod':'__mod__',
    'pow':'__pow__',
    'floordiv':'__floordiv__',
    # comprarisons
    'eq':'__eqls__',
    'ls':'__lessthan__',
    'gr':'__grtrthan__',
    'lesseq':'__lesseqls__',
    'grtreq':'__grtreqls__',
    #semantic
}

# binops that ar teh "!(expr)" of other binops
inverse_binop_method_names = {
    # comprarisons
    'noteq':'__eq__',
    'notin':'__contains__',
    #'isnot':'__is__'
}
