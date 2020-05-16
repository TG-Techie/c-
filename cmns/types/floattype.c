#include "floattype.h"
#include "inttype.h"

void freefloat(floattype self){
    freeany((anytype)self);
}

cmnsclass floatclass = &((struct cmns_struct_class){&freefloat});

void float_constructfn(floattype self, float value){
    self->value = value;
}

floattype newfloat(float value){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = floatclass;
    floattype inst = malloc(sizeof(floattype));
    inst->base = base;
    float_constructfn(inst, value);
    _cmns_record_var_as_alloced((anytype)inst);
    return inst;
}

//method

// __add__ method for the + operator
floattype float___add__fn(floattype self, floattype other){
    return newfloat(self->value + other->value);
}

// __sub__ method for the - operator
floattype float___sub__fn(floattype self, floattype other){
    return newfloat(self->value - other->value);
}

// __mul__ method for the * operator
floattype float___mul__fn(floattype self, floattype other){
    return newfloat(self->value * other->value);
}

// __div__ method for the / operator
floattype float___div__fn(floattype self, floattype other){
    return newfloat((float)(self->value * other->value));
}

// __floordiv__ method for the // operator
inttype float___floordiv__fn(floattype self, floattype other){
    return newint((int)(self->value * other->value));
}
