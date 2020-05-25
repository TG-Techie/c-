from elements import *
from types import *

class PassStmt(Stmt):
    pass

class BreakStmt(Stmt):
    pass

class ContinueStmt(Stmt):
    pass

class DelStmt(Stmt):

    def __init__(self, scope, lineno, exprs=None):
        super().__init__(scope, lineno)

        if exprs is None:
            exprs = []

        self.exprs = exprs

class CondBlock:

    def __init__(self, expr, block):
        assert self.expr.type == cnmsBool, f"the 'type' attribute of argument 'expr' must be of type 'Bool', got '{expr.type.name}"
        assert isinstance(block, StmtBlock), f"'block' must be of type 'StmtBlock', got '{block.__class__.__name__}"

        self.expr = expr
        self.block = block

class IfStmt(Stmt):

    def __init__(self, scope, lineno, ifblock, elifblocks, elseblock):
        assert isinstance(ifblock, CondBlock), f"'ifblock' must be of type 'CondBlock', got '{elifblock.__class__.__name__}'"
        assert all(isinstance(elifblock, CondBlock) for elifblock in elifblocks), f"'elifblocks' be of type 'list' or of type 'tuple' conatining only objects of type 'CondBlock'"

        super().__init__(scope, lineno)

        self.ifblock    = ifblock
        self.elifblocks = elifblocks
        self.elseblock  = elseblock

class WhileStmt(Stmt, CondBlock):

    def __init__(self, scope, lineno, expr, block):
        assert isinstance(block, CondBlock), "'block' must be of type 'CondBlock'"

        super().__init__(scope, lineno)
        CondBlock.__init__(self, expr, block)

class ReturnStmt(Stmt):

    def __init__(self, scope, lineno, expr=None):
        assert isinstance(expr, (Expr, NoneType)), "'expr' must be of type 'Expr' or of value 'None'"

        super().__init__(scope, lineno)

        if expr is None:
            expr = cmnsNone

        self.expr = expr

class AssignStmt(Stmt):

    def __init__(self, scope, lineno, value, *args, **kwargs):
        raise NotImplementedError('assignmetn statement modeling not implemted yet')
