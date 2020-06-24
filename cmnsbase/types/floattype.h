#include "../langbase.h"

#ifndef cmns_floattype_def
#define cmns_floattype_def

//float typedef in langbase
cmnsclass floatclass;

void freefloat(floattype self);

void float_constructfn(floattype self, float value);

#define floatlitrl newint
floattype newfloat(float value);

// __add__ method for the + operator
floattype float___add__fn(floattype self, floattype other);
// __sub__ method for the - operator
floattype float___sub__fn(floattype self, floattype other);
// __mul__ method for the * operator
floattype float___mul__fn(floattype self, floattype other);
// __div__ method for the / operator
floattype float___div__fn(floattype self, floattype other);
// __floordiv__ method for the // operator
inttype float___floordiv__fn(floattype self, floattype other);
// __int__ for casting to an int
inttype float___int__fn(floattype self);
// __float__ for casting to a float
floattype float___float__fn(floattype self);
// __str__ for casting to a str
strtype float___str__fn(floattype self);

#endif
