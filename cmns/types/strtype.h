#include "../langbase.h"

// int typedef in langbase

void freeint(inttype self);

cmnsclass intclass = &((cmnsclass){&freeint});

void int_constructfn(inttype self, int value);

#define intlitrl newint
inttype newint(int value);
