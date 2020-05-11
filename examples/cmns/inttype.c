#include "inttype.h"

void freeint(inttype self){
    freeany(self);
}

void constructint(inttype self, int value){
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
