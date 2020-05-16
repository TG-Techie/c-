#include "file.h"

#ifndef _cmns_max_vars
    #define _cmns_max_vars  ((int)1024)
#endif

int main(){
    //if (sizeof(_cmns_alloced_vars) < 128){
    //    anytype cmns_alloced_vars[_cmns_max_vars]
    mainfn();
    _cmns_gc();
}
