#include "cmns/file.h"

nonetype mainfn(){
    /*no arguments passed*/
    /*line 2: assign 'x'*/
    /*first assignment of 'x' in scope*/
    strtype x_var = refto(strlitrl("5"));
    /*line 3: conditional branch*/
    if ((str___eqls__fn(x_var, strlitrl("5")))->value){
        /*line 4: conditional branch*/
        if ((truelitrl)->value){
            /*line 5: return routine,  type 'nonetype'*/
            anytype retval = refto(nonelitrl);
            /*return type validated at compile time*/
            deref(x_var);
            _cmns_gc();
            refreturn(retval);
        } else {
            /*line 7: assign 'x'*/
            rerefto(x_var, strlitrl("56"));
        }
    } else {
        /*line 9: pass*/
    }
    /*implicit 'nonetype' return routine at end of function 'main'*/
    _cmns_gc();
    refreturn(nonelitrl);
}

