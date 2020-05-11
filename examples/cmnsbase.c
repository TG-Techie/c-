#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>


//cmns dev utilitieas b/c lazy
typedef unsigned int uint;

//memory functions and variables
//a list of all alloced var

//anytype prototype
typedef struct any_struct_type* anytype;

//memory stacking stuff
#define _cmns_max_vars    ((int)20)
anytype _cmns_alloced_vars [_cmns_max_vars];
uint _cmns_next_alloced_var_index = 0;

//FIXME: add a cmnsclass typedef as a
//  cmns_struct_class pointer so ducktyping can identify the type
typedef struct cmns_struct_class{
    void (*free)(anytype self);
}* cmnsclass;

typedef struct cmns_struct_base{
    uint refs;
    uint _var_index;
    cmnsclass type;
}* cmnsbase;

typedef struct any_struct_type {
    cmnsbase base;
}* anytype;


anytype _cmns_referenceto(anytype inst){
    inst->base->refs += 1;
    return inst;
}

#define refto(varname) _cmns_referenceto(varname)

void _cmns_free(anytype inst){
    //printf("freeing: %d\n", inst);
    _cmns_alloced_vars[inst->base->_var_index] = NULL;
    inst->base->refs = 0;
    (inst->base->type->free)(inst);
}


void _cmns_dbg_print_vars(){
    printf("allocated_vars: ");
    for (int i=0; i<_cmns_max_vars; i++){
        if (_cmns_alloced_vars[i]){
            printf("%d, ", _cmns_alloced_vars[i]->base->refs);
        }
    }
    printf("\n");
}

void _cmns_record_var_as_alloced(anytype newvar){
    _cmns_alloced_vars[_cmns_next_alloced_var_index] = newvar;
    newvar->base->_var_index = _cmns_next_alloced_var_index;
    _cmns_next_alloced_var_index += 1;
    //printf("%d\n", newvar);
}

// scan and garbage collects any 0 reference items
// this function may be removed since dereferencing
// auto collects
void _cmns_gc(){
    int moveback = 0;
    //loopvars
    int refs;
    anytype var;
    //_cmns_print_vars();
    for (int i=0; i<_cmns_max_vars; i++){
        var = _cmns_alloced_vars[i];
        //printf("%d: (%d)\n", i, var);
        if (var){
            refs = var->base->refs;
            if (refs == 0){
                //printf("%d ", i);
                _cmns_free(var);
                //_cmns_alloced_vars[i] = NULL;
                moveback += 1;
            } else if (moveback > 1) {
                _cmns_alloced_vars[i-moveback] = var;
                var->base->_var_index = i-moveback;
                _cmns_alloced_vars[i] = NULL;
            }
        }
    }
    _cmns_next_alloced_var_index -= moveback;
    return;
}

void _cmns_dereference_var(anytype inst){
    if (inst){ // make tolerable to NULL pointers
        inst->base->refs -= 1;
        if (inst->base->refs == 0){
            //free the inst if there are no other references to it
            _cmns_free(inst);
        }
    } else {
        printf("NULL pointer passed to '_cmns_dereference_var' function!");
    }
}

#define deref(varname) _cmns_dereference_var(varname); varname = NULL
#define rerefto(varname,newvar) _cmns_dereference_var(varname); varname = _cmns_referenceto(newvar)

void dereference_no_gc(anytype inst){
    if (inst){
        inst->base->refs -= 1;
    }
}

#define refreturn(varname) dereference_no_gc(varname); return varname


// TYPE IMPLEMENTATION

void freeany(anytype self){
    free(self->base);
    free(self);
}

//cmnsclass anyclass = &(cmns_struct_class){.free=&freeany};
//cmns_struct_class _anyclass_struct;
//_anyclass_struct = {.free=&freeany};
//cmnsclass anyclass;
cmnsclass anyclass = &((cmnsclass){&freeany});

void any_constructfn(anytype self){
}

anytype newany(){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = anyclass;
    anytype inst = malloc(sizeof(anytype));
    inst->base = base;
    any_constructfn(inst);
    _cmns_record_var_as_alloced(inst);
    return inst;
}

// start int class def
typedef struct int_struct_type{
    cmnsbase base;
    //void (*_free)(struct int_struct_type* self);
    int value;
}* inttype;

void freeint(inttype self){
    freeany(self);
}

cmnsclass intclass = &((cmnsclass){&freeint});

void int_constructfn(inttype self, int value){
    self->value = value;
}

#define intlitrl newint
inttype newint(int value){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = intclass;
    inttype inst = malloc(sizeof(inttype));
    inst->base = base;
    int_constructfn(inst, value);
    _cmns_record_var_as_alloced(inst);
    return inst;
}
// end int class def

// start str class def
typedef struct str_struct_type{
    cmnsbase base;
    char* value;
}* strtype;

void freestr(strtype self){
    free(self->value);
    freeany(self);
    return;
}

cmnsclass strclass = &((cmnsclass){&freestr});

void str_constructfn(strtype self, char* contents){
    self->value = malloc(strlen(contents)+1);
    strcpy(self->value, contents);
}

#define strlitrl newstr
strtype newstr(char* contents){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = strclass;
    strtype inst = malloc(sizeof(strtype));
    inst->base = base;

    str_constructfn(inst, contents);
    _cmns_record_var_as_alloced(inst);
    return inst;
}
//end str class def

// start inttype methods
inttype int__addfn(inttype self, inttype other){
    return newint(self->value + other->value);
}

strtype int__tostr(inttype self){
    uint power = (int)(log10(self->value + 1) + 1);
    char string[power];

    uint remainder = self->value;
    uint place;
    //printf("self->value %d; power %d\n", self->value, power);
    //printf("%d\n", (uint)pow(10,0));
    for (uint index = 0; index < power; index++){
        place = (uint)pow(10, power-1-index);
        string[index] = (char)('0' + (remainder / place));
        //printf("remainder %d, place %d, index %d, string[index] %c\n", remainder, place, index, string[index]);
        remainder %= place;

    }

    return newstr(string);
}
// end inttype methods


//start strtype methods
strtype str__addfn(strtype self, strtype other){
    char c[(strlen(self->value) + strlen(other->value) + 1)];
    strcpy(c, self->value);
    strcat(c, other->value);
    return newstr(c);
}

//end strtype methods



//builtin fincs

void printfn(strtype out){
    printf("%s\n", out->value);
}

void mainfn();
int main(){
    mainfn();
    return 0;
}
