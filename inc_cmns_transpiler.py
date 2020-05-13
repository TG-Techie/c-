from lark.tree import Tree
from lark import Token
from cmns_parse import parse
from cmns_model import *

######TODO: all functions return something to make expressions easier to deal with. with all taht means.
# make: booltype, make: nonetype


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

def trans_method_call(scope, expr, funcname, args):
    if funcname in expr.type.methods:
        outargs = ''.join([f', {argexpr.outstr}' for argexpr in args])
        return Expr(scope, expr.type.methods[funcname].type, f"{expr.type.methods[funcname].outstr}({expr.outstr}{outargs})")
    else:
        raise CMNSCompileTimeError(f"line {'UNKNOWN'}: expr '{expr.outstr}' of type '{expr.type.name}' has no method '{funcname}'")

def trans_expr(scope, tree):
    tree = tree.children[0] # all 'expr's only contain one child
    if tree.data == 'literal':
        litrl = trans_literal(tree)
        return Expr(scope, litrl.type, litrl.outstr)
    elif tree.data == 'binop_expr':
        a = trans_expr(scope, tree.children[0])
        b = trans_expr(scope, tree.children[2])
        op = tree.children[1].children[0].data
        if op in binop_methodnames:
            return trans_method_call(scope, a, binop_methodnames[op], (b,))
        else:
            SHIT
    elif tree.data == 'name':
        for varname, var in scope.all:
            #print(varname, var, str(tree.children[0]))
            if varname == str(tree.children[0]):
                return var
    else:
        SHIT

def comment(cmnt):
    if enable_comments:
        return f"/*{cmnt}*/"
    else:
        return ''

def trans_stmt(scope, stmt, rettype=None):
    stmtmdl = Stmt(scope=scope)
    #scope = stmtmdl.scope
    if stmt.data == 'assign_stmt':
        print(scope)
        nametree, expr, newline = stmt.children

        expr = trans_expr(scope, expr)
        varname, lineno = namefromtree(nametree)
        var = Var(scope, varname, expr.type)
        stmtmdl.lines.append(comment(f"line {lineno}: assign '{varname}'"))
        if var.name in scope:
            if var.type is not scope[var.name].type:
                # casting can only happen in the local scope, each block is it's own scope
                if static_typing:
                    raise CMNSCompileTimeError(f"line {lineno}: using static typing you cannot assign '{var.name}' declared as a '{scope[var.name].type.name}' to a '{var.type.name}'")
                elif var.name in scope.locals:
                        stmtmdl.lines.append(comment(f"casting '{var.name}' from type '{scope[var.name].type.name}' to  type '{var.type.name}'"))
                        scope[var.name] = var
                        stmtmdl.lines.append(f"rerefto({var.outstr}, {expr.outstr});")
                else:
                    raise CMNSCompileTimeError(f"line {lineno}: cannot cast variables outside of the local scope, you tried to assign '{var.name}' declared as a '{scope[var.name].type.name}' to a '{var.type.name}'")

            else:
                stmtmdl.lines.append(f"rerefto({var.outstr}, {expr.outstr});")
        else:
            scope.locals[var.name] = var
            stmtmdl.lines.append(comment(f"first assignment of '{var.name}' in scope"))
            stmtmdl.lines.append(f"{var.type.outstr} {var.outstr} = refto({expr.outstr});")
    elif stmt.data == 'return_stmt':
        if rettype is None:
            raise CMNSCompileTimeError(f"return type not specified for return on line {'UNKNOWN'}, given '{rettype}' instead")
        else:
            if len(stmt.children):
                retexpr = trans_expr(scope, stmt.children[0])
                foundtype = retexpr.type
            else:
                retexpr = None
                foundtype = nonetype
            if foundtype != rettype:
                #FIXME: add better error
                print( foundtype , rettype,  foundtype == rettype)
                raise CMNSCompileTimeError(f"type of return expression does not watch required return type ")

            stmtmdl.lines.append(comment("return routine"))
            stmtmdl.lines.append(f'anytype retval = refto({retexpr.outstr});')
            stmtmdl.lines.append(comment("return type validated at compile time"))
            for varname, var in scope.all:
                if var != retexpr:
                    stmtmdl.lines.append(f"deref({var.outstr});")
            stmtmdl.lines.append('_cmns_gc();')
            #if retexpr is not None:
            stmtmdl.lines.append(f'refreturn(retval);')
            #else:
            #    stmtmdl.lines.append(f'return nonelitrl();')
    else:
        raise NotImplementedError(f"unsupported stmt found: '{stmt.data}'")
    return stmtmdl

def trans_func(scope, tree, prefix=''):
    funcscope = Scope()
    #print([foo.data for foo in tree.children])
    children = tree.children
    if len(children) == 3:
        nametok, typelist, stmt_block = tree.children
        rettype = nonetype
    elif len(children) == 4:
        nametok, typelist, rettypetok, stmt_block = tree.children
        rettype = cmnstype_from_tree(scope, rettypetok)
    else:
        SHIT
    name = str(nametok.children[0])
    outname = prefix+name+'fn'
    params = trans_typelist(scope, typelist, content_type=Arg)
    for arg in params:
        funcscope[arg.name] = arg
    c_open_block = "{"
    paramsout = ", ".join([f"{arg.type.outstr} {arg.outstr}" for arg in params])
    lines = [f"{rettype.outstr} {outname}({paramsout}){c_open_block}", '    '+comment("argument refs to preclude gc")]
    lines += ['    '+f"refto({arg.outstr});" for arg in params]
    lines += ['    '+line for line in trans_stmt_block(funcscope, stmt_block, rettype=rettype)]
    #[print(arg.type, arg.outstr) for arg in params]

    lines.append("}")
    return Function(name, outname, rettype, params, lines=lines)

def cmnstype_from_tree(scope, tree):
    child = tree.children[0]
    if type(child) == Tree:
        rettypename = child.data
    else:
        rettypename = str(child)
    for cmnstype in scope.types:
        if rettypename == cmnstype.name:
            return cmnstype
            break
    else:
        raise CMNSCompileTimeError(f"type '{rettypename}' not found, line {'UNKNOWN'}")

    #return Function(name, prefix+name+'fn', rettype, )
def trans_typelist(scope, tree, content_type=Var) -> TypeList:
    pairs = TypeList()
    toks = tree.children
    #print(tree.pretty())
    argname = ''
    argtype = None
    while len(toks):
        tok = toks.pop(0)
        if tok.data == 'typename':
            argtype = cmnstype_from_tree(scope, tok)
        elif tok.data == 'name':

            argname = str(tok.children[0])
        elif tok.data == 'comma':
            pairs[argname] = content_type(scope, argname, argtype)
            argname = ''
            argtype = None
    if tok.data != 'comma':
        pairs[argname] = content_type(scope, argname, argtype)
        argname = ''
        argtype = None
    return pairs

def trans_stmt_block(scope, tree, rettype=None) -> list:
    scope = Scope(outer=scope)
    ls = list()
    for stmt in tree.children:
        if type(stmt) == Tree and stmt.data == 'stmt':
            ls += trans_stmt(scope, stmt.children[0], rettype=rettype).lines
    return ls

def trans_module(foo):
    scope = Scope()
    contents = []
    lines = []
    for foo in foo.children:
        if foo.data == 'stmt':
            #print('STMT!')
            contents.append(trans_stmt(scope, foo.children[0]))
        elif foo.data == 'funcdef':
            #print('FUNCDEF!')
            contents.append(trans_func(scope, foo))
        else:
            raise NotImplementedError(f"unsupported sentence '{foo.data}'")
    return contents


if __name__ == '__main__':
    paths =    ('./sentences/assign_int_lit.c-',
                './sentences/binop_add.c-',
                './sentences/funcdef.c-',
                )
    for path in paths:
        print(f"\ntesting: '{path}'")
        with open(path) as file:
            tree = parse(file.read())
            #print(tree.pretty())
            mod = trans_module(tree)
            print(mod)
            for thing in mod:
                print(f"\nprinting: {thing}")
                [print(line) for line in thing.lines]
            #[print(thing) for thing in mod]
            #for line in mod[0].lines:
            #    print(line)
