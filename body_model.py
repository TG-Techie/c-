
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
