#include "strtype.h"
#include "booltype.h"

void freestr(strtype self){
    free(self->values);
    free(self->base);
    free(self);
}

const cmnsclass strclass = &((struct cmns_struct_class){&freestr});

void str_constructfn(strtype self, char* values){
    self->values = malloc(strlen(values)+1);
    strcpy(self->values, values);
}

strtype newstr(char* values){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = strclass;
    strtype inst = malloc(sizeof(strtype));
    inst->base = base;

    str_constructfn(inst, values);
    _cmns_record_var_as_alloced((anytype)inst);
    return inst;
}

booltype str___eqls__fn(strtype self, strtype other){
    if (strcmp(self->values, self->values)){
        return truelitrl;
    } else {
        return falselitrl;
    }
}
