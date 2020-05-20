

class NameSpace():

    def __init__(self, outer, lineno, tree, name):
        """
        desc:
        """
        assert isinstance(outer, (NameSpace, NoneType)), "'outer' must be of type 'NameSpace' or value 'None'"
        assert isinstance(name, str) and len(name)\
            and name.isidentifier(), "'name' must be of type 'str' and length >= 1"

        self._tree = tree
        self.lineno = lineno
        self.name = name
        self.space = space

        #self._initialised = False

        #self.values = {}
        self.functions = {}
        self.traits = {}
        self.types = {}

    @property
    def outprefix(self):
        return f"{self.space.outprefix}_{name}"

    def new_function(self, name):
        func = Function(self, name)
        self.functions[name] = func
        return func

    def new_trait(self, name):
        trait = Trait(self, name)
        self.traits[name] = trait
        return trait

    def new_type(self, name):
        type = Type(self, name)
        self.types[name] = type
        return type

class Function():

    def __init__(self, space, lineno, tree, name, outname=None):
        assert isinstance(space, (NameSpace)), "'outer' must be of type 'NameSpace' or value 'None'"
        assert isinstance(name, str) and len(name)\
            and name.isidentifier(), "'name' must be of type 'str' and length >= 1"

        if outname is None:
            outname = f"{space.prefix}_{name}"

        assert isinstance(outname, str) and len(outname)\
            and outname.isidentifier(), "'outname' must be of type 'str' and length >= 1"

        self._tree = tree
        self.lineno = lineno
        self.space = space
        self.name = name
        self.outname = outname

        self._initialised = False

    def initialise(self):
        pass # parses the given tree and asserts its own type

    def call(self, args):
        assert self._initialised, f"{self} not _initialised"
