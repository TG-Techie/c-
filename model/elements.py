from lark import Tree


class CMNSCompileTimeError(Exception):
    def __init__(self, lineno, message):
        super().__init__(f"line {lineno}: {message}")


class CMNSRedefinitionError:
    pass


class NameSpace:
    def __init__(self, outer, lineno, name, tree):
        """
        desc:
        """
        assert isinstance(
            outer, (NameSpace, NoneType)
        ), "'outer' must be of type 'NameSpace' or value 'None'"
        assert (
            isinstance(name, str) and len(name) and name.isidentifier()
        ), "'name' must be of type 'str' and length >= 1"

        self._tree = tree
        self.lineno = lineno
        self.name = name
        self.space = space

        # self._initialised = False

        self.values = {}  # for variables / attributes
        self._functions = {}
        self.types = {}

    @property
    def functions(self):
        return self._functions

    @property
    def outprefix(self):
        return f"{self.space.outprefix}_{name}"

    def add_function(self, func):
        if func.name not in self._functions[func.name]:
            self._functions[func.name] = func
        else:
            raise CMNSRedefinitionError(
                self.lineno, f"cannot redefine {self.types[name]}, already defined."
            )

    def add_type(self, type):
        if type.name not in self._types:
            self.types[name] = trait
        else:
            raise CMNSRedefinitionError(
                self.lineno, f"cannot redefine {self.types[name]} to {trait}"
            )


class Function:
    def __init__(self, space, lineno, name, tree, outname=None):
        assert isinstance(
            space, (NameSpace, NoneType)
        ), "'space' must be of type 'NameSpace' or value 'None'"
        assert (
            isinstance(name, str) and len(name) and name.isidentifier()
        ), "'name' must be of type 'str' and length >= 1"

        if outname is None:
            outname = f"{space.prefix}_{name}"

        assert (
            isinstance(outname, str) and len(outname) and outname.isidentifier()
        ), "'outname' must be of type 'str' and length >= 1"

        self._tree = tree
        self.lineno = lineno
        self.space = space
        self.name = name
        self.outname = outname

        self._initialised = False

    def initialise(self):
        pass  # parses the given tree and asserts its own type

    def call(self, args):
        assert self._initialised, f"{self} not _initialised"


class Method(Function):
    pass


class Type(NameSpace):
    def __init__(self, space, lineno, name, tree, outname=None):
        assert isinstance(
            space, (NameSpace, NoneType)
        ), "'space' must be of type 'NameSpace' or value 'None'"
        assert (
            isinstance(name, str) and len(name) and name.isidentifier()
        ), "'name' must be of type 'str' and length >= 1"

        if outname is None:
            outname = f"{space.prefix}_{name}"

        assert (
            isinstance(outname, str)
            and len(outname.strip("_")) >= 3
            and outname.isidentifier()
        ), "'outname' must be of type 'str' and length >= 1"

        self.outname = outname

        super().__init__(space, lineno, tree, name)
        self._attrs = {}

    # change add_funtion into add_method
    add_method = NameSpace.add_function

    @property
    def add_function(self, *args, **kwargs):
        raise AttributeError("types don't have functions, they have methods")

    functions = add_function

    # change types to triats
    add_trait = NameSpace.add_type

    @property
    def add_type(self, *args, **kwargs):
        raise AttributeError("classes (types) cannot/do not have inner classes")

    types = add_type

    def add_attr(self, attr):
        if attr.name in self._attrs:
            raise CMNSRedefinitionError(
                self.lineno,
                f"{self._attrs[attr.name]} already defined, cannot be redefined. tried to redefine to {attr}",
            )
        else:
            self._attrs[attr.name] = attr

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

    def initialise(self):
        pass  # parses the given tree and asserts its own type


class Trait(NameSpace):

    # change add_funtion into add_method
    add_method = NameSpace.add_function

    @property
    def add_function(self, *args, **kwargs):
        raise AttributeError("types don't have functions, they have methods")

    functions = add_function

    # change types to triats
    add_trait = NameSpace.add_type

    @property
    def add_type(self, *args, **kwargs):
        raise AttributeError("classes (types) cannot/do not have inner classes")

    types = add_type

    def __eq__(self, other):
        if isinstance(other, Trait) and self is other:
            return True
        else:
            return True in [self == trait for trait in other.traits.values()]


# evaluatuation time model elements


class Scope:
    def __init__(self, space, outer):
        assert isinstance(
            space, (NameSpace, NoneType)
        ), "'space' must be of type 'NameSpace' or value 'None'"
        assert isinstance(
            outer, (Scope, NoneType)
        ), "'outer' must be of type 'Scope' or value 'None'"
        if outname is None:
            outname = f"{space.prefix}_{name}"

        assert (
            isinstance(outname, str)
            and len(outname.strip("_")) >= 3
            and outname.isidentifier()
        ), "'outname' must be of type 'str' and length >= 1"

        self._locals = {}

    @property
    def locals(self):
        return self._locals

    @property
    def all(self):
        if self.outer is not None:
            return {**self.locals, **self.outer.all}
        else:
            return self.locals

    def new_var(self, var):
        assert isinstance(var, Var), "'var' must be of type 'Var'"
        if var.name in self.locals:
            self._locals[var.name] = var
        elif (self.outer is not None) and (var.name in self.outer.all):
            if var.type == self.outer.all[var.name].type:
                self._locals[var.name] = var
            else:
                SHIT
        else:
            self._locals[var.name] = var


class Stmt:
    def __init__(self, scope, lineno, tree):

        self._tree = tree
        self.lineno = lineno
        self.scope = scope


class StmtBlock:
    def __init__(self, outer, lineno, tree):
        assert isinstance(outer, Scope), "'outer' must be of type 'Scope"

        self._tree = tree
        self.outer = outer
        self.lineno = lineno
        self.scope = Scope(
            outer.space, outer
        )  # make the scope for the indented block (differes from python)


class Expr:
    def __init__(self, scope, lineno, type):

        assert isinstance(scope, Scope), "'scope' must be of type 'Scope'"
        assert isinstance(
            type, (Type, Trait)
        ), "'type' must be of type 'Type' or of type 'Trait'"

        self.scope = scope
        self.lineno = lineno
        self.type = type


class Pair:
    def __init__(self, name, type, refcounted=True):
        assert isinstance(name, str), "'name' must be of type 'str'"
        assert isinstance(
            type, (Type, Trait)
        ), "'type' must be of type 'Type' or of type 'Trait'"

        self.name = name
        self.type = type


class Var(Pair):
    def __init__(self, *args, outname=None, **kwargs):
        super().__init__(self, *args, **kwargs)

        if outname is None:
            outname = self.name + "_var"


class Attr(Pair):
    def __init__(self, *args, outname=None, **kwargs):
        super().__init__(self, *args, **kwargs)

        if outname is None:
            outname = self.name + "_attr"
