#include "cmns/langbase.h"

nonetype block_align_testfn(){
    /*no arguments passed*/
    /*line 1: assign 'x'*/
    /*first assignment of 'x' in scope*/
    inttype x_var = refto(intlitrl(5));
    /*return routine*/
    /*automatically returning none*/
    /*return type validated at compile time*/
    _cmns_gc();
    refreturn(nonelitrl);
}

booltype the_questionfn(strtype prompt_var){
    /*argument refs to preclude gc*/
    refto(prompt_var);
    /*line 4: assign 'rootvar'*/
    /*first assignment of 'rootvar' in scope*/
    inttype rootvar_var = refto(intlitrl(1));
    if ((str___eq__fn(prompt_var, strlitrl("blue")))->value){
        /*line 6: assign 'bluevar'*/
        /*first assignment of 'bluevar' in scope*/
        inttype bluevar_var = refto(intlitrl(2));
        /*return routine*/
        anytype retval = refto(truelitrl);
        /*return type validated at compile time*/
        deref(bluevar_var);
        deref(rootvar_var);
        deref(prompt_var);
        _cmns_gc();
        refreturn(retval);
    } else if ((str___eq__fn(prompt_var, strlitrl("\")))->value){
        /*line 9: assign 'redvar'*/
        /*first assignment of 'redvar' in scope*/
        inttype redvar_var = refto(intlitrl(3));
        /*return routine*/
        anytype retval = refto(truelitrl);
        /*return type validated at compile time*/
        deref(redvar_var);
        deref(rootvar_var);
        deref(prompt_var);
        _cmns_gc();
        refreturn(retval);
    } else {
        /*pass*/
    }
    /*return routine*/
    anytype retval = refto(falselitrl);
    /*return type validated at compile time*/
    deref(rootvar_var);
    deref(prompt_var);
    _cmns_gc();
    refreturn(retval);
}

nonetype mainfn(){
    /*no arguments passed*/
    /*line 16: assign 'answer'*/
    /*first assignment of 'answer' in scope*/
    inttype answer_var = refto(intlitrl(5));
    /*return routine*/
    /*automatically returning none*/
    /*return type validated at compile time*/
    _cmns_gc();
    refreturn(nonelitrl);
}

