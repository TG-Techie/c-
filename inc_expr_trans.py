from cmns_parse import parse

######TODO: add calllese start with capitcal, vars/attrs start with lower
######TODO: all functions return something to make expressions easier to deal with. with all taht means.
# make: booltype, make: nonetype

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

    def __init__(self, static = False):
        self._pairs = {}
        self.static = static

    def add(self, var):
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
            del self._pair[var.name]

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

class Scope():
    globals = TypeList()
    types = []

    def __init__(self):
        self.locals = TypeList()

    def __contains__(self, string):
        if string in self.locals:
            return True
        elif string in self.globals:
            return True
        else:
            return False

    def __contains__(self, var):
        return (var in self.locals) or (var in self.globals)

    def __getitem__(self, var):
        if var in self.locals:
            return  self.locals[var]
        elif var in self.globals:
            return  self.globals[var]
        else:
            raise CMNSCompileTimeError("'{var}' not in 'TypeList'")

    def __setitem__(self, name, value):
        if name in self.globals:
            self.globals.add(value)
        elif name in self.locals:
            self.locals.add(value)
        else:
            print(f"name:{name}, value:{value}, value.type:{value.type.name}")
            raise CMNSCompileTimeError('sh*t! soemthing when wrong with scoping')

class Expr():

    def __init__(self, scope, type, outstr):
        self.scope = scope
        self.type = type
        self.outstr = outstr

class Function (Scope):

    def __init__(self, selfpair, argpairs):
        super().__init__()
        self.name, self.returntype = selfpair
        self.args = tuple(argpairs)

class Stmt():
    
    def __init__(self, lines):
        self.lines = lines

class Type():

    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

        self.outstr = name+'type'

    def __repr__(self):
        return f"<cmnstype '{self.name}'>"

intfuncs = []
inttype = Type('int', intfuncs)
Scope.types.append(inttype)
strfuncs = []
strtype = Type('str', strfuncs)
Scope.types.append(strtype)

intfuncs += [
    Function( Pair('__add__', inttype),
        (Pair('self', inttype), Pair('other', inttype))
    ),
    Function( Pair('__str__', strtype),
        (Pair('self', inttype), Pair('other', inttype))
    ),
]

def namefromtree(nametree):
    #FIXME: make work for dotting and such
    if len(nametree.children) == 1:
        tok = nametree.children[0]
        return str(tok), int(tok.line)

def trans_literal(litrl):
    litrl = litrl.children[0]
    if litrl.data == 'number':
        num = litrl.children[0]
        if num.data == 'integer':
            tok = num.children[0]
            #tok.type is how to get the 'DEC_NUMBER' or other token identifier
            return Litrl(inttype, f"intlitrl({int(tok)})")
        else:
            raise Exception(f"{num, num.children}")
    elif litrl.data == 'string':
        string = litrl.children[0]
        litrl_text = str(string).strip('"' + "'")
        return Litrl(strtype, f'''strlitrl("{litrl_text}")''')
    else:
        raise CMNSCompileTimeError(f"{litrl.pretty()} invalid literal")

def trans_expr(scope, expr):
    expr = expr.children[0] # all 'expr's only contain one child
    if expr.data == 'literal':
        litrl = trans_literal(expr)
        return Expr(scope, litrl.type, litrl.outstr)

def comment(cmnt):
    if enable_comments:
        return f"/*{cmnt}*/"
    else:
        return ''

def trans_stmt(scope, stmt):
    lines = []
    if stmt.data == 'assign_stmt':
        nametree, equals, expr, newline = stmt.children
        expr = trans_expr(scope, expr)
        varname, lineno = namefromtree(nametree)
        var = Var(scope, varname, expr.type)
        lines.append(comment(f"line {lineno}: assign '{varname}'"))
        if var.name in scope:
            if var.type is not scope[var.name].type:
                if static_typing:
                    raise CMNSCompileTimeError(f"line {lineno}: cannot assign {var.name} declared as '{scope[var.name].type.name}' to '{var.type.name}'")
                else:

                    lines.append(comment(f"casting '{var.name}' from type '{scope[var.name].type.name}' to  type '{var.type.name}'"))
                    scope[var.name] = var
                    lines.append(f"rerefto({var.outname}, {expr.outstr});")

            else:
                lines.append(f"rerefto({var.outname}, {expr.outstr});")
        else:
            scope.locals.add(var)
            lines.append(comment(f"first assignment of '{var.name}' in scope"))
            lines.append(f"{var.type.outstr} {var.outname} = refto({expr.outstr});")

    return lines

def trans_module(foo):
    scope = Scope()
    lines = []
    for foo in foo.children:
        if foo.data == 'stmt':
            lines += trans_stmt(scope, foo.children[0])
        else:
            raise NotImplementedError(f"unsupported sentence '{foo.data}'")
    return Stmt(lines)

if __name__ == '__main__':
    with open('./sentences/assign_int_lit.c-') as file:
        tree = parse(file.read())
        print(tree.pretty())
        [print(line) for line in trans_module(tree)]
