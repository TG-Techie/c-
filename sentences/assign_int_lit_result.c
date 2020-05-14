#include "cmns/langbase.h"

/*line 1: assign 'foo'*/
/*first assignment of 'foo' in scope*/
inttype foo_var = refto(intlitrl(5));

/*line 2: assign 'foo'*/
rerefto(foo_var, intlitrl(7));

/*line 3: assign 'foo'*/
/*casting 'foo' from type 'int' to  type 'str'*/
rerefto(foo_var, strlitrl("teststr"));

