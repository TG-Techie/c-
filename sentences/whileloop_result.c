#include "cmns/file.h"

nonetype mainfn(){
    /*no arguments passed*/
    /*line 3: assign 'x'*/
    /*first assignment of 'x' in scope*/
    inttype x_var = refto(intlitrl(1));
    /*line 4: while*/
    while ((truelitrl)->value){
        /*line 5: conditional branch*/
        if ((int___lessthan__fn(x_var, intlitrl(10)))->value){
            /*line 6: assign 'x'*/
            rerefto(x_var, int___add__fn(x_var, intlitrl(1)));
            /*line 7: continue*/
            continue;
        } else {
            /*line 8: break*/
            break;
        }
    }
    /*implicit 'nonetype' return routine at end of function 'main'*/
    deref(x_var);
    _cmns_gc();
    refreturn(nonelitrl);
}

