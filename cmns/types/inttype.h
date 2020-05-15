#include "../langbase.h"

#ifndef cmns_inttype_def
#define cmns_inttype_def
// int typedef in langbase

cmnsclass intclass;

void freeint(inttype self);

void int_constructfn(inttype self, int value);

#define intlitrl newint
inttype newint(int value);

// mathematical operator methods
// __add__ method for the + operator
inttype     int___add__fn(inttype self, inttype other);
// __sub__ method for the - operator
inttype     int___sub__fn(inttype self, inttype other);
// __mul__ method for the * operator
inttype     int___mul__fn(inttype self, inttype other);
// __div__ method for the / operator
floattype   int___div__fn(inttype self, inttype other);
// __floordiv__ method for the // operator
inttype     int___floordiv__fn(inttype self, inttype other);

// casting / traits
// __bool__ for casting to an int
booltype   int___bool__fn(inttype self);
// __int__ for casting to an int
inttype     int___int__fn(inttype self);
// __float__ for casting to a float
floattype   int___float__fn(inttype self);
// __str__ for casting to a str
strtype     int___str__fn(inttype self);
#endif
