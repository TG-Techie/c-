enable_comments = True
static_typing = False

class CMNSCompileTimeError(Exception):
    pass

class Pair():

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __iter__(self):
        return iter((self.name, self.type))

class Var(Pair):

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)
        self.outname = self.name+'_var'

class Arg(Pair):

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)
        self.outname = self.name+'_var'

class Attr(Pair):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outname = self.name+'_attr'

class Litrl():

    def __init__(self, type, source):
        self.type = type
        self.outstr = source

class TypeList():

    def __init__(self):
        self._pairs = {}

    """def add(self, var):
        if self.static:
            raise CMNSCompileTimeError("'TypeList' cannot be altered if static")
        if ((var.name in self._pairs) and (var.type is self[var.name].type))and static_typing:
            raise ValueError(f"var by name '{var.name}' already in 'TypeList'")
        else:
            self._pairs[var.name] = var

    def remove(self, var):
        if self.static:
            raise CMNSCompileTimeError("'TypeList' cannot be altered if static")
        if var.name not in self._pairs:
            raise CMNSCompileTimeError("cannot remove undeclared Pair'' from 'TypeList'")
        else:
            del self._pair[var.name]"""

    def __contains__(self, target):
        if isinstance(target, str):
            return target in self._pairs
        elif isinstance(target, pair):
            tup = tuple(target)
            return tup in [tuple(pair) for pait in self._pairs]
        else:
            raise ValueError("can only check if 'TypeList' contains a variable by c-name")

    def __getitem__(self, name):
        return self._pairs[name]

    def __setitem__(self, name, var):
        if name != var.name:
            raise ValueError(f"key '{name}' does not match the name in the given variable, '{name}' != '{var.name}'")
        else:
            self._pairs[name] = var

class Scope(TypeList):
    #globals = TypeList()
    types = []

    def __init__(self, outer=None):
        super().__init__()
        self.outer = outer
        #self.locals = TypeList()

    @property
    def locals(self):
        return self._pairs

    def __contains__(self, string):
        if string in self.locals:
            return True
        elif self.outer is not None and string in self.outer:
            return True
        else:
            return False

    def __getitem__(self, var):
        if var in self.locals:
            return  self.locals[var]
        elif self.outer is not None and var in self.outer:
            return  self.super[var]
        else:
            raise CMNSCompileTimeError("'{var}' not found in scope")

    def __setitem__(self, name, var):
        #check if the name is a valid name
        if name != var.name:
            raise ValueError(f"key '{name}' does not match the name in the given variable, '{name}' != '{var.name}'")
        if name in self.locals: # overwrite local, check if in local before outer
            self.locals[name] = var
        elif self.outer is not None and name in self.outer: # overwrite in outer scope if same type
            if var.type is self.outer[name].type:
                self.outer[name] = var
            else:
                raise CMNSCompileTimeError("cannot cast variables outsideof the local scope" #python auto cats string w/out a comma seperator
                    f"tried to cast '{name}' declared as a '{self.outer[name].type.name}' to a '{var.type.name}'")
        else:
            self.locals[name] = var

class Expr():

    def __init__(self, scope, type, outstr):
        self.scope = scope
        self.type = type
        self.outstr = outstr

class Function ():

    def __init__(self, name, type, argpairs):
        super().__init__()
        self.name = name
        self.type = type
        self.args = tuple(argpairs)

class Stmt():

    def __init__(self, scope=None, lines=None):
        self.scope = Scope(outer=scope)
        if lines is None:
            self.lines = []
        else:
            self.lines = lines


class Type():

    def __init__(self, name, methods=None):
        self.name = name
        if methods is None:
            self.methods = {}
        else:
            self.methods = mwthods

        self.outname = name+'type'

    def __repr__(self):
        return f"<cmnstype '{self.name}'>"

    def addmethod(self, name, type, args):
        if name not in self.methods:
            self.methods[name] = Function(f"{self.name}_{name}fn", type, args)
        else:
            raise ValueError(f"function '{name}' already defined in type {self.name}")

inttype = Type('int')
Scope.types.append(inttype)

strtype = Type('str')
Scope.types.append(strtype)

inttype.addmethod('__add__', inttype,
        (Pair('self', inttype), Pair('other', inttype))
)
inttype.addmethod('__str__', strtype,
        (Pair('self', inttype), Pair('other', inttype))
)
