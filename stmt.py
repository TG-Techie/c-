
class Stmt():
    pass

class PassStmt(Stmt):
    pass

class DelStmt(Stmt):
    pass

class ContinueStmt(Stmt):
    pass

class BreakStmt(Stmt):
    pass

class IfStmt(Stmt):
    pass

class WhileStmt(Stmt):
    pass

class ForStmt(Stmt):
    pass

class CountStmt(Stmt):
    pass

class ReturnStmt(Stmt):
    pass

class ItemAssignStmt(Stmt):
    pass

class IdentAssignStmt(Stmt):
    pass

class ExprStmt(Stmt):
    pass

class StmtBlock():

    def __init__(self, stmts, require_return=None):
        self._stmts = tuple(stmts)


    @classmethod
    def from_tree(cls, tree):
        pass\
        
