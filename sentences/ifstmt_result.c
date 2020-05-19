#include "cmns/file.h"

nonetype block_align_testfn(){
    /*no arguments passed*/
    /*line 1: assign 'x'*/
    /*first assignment of 'x' in scope*/
    inttype x_var = refto(intlitrl(5));
    /*implicit 'nonetype' return routine at end of function 'block_align_test'*/
    deref(x_var);
    _cmns_gc();
    refreturn(nonelitrl);
}

booltype the_questionfn(strtype prompt_var){
    /*argument refs to preclude gc*/
    refto(prompt_var);
    /*line 4: assign 'rootvar'*/
    /*first assignment of 'rootvar' in scope*/
    inttype rootvar_var = refto(intlitrl(1));
    /*line 5: conditional branch*/
    if ((str___eqls__fn(prompt_var, strlitrl("blue")))->value){
        /*line 6: assign 'bluevar'*/
        /*first assignment of 'bluevar' in scope*/
        inttype bluevar_var = refto(intlitrl(2));
        /*line 7: return routine,  type 'bool'*/
        booltype retval = refto(truelitrl);
        /*return type validated at compile time*/
        deref(bluevar_var);
        deref(rootvar_var);
        deref(prompt_var);
        _cmns_gc();
        refreturn(retval);
    } else if ((str___eqls__fn(prompt_var, strlitrl("red")))->value){
        /*line 9: assign 'redvar'*/
        /*first assignment of 'redvar' in scope*/
        inttype redvar_var = refto(intlitrl(3));
        /*line 10: assign 'redvar'*/
        /*casting 'redvar' from type 'int' to  type 'str'*/
        rerefto(redvar_var, strlitrl("3"));
        /*line 11: return routine,  type 'bool'*/
        booltype retval = refto(truelitrl);
        /*return type validated at compile time*/
        deref(redvar_var);
        deref(rootvar_var);
        deref(prompt_var);
        _cmns_gc();
        refreturn(retval);
    } else {
        /*line 12: pass*/
    }
    /*line 14: return routine,  type 'bool'*/
    booltype retval = refto(falselitrl);
    /*return type validated at compile time*/
    deref(rootvar_var);
    deref(prompt_var);
    _cmns_gc();
    refreturn(retval);
}

nonetype mainfn(){
    /*no arguments passed*/
    /*line 17: assign 'answer'*/
    /*first assignment of 'answer' in scope*/
    inttype answer_var = refto(intlitrl(5));
    /*implicit 'nonetype' return routine at end of function 'main'*/
    deref(answer_var);
    _cmns_gc();
    refreturn(nonelitrl);
}

