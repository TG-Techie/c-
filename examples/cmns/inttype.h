#include "langbase.h"

// start int class def
typedef struct int_struct_type{
    cmnsbase base;
    int value;
}* inttype;

void freeint(inttype self);

cmnsclass intclass = &((cmnsclass){&freeint});

void int_constructfn(inttype self, int value);

#define intlitrl newint
inttype newint(int value);
