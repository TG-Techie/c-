#include "cmns/file.h"

nonetype mainfn(){
    /*no arguments passed*/
    /*line 3: assign 'strin'*/
    /*first assignment of 'strin' in scope*/
    strtype strin_var = refto(inputfn(strlitrl("input your name")));
    /*line 4: expression as statement*/
    printfn(strlitrl("your name is:"));
    /*line 5: expression as statement*/
    printfn(strin_var);
    /*implicit 'nonetype' return routine at end of function 'main'*/
    deref(strin_var);
    _cmns_gc();
    refreturn(nonelitrl);
}

