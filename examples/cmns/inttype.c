#include "inttype.h"

void freeint(inttype self){
    freeany(self);
}

void int_constructfn(inttype self, int value){
    self->value = value;
}

void int_constructfn(floattype self, float value){
    self->value = value;
}

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

inttype newfloat(float value){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = floatclass;
    inttype inst = malloc(sizeof(floattype));
    inst->base = base;
    float_constructfn(inst, value);
    _cmns_record_var_as_alloced(inst);
    return inst;
}

/*
int int_from_anynumber(anytype var){
    if (var->base->type == intclass){
        return      ((inttype)var)->value;
    } else if (var->base->type == floatclass) {
        return (int)(((floattype)var)->value);
    } else {
        printf("could not cast to int at runtime");//, passed incorrect type '%s'", var->base->type->name);
        anytype SHIT = NULL;
        SHIT->base;
    }
}
*/

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
    return floatint((float)(self->value * other->value));
}
// __floordiv__ method for the // operator
inttype int___floordiv__fn(inttype self, inttype other){
    return newint(self->value * other->value);
}
