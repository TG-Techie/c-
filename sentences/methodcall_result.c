#include "cmns/file.h"

inttype addintsfn(inttype a_var, inttype b_var){
    /*argument refs to preclude gc*/
    refto(a_var);
    refto(b_var);
    /*line 4: return routine,  type 'int'*/
    inttype retval = refto(int___add__fn(a_var, b_var));
    /*return type validated at compile time*/
    deref(a_var);
    deref(b_var);
    _cmns_gc();
    refreturn(retval);
}

inttype retintfn(){
    /*no arguments passed*/
    /*line 7: assign 'a'*/
    /*first assignment of 'a' in scope*/
    inttype a_var = refto(intlitrl(100));
    /*line 8: return routine,  type 'int'*/
    inttype retval = refto(addintsfn(a_var, intlitrl(9999)));
    /*return type validated at compile time*/
    deref(a_var);
    _cmns_gc();
    refreturn(retval);
}

