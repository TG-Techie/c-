#include "langbase.h"

void freefloat(inttype self){
    freeany(self);
}

void float_constructfn(inttype self, float value){
    self->value = value;
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
float float_from_anynumber(anytype var){
    if (var->base->type == intclass){
        return (float)(((inttype)var)->value);
    } else if (var->base->type == floatclass) {
        return        ((floattype)var)->value;
    } else {
        printf("could not cast to float at runtime");//, passed incorrect type '%s'", var->base->type-
        anytype SHIT = NULL;
        SHIT->base;
    }
}
*/

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
    return floatint(self->value * other->value);
}

// __floordiv__ method for the // operator
inttype float___floordiv__fn(floattype self, floattype other){
    return newint((int)(self->value * other->value));
}

