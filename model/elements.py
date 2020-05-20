
class CMNSCompileTimeError(Exception):

    def __init__(self, lineno, message):
        super().__init__(f"line {lineno}: {message}")

class CMNSDefinitionError:
    pass

class NameSpace():

    def __init__(self, outer, lineno, name, tree):
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

        #self.values = {} # for global variables
        self._functions = {}
        self.types = {}

    @property
    def functions(self):
        return self._functions

    @property
    def outprefix(self):
        return f"{self.space.outprefix}_{name}"

    def add_function(self, func):
        if self._functions[name] = func
        else:
            raise CMNSDeclarationError(self.lineno, f"cannot redefine {self.types[name]}, already defined.")
        return func

    def add_type(self, type):
        if type.name not in self._types:
            self.types[name] = trait
        else:
            raise CMNSDeclarationError(self.lineno, f"cannot redefine {self.types[name]} to {trait}")
        return type

class Function():

    def __init__(self, space, lineno, name, tree, outname=None):
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

class Type(NameSpace):

    def __init__(self, space, lineno, name, tree, outname=None):
        assert isinstance(space, (NameSpace)), "'outer' must be of type 'NameSpace' or value 'None'"
        assert isinstance(name, str) and len(name)\
            and name.isidentifier(), "'name' must be of type 'str' and length >= 1"

        if outname is None:
            outname = f"{space.prefix}_{name}"

        assert isinstance(outname, str) and len(outname.strip('_')) >= 3\
            and outname.isidentifier(), "'outname' must be of type 'str' and length >= 1"

        self.outname = outname

        super().__init__(space, lineno, tree, name)

    # change add_funtion into add_method
    add_method = NameSpace.add_function
    add_function = property(lambda self: raise AttributeError("types don't have functions, they have methods"))
    functions = add_function

    # change types to triats
    add_trait = NameSpace.add_type
    add_type = property(lambda self: raise AttributeError("classes (types) cannot have inner classes"))
    types = add_type

    @property
    def methods(self):
        return self._functions

    @property
    def traits(self):
        return self._types

    def __eq__(self, other):
        if isinstance(other, Trait):
            return other == self
        else:
            return self is other

def Trait(Type):

    def __eq__(self, other):
        if isinstance(other, Trait) and self is other:
            return True
        else:
            return True in [self == trait for trait in other.traits.values()]
