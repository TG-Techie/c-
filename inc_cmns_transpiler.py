from lark.tree import Tree
from lark import Token
from cmns_parse import parse
from cmns_model import *


#####TODO: make else not required
#FUTURE: add traits? get, set,


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
    elif litrl.data == 'bool':
        if litrl.children[0] == 'True':
            return Litrl(booltype, "truelitrl")
        elif litrl.children[0] == 'False':
            return Litrl(booltype, "falselitrl")
        else:
            SHIT
    elif litrl.data == 'nonetype':
        return Litrl(nonetype, "nonelitrl")
    #else:
    raise CMNSCompileTimeError(f"{litrl.pretty()} invalid literal")

def trans_method_call(scope, expr, funcname, args, lineno):
    if funcname in expr.type.methods:
        outargs = ''.join([f', {argexpr.outstr}' for argexpr in args])
        return Expr(scope, expr.type.methods[funcname].type, f"{expr.type.methods[funcname].outstr}({expr.outstr}{outargs})")
    else:
        raise CMNSCompileTimeError(f"line {'UNKNOWN'}: expr '{expr.outstr}' of type '{expr.type.name}' has no method '{funcname}'")

def trans_expr(scope, tree, lineno):
    roottree = tree
    tree = tree.children[0] # all 'expr's only contain one child
    if tree.data == 'literal':
        litrl = trans_literal(tree)
        return Expr(scope, litrl.type, litrl.outstr)
    elif tree.data == 'binop_expr':
        a = trans_expr(scope, tree.children[0], lineno)
        b = trans_expr(scope, tree.children[2], lineno)
        op = tree.children[1].children[0].data
        if op in binop_methodnames:
            return trans_method_call(scope, a, binop_methodnames[op], (b,), lineno)
        else:
            raise NotImplementedError(f"unimplemented binop '{tree.data}'")
    elif tree.data == 'name':
        for varname, var in scope.all:
            #print(varname, var, str(tree.children[0]))
            if varname == str(tree.children[0]):
                return var
    else:
        raise NotImplementedError(f"unimplemented expr '{tree.data}'")

def comment(cmnt):
    if enable_comments:
        return f"/*{cmnt}*/"
    else:
        return ''

def lineno_from_newline(nl):
    return nl.line
    #print('newline!', nl.line)


def trans_stmt(scope, tree, rettype):
    stmt = tree.children[0]
    stmtmdl = Stmt(scope=scope)
    #print(stmt.__repr__())
    if stmt.data == 'assign_stmt':
        #print(scope)
        nametree, expr, newline = stmt.children
        stmtmdl.lineno = lineno_from_newline(newline)

        expr = trans_expr(scope, expr, stmtmdl.lineno)
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
        stmtmdl.lineno = lineno_from_newline(stmt.children[-1])
        if rettype is None:
            raise CMNSCompileTimeError(f"return type not specified for return on line {stmtmdl.lineno}, given '{rettype}' instead, error in func?")
        else:

            if len(stmt.children) > 1:
                retexpr = trans_expr(scope, stmt.children[0], stmtmdl.lineno)
                foundtype = retexpr.type
            else:
                retexpr = None
                foundtype = nonetype
            if foundtype != rettype:
                #FIXME: add better error
                #print( foundtype , rettype,  foundtype == rettype)
                raise CMNSCompileTimeError(f"type '{foundtype.name}' of return expression does not watch required return type '{rettype.name}' ")

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
    elif stmt.data == 'if_stmt':
        children = stmt.children
        #print(children[0].children[0], children[1].data, children[-1].data)
        toplines, lineno = trans_stmt_block(scope, children[1], rettype)
        elselines, elselineno = trans_stmt_block(scope, children[-1], rettype)
        topexpr = trans_expr(scope, children[0], lineno)
        if topexpr.type != booltype:
            #FURTURE: use a cast attempt
            topexpr = trans_method_call(scope, topexpr, '__bool__', [], lineno)

        #if header: "if (){"
        stmtmdl.lines.append(f'if (({topexpr.outstr})->value)'+"{")
        stmtmdl.lines += ['    '+line for line in toplines]

        elifs = children[2:-1]
        while len(elifs):

            eliflines, eliflineno = trans_stmt_block(scope, elifs[1], rettype)
            elifexpr = trans_expr(scope, elifs[0], eliflineno)
            #remove first two items form list
            elifs = elifs[2:]

            if elifexpr.type != booltype:
                #FURTURE: use a cast attempt
                elifexpr = trans_method_call(scope, elifexpr, '__bool__', [], lineno)

            stmtmdl.lines.append("} "+f'else if (({elifexpr}.outstr)->value)'+"{")
            stmtmdl.lines += ['    '+line for line in eliflines]

        #else footer "} else {"
        stmtmdl.lines.append('} else {')
        stmtmdl.lines += ['    '+line for line in elselines]
        stmtmdl.lines.append('}')
    elif stmt.data == 'pass_stmt':
        stmtmdl.lines.append(comment("pass"))
    else:
        maybe_nl = stmt.children[-1]
        if isinstance(maybe_nl, Token) and maybe_nl.type == 'NEWLINE':
            lineno = lineno_from_newline(maybe_nl)
        else:
            lineno = 'UNKNOWN'
        try:
            pretty = stmt.pretty()
        except:
            pretty = ''
        raise NotImplementedError(f"unsupported stmt '{stmt.data}' found at newline {lineno}:\n{pretty}")
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
    blocklines, blocklineno = trans_stmt_block(funcscope, stmt_block, rettype=rettype)
    lines += ['    '+line for line in blocklines]
    #[print(arg.type, arg.outstr) for arg in params]

    if not lines[-1].strip().startswith('refreturn'):#stmt.data != 'return_stmt':

        if rettype != nonetype:
            print(rettype)
            raise CMNSCompileTimeError(f"return statement missing from end of function '{name}'")
        else:
            lines.append('    '+comment("return routine"))
            lines.append('    '+comment("automatically returning none"))
            #stmtmdl.lines.append(f'anytype retval = refto(nonelitrl);')
            lines.append('    '+comment("return type validated at compile time"))
            for varname, var in scope.all:
                stmtmdl.lines.append('    '+f"deref({var.outstr});")
            lines.append('    '+'_cmns_gc();')
            #if retexpr is not None:
            lines.append('    '+f'refreturn(nonelitrl);')


        ## check for return
        #for line in reversed(lines):
        #    if line.strip() = '}':
        #        continue
        #    else:
        #        if not line.strip().startswith('refreturn'):
        #            raise CMNSCompileTimeError("return statement missinf from end function")

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
    #else:
    raise CMNSCompileTimeError(f"type '{rettypename}' not found, line {'UNKNOWN'}")

    #return Function(name, prefix+name+'fn', rettype, )
def trans_typelist(scope, tree, content_type=Var) -> TypeList:
    pairs = TypeList()
    toks = tree.children
    #print(tree.pretty())
    argname = ''
    argtype = None
    tok = None
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
    if tok is not None and tok.data != 'comma':
        pairs[argname] = content_type(scope, argname, argtype)
        argname = ''
        argtype = None
    return pairs

def trans_stmt_block(scope, tree, rettype) -> list:
    scope = Scope(outer=scope)
    ls = list()
    #print(tree.pretty())
    #print(tree.data, len(tree.children) == 1, tree.data == 'stmt')
    if  len(tree.children) == 1: # if one-line smtmt def
        #print('one-line smtmt def')
        #print(tree.pretty())
        #print('trans_stmt_block', tree.data, tree.children[0].data)
        if tree.data == 'stmt':
            newstmt = trans_stmt(scope, tree, rettype)
        else:
            newstmt = trans_stmt(scope, tree.children[0], rettype)

        lineno = newstmt.lineno
        ls += newstmt.lines
    else:
        #print('mulit-line smtmt def')
        lineno = lineno_from_newline(tree.children[0])
        #print('stmt_block lineno rettype', lineno, rettype)
        #last_stmt = None
        #last_line_of_stmt = ''
        for stmt in tree.children:
            if type(stmt) == Tree and stmt.data == 'stmt':
                newstmt = trans_stmt(scope, stmt, rettype)
                finallineno = newstmt.lineno
                ls += newstmt.lines

                #last_stmt = stmt
                #if len(stmt.lines):
                #    last_line_of_stmt = stmt.lines[-1]
                #else:
                #    last_line_of_stmt = ''

        #check for return


        #if stmt.data != 'return_stmt':
        #    if stmt.data == 'if_stmt':
        #        if last_line_of_stmt.strip().startswith

    #print(lineno)
    return ls, lineno

def trans_module(foo):
    scope = Scope()
    contents = []
    lines = []
    for foo in foo.children:
        if foo.data == 'stmt':
            #print('STMT!')
            contents.append(trans_stmt(scope, foo, None))
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
                './sentences/ifstmt.c-'
                )
    for path in paths:
        print(f"\ntesting: '{path}'")
        with open(path) as file:
            text = file.read()
            print(text)

            tree = parse(text)
            print(tree.pretty())
            mod = trans_module(tree)
            #print(mod)
            for thing in mod:
                #print(f"\nprinting: {thing}")
                [print(line) for line in thing.lines]

            with open(path[:-3]+'_result.c', 'w') as outfile:
                outfile.truncate(0)
                outfile.write('#include "cmns/langbase.h"\n')
                for thing in mod:
                    outfile.write('\n')
                    [outfile.write(line+'\n') for line in thing.lines]
                outfile.write('\n')


            #[print(thing) for thing in mod]
            #for line in mod[0].lines:
            #    print(line)
