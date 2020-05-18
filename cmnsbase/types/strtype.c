#include "../langbase.h"
#include "strtype.h"
#include "booltype.h"

void freestr(strtype self){
    free(self->values);
    //free(self->base);
    free(self);
}

const cmnsclass strclass = &((cmns_struct_class){&freestr});

void str_constructfn(strtype self, char* values){

    // constructor for the strtype

    // find the length of the str to duplicate it
    int length = strlen(values) + 1;

    //reserve a place in the heap to store the char[]
    char * arr = (char*)malloc(length);

    // copy the contents of the desired string into the heap
    strcpy(arr, values);

    //set the pointer in teh struct equal to the arr location
    self->values = arr;

}

strtype newstr(char* values){
    cmnsbase base = malloc(sizeof(cmns_struct_base));
    base->refs = 0;
    base->type = strclass;
    strtype inst = malloc(sizeof(str_struct_type));
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
