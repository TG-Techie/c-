#include "cmns/langbase.h"

inttype addintsfn(inttype a_var, inttype b_var){
    /*argument refs to preclude gc*/
    refto(a_var);
    refto(b_var);
    /*return routine*/
    anytype retval = refto(int___add__fn(a_var, b_var));
    /*return type validated at compile time*/
    deref(a_var);
    deref(b_var);
    _cmns_gc();
    refreturn(retval);
}

strtype addstrfn(strtype a_var, strtype b_var){
    /*argument refs to preclude gc*/
    refto(a_var);
    refto(b_var);
    /*line 5: assign 'baz'*/
    /*first assignment of 'baz' in scope*/
    inttype baz_var = refto(intlitrl(0));
    /*line 6: assign 'baz'*/
    /*casting 'baz' from type 'int' to  type 'str'*/
    rerefto(baz_var, strlitrl("baz"));
    /*return routine*/
    anytype retval = refto(str___add__fn(a_var, str___add__fn(b_var, baz_var)));
    /*return type validated at compile time*/
    deref(baz_var);
    deref(a_var);
    deref(b_var);
    _cmns_gc();
    refreturn(retval);
}

