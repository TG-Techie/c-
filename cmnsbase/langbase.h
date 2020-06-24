#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

/* // potential build tool replacements
re.findall('#include[a \t]*.*\n', x)
['#include <stdlib.h>\n', '#include <stdio.h>\n', '#include <string.h>\n', '#include <stdbool.h>\n', '#include <math.h>\n']
>>> includes = re.findall('#include[a \t]*.*\n', x)
>>> incs = includes
>>> incs
['#include <stdlib.h>\n', '#include <stdio.h>\n', '#include <string.h>\n', '#include <stdbool.h>\n', '#include <math.h>\n']
>>> paths = [path.split() for path in incs]
>>> paths = [path.split()[-1] for path in incs]
>>>
>>> paths
['<stdlib.h>', '<stdio.h>', '<string.h>', '<stdbool.h>', '<math.h>']
>>>
*/

/*
build command
gcc  -Wno-incompatible-function-pointer-types -Wno-incompatible-pointer-types atest.c langbase.c file.c types/booltype.c types/floattype.c types/inttype.c types/nonetype.c types/strtype.c functions/print.c

*/
//TODO: switch intclass, floatclass, etc to bool and
//      none class definition foamts ot avoind null pointers

#ifndef cmns_langbase_def
#define cmns_langbase_def


//cmns dev utilitieas b/c lazy
typedef unsigned int /*as*/ uint;

//memory functions and variables
//a list of all alloced var

//anytype prototype
typedef struct _any_t /*as*/ *anytype, any_struct_type;


anytype _cmns_referenceto(anytype inst);

void _cmns_free(anytype inst);

void _cmns_dbg_print_vars();

void _cmns_record_var_as_alloced(anytype newvar);

void _cmns_gc();

void _cmns_dereference_var(anytype inst);

void dereference_no_gc(anytype inst);


#define refto(varname) _cmns_referenceto((anytype)varname)

#define deref(varname) _cmns_dereference_var((anytype)varname);\
                        varname = NULL

#define rerefto(varname,newvar) _cmns_dereference_var((anytype)varname);\
                        varname = _cmns_referenceto((anytype)newvar)

#define refreturn(varname) dereference_no_gc((anytype)varname);\
                        return varname


typedef struct {
    void (*free)(anytype);
}* cmnsclass, cmns_struct_class;

typedef struct {
    uint refs;
    uint var_index;
    cmnsclass type;
}* cmnsbase, cmns_struct_base;


//anytype definition
typedef struct _any_t {
    cmnsbase base;
}* anytype, any_struct_type;

void freeany(anytype self);

cmnsclass anyclass;

void any_constructfn(anytype self);

anytype newany();

//typedefs for all built-in  types
typedef struct {
    cmnsbase base;
}* nonetype, none_struct_type;

typedef struct {
    cmnsbase base;
    bool value;
}* booltype, bool_struct_type;

typedef struct {
    cmnsbase base;
    int value;
}* inttype, int_struct_type;

//define float double
typedef struct {
    cmnsbase base;
    float value;
}* floattype, float_struct_type;

typedef struct {
    cmnsbase base;
    uint length; // length of the char array stored for ease
    char* values; // the char array location
}* strtype, str_struct_type;

typedef struct {
    cmnsbase base;
    //FIXME:need?:cmnsclass item_type;
    uint length; // current length
    uint capacity; // amount of allocated space;
    anytype itemarr; // array pointer
}* arrtype, arr_struct_type;

typedef struct {
    cmnsbase base;
    //FIXME:need?:cmnsclass value_type;
    uint length; // current length
    uint capacity; // amount of allocated space;
    anytype keyarr; // pointer to carray
    anytype valuearr; // pointer to carray
}* dicttype, dict_struct_type;

#endif /* end of include guard: cmns_langbase_def */
