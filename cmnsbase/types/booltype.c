#include "booltype.h"

//since True and False abre both singtons of bool_struct_typ
//  they should not be collected
void freebool(booltype self){
    return;
}

const cmnsclass boolclass = &(cmns_struct_class){&freebool};

const booltype truelitrl = &(bool_struct_type){
    &((cmns_struct_base){0, 0, boolclass}),
    true
};

const booltype falselitrl = &(bool_struct_type){
    &((cmns_struct_base){0, 0, boolclass}),
    false
};

// other implementations:
/*
bool_struct_type _truelitrl_struct = {
    &((struct cmns_struct_base){0, 0, boolclass})
};
const booltype truelitrl = &_truelitrl_struct;
*/
/*
// make truelitrl
struct cmns_struct_base _truebase_struct = {0, 0, boolclass};
struct bool_struct_type _truelitrl_struct = {&_truebase_struct};
const booltype truelitrl = &_truelitrl_struct;
*/
// make falselitrl
/*
struct bool_struct_type _falselitrl_struct = {&_falsebase_struct};
const booltype falselitrl = &_falselitrl_struct;
*/
