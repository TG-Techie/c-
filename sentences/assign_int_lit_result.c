#include "cmns/file.h"

nonetype mainfn(){
    /*no arguments passed*/
    /*line 2: assign 'foo'*/
    /*first assignment of 'foo' in scope*/
    inttype foo_var = refto(intlitrl(5));
    /*line 3: assign 'foo'*/
    rerefto(foo_var, intlitrl(7));
    /*line 4: assign 'foo'*/
    /*casting 'foo' from type 'int' to  type 'str'*/
    rerefto(foo_var, strlitrl("teststr"));
    /*implicit 'nonetype' return routine at end of function 'main'*/
    _cmns_gc();
    refreturn(nonelitrl);
}

