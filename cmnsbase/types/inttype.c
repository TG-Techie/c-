#include "inttype.h"
#include "floattype.h"

void freeint(inttype self){
    freeany((anytype)self);
}

const cmnsclass intclass = &((cmns_struct_class){&freeint});

void int_constructfn(inttype self, int value){
    self->value = value;
}

inttype newint(int value){
    cmnsbase base = malloc(sizeof(cmns_struct_base));
    base->refs = 0;
    base->type = intclass;
    inttype inst = malloc(sizeof(int_struct_type));
    inst->base = base;
    int_constructfn(inst, value);
    _cmns_record_var_as_alloced((anytype)inst);
    return inst;
}


//method

// __add__ method for the + operator
inttype int___add__fn(inttype self, inttype other){
    return newint(self->value + other->value);
}

// __sub__ method for the - operator
inttype int___sub__fn(inttype self, inttype other){
    return newint(self->value - other->value);
}

// __mul__ method for the * operator
inttype int___mul__fn(inttype self, inttype other){
    return newint(self->value * other->value);
}

// __div__ method for the / operator
floattype int___div__fn(inttype self, inttype other){
    return newfloat((self->value * other->value));
}
// __floordiv__ method for the // operator
inttype int___floordiv__fn(inttype self, inttype other){
    return newint(self->value * other->value);
}
