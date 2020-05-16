#include "../langbase.h"

// int typedef in langbase

void freestr(strtype self);

const cmnsclass strclass;

void str_constructfn(strtype self, char *values);

#define strlitrl newstr
strtype newstr(char *);


booltype str___eqls__fn(strtype self, strtype other);
