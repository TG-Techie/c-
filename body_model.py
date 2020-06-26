
binop_methodnames = {
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
inverse_binop_methodnames = {
    # comprarisons
    'noteq':'__eq__',
    'notin':'__contains__',
    #'isnot':'__is__'
}


class Pair():

    def __init__(self, name, type):
        assert isinstance(name, str)
        assert isinstance(type, Type)
        self.name = name
        self.type = type

    def __iter__(self):
        return iter((self.name, self.type))

class Var(Pair):

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)
        self.outstr = self.name+'_var'


class Arg(Pair):

    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        super().__init__(*args, **kwargs)
        self.outstr = self.name+'_var'


class Attr(Pair):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outstr = self.name+'_attr'

class Expr():

    def __init__(self, lineno, type):
        self.lineno = lineno
        self.type = type

    def get_attr(self, name):
        '''
        gets either an expression or a bound method w/ self in it
        '''
        pass

    def iscallable(self):
        return '__call__' in self.type

    def call(self):
        pass

class Litrl(Expr):

    def __init__(self, lineno, prefix, outstr):
        super().__init__(lineno, prefix)
        self.outstr = outstr

class TypeList():

    def __init__(self, pairs=None):

        if pairs is None:
            pairs = {}
        else:
            # TODO: ass assert for dict contents
            assert isinstance(pairs, esc), f"argument 'pairs' must be of type 'esc', got type '{type(pairs).__name__}'"

        self._pairs = pairs # dicts are ordered

    def __iter__(self):
        return iter(self._pairs.values())

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

    def __len__(self):
        return len(self._pairs)

class Scope():

    def __init__(self, outer, space=None):
        assert isinstance(outer, (Scope, NoneType)), f"argument 'outer' must be one of types {', '.join([repr(typ.__name__) for typ in (Scope,)])}, or 'NoneType', got type '{type(outer).__name__}'"

        self.outer = outer
        self._space = space

        self._vars = {} # name : Type

    @property
    def space(self):
        if self.outer is None:
            assert self._space is not None, "a root scope must have a NameSpace"
            return self._space
        elif self._space is None:
            return self.outer._space
        else:
            return self._space

    def __getitem__(self, name):
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"

        if name in self._vars:
            return self._vars[name]
        else:
            try:
                return self.outer[name]
            except:
                raise CMNSCompileTimeError(f"cannot find var '{name}' in scope '{self}'")

    def __setitem__(self, name, value):
        assert isinstance(name, str), f"argument 'name' must be of type 'str', got type '{type(name).__name__}'"

        if name in self._vars:
            self._vars[name] = value
        NOT_DONE_HERE
