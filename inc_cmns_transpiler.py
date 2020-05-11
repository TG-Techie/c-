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
        return Expr(scope, expr.type.methods[funcname].type, f"{expr.type.methods[funcname].outname}({expr.outstr}{outargs})")
    else:
        raise CMNSCompileTimeError(f"line #lineno not implemented#: expr '{expr.outstr}' of type '{expr.type.name}' has no method '{funcname}'")

def trans_expr(scope, expr):
    expr = expr.children[0] # all 'expr's only contain one child
    if expr.data == 'literal':
        litrl = trans_literal(expr)
        return Expr(scope, litrl.type, litrl.outstr)
    if expr.data == 'binop_expr':
        a = trans_expr(scope, expr.children[0])
        b = trans_expr(scope, expr.children[2])
        op = expr.children[1].children[0].data
        if op in binop_methodnames:
            return trans_method_call(scope, a, binop_methodnames[op], (b,))
        else:
            SHIT

def comment(cmnt):
    if enable_comments:
        return f"/*{cmnt}*/"
    else:
        return ''

def trans_stmt(scope, stmt):
    stmtmdl = Stmt(scope=scope)
    scope = stmtmdl.scope
    if stmt.data == 'assign_stmt':
        nametree, equals, expr, newline = stmt.children

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
                        stmtmdl.lines.append(f"rerefto({var.outname}, {expr.outstr});")
                else:
                    raise CMNSCompileTimeError(f"line {lineno}: cannot cast variables outside of the local scope, you tried to assign '{var.name}' declared as a '{scope[var.name].type.name}' to a '{var.type.name}'")

            else:
                stmtmdl.lines.append(f"rerefto({var.outname}, {expr.outstr});")
        else:
            scope.locals[var.name] = var
            stmtmdl.lines.append(comment(f"first assignment of '{var.name}' in scope"))
            stmtmdl.lines.append(f"{var.type.outname} {var.outname} = refto({expr.outstr});")
    elif stmt.data == 'if_stmt':
        print(stmt.pretty())
    else:
        print(stmt)
        raise NotImplementedError("unsupported stmt found")
    return stmtmdl

def trans_module(foo):
    scope = Scope()
    lines = []
    for foo in foo.children:
        if foo.data == 'stmt':
            lines += trans_stmt(scope, foo.children[0]).lines
        else:
            raise NotImplementedError(f"unsupported sentence '{foo.data}'")
    return lines

if __name__ == '__main__':
    paths =    ('./sentences/assign_int_lit.c-',
                './sentences/binop_add.c-',
                )
    for path in paths:
        with open(path) as file:
            tree = parse(file.read())
            print(tree.pretty())
            [print(line) for line in trans_module(tree)]
