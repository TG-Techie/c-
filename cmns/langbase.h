#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>


//TODO: switch intclass, floatclass, etc to bool and
//      none class definition foamts ot avoind null pointers

#ifndef cmns_langbase_def
#define cmns_langbase_def

//cmns dev utilitieas b/c lazy
typedef unsigned int /*as*/ uint;

//memory functions and variables
//a list of all alloced var

//anytype prototype
typedef struct any_struct_type* /*as*/ anytype;


anytype _cmns_referenceto(anytype inst);
#define refto(varname) _cmns_referenceto(varname)

void _cmns_free(anytype inst);

void _cmns_dbg_print_vars();

void _cmns_record_var_as_alloced(anytype newvar);

void _cmns_gc();

void _cmns_dereference_var(anytype inst);
#define deref(varname) _cmns_dereference_var(varname);\
                        varname = NULL
#define rerefto(varname,newvar) _cmns_dereference_var(varname);\
                        varname = _cmns_referenceto(newvar)

void dereference_no_gc(anytype inst);


typedef struct cmns_struct_class{
    void (*free)(anytype);
}* cmnsclass;

typedef struct cmns_struct_base{
    uint refs;
    uint var_index;
    cmnsclass type;
}* cmnsbase;


//anytype definition
typedef struct any_struct_type {
    cmnsbase base;
}* anytype;

void freeany(anytype self);

cmnsclass anyclass;

void any_constructfn(anytype self);

anytype newany();

//typedefs for all built-in  types
typedef struct none_struct_type{
    cmnsbase base;
}* nonetype;

typedef struct bool_struct_type{
    cmnsbase base;
    bool value;
}* booltype;

typedef struct int_struct_type{
    cmnsbase base;
    int value;
}* inttype;

//define float double
typedef struct float_struct_type{
    cmnsbase base;
    float value;
}* floattype;

typedef struct str_struct_type{
    cmnsbase base;
    uint length; // length of the char array stored for ease
    char* values; // the char array location
}* strtype;

typedef struct arr_struct_type{
    cmnsbase base;
    //FIXME:need?:cmnsclass item_type;
    uint length; // current length
    uint capacity; // amount of allocated space;
    anytype itemarr; // array pointer
}* arrtype;

typedef struct dict_struct_type{
    cmnsbase base;
    //FIXME:need?:cmnsclass value_type;
    uint length; // current length
    uint capacity; // amount of allocated space;
    anytype keyarr; // pointer to carray
    anytype valuearr; // pointer to carray
}* dicttype;

#endif /* end of include guard: cmns_langbase_def */
