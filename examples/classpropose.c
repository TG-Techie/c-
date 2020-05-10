#include "cmnsbase.c"

typedef struct coord_struct_type {
    cmnsbase base;
    inttype x_attr;
    inttype y_attr;
}* coordtype;

void coord_constructfn(coordtype self, inttype x_arg, inttype y_arg){
    //self->x_attr;
    self->x_attr = refto(x_arg);
    //self->y_attr;
    self->y_attr = refto(y_arg);
}

void freecoord(coordtype inst){
    deref(inst->x_attr);
    _cmns_free(inst->x_attr);
    deref(inst->y_attr);
    _cmns_free(inst->y_attr);
    freeany(inst);
}

coordtype newcoord(inttype x_arg, inttype y_arg){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->free = &freecoord;
    coordtype inst = malloc(sizeof(coordtype));
    inst->base = base;

    coord_constructfn(inst, x_arg, y_arg);
    _cmns_record_var_as_alloced(inst);
    return inst;
}

void mainfn(){
    inttype x_var;
    x_var = refto(intlitrl(0));
    inttype y_var;
    y_var = refto(intlitrl(0));

    coordtype asside_var;
    asside_var = refto(newcoord(x_var, y_var));

    coordtype target_var;
    target_var = refto(newcoord(intlitrl(5), intlitrl(5)));

}
