#include "cmns/langbase.h"

nonetype mainfn(){
    /*no arguments passed*/
    /*line 2: assign 'x'*/
    /*first assignment of 'x' in scope*/
    strtype x_var = refto(strlitrl("5"));
    if ((str___eq__fn(x_var, strlitrl("5")))->value){
        if ((truelitrl)->value){
            /*return routine*/
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
        /*pass*/
    }
    /*return routine*/
    /*automatically returning none*/
    /*return type validated at compile time*/
    _cmns_gc();
    refreturn(nonelitrl);
}

