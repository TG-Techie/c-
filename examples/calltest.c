#include "cmnsbase.c"

inttype combsintsfn(inttype a_var, inttype b_var){
    // args get refs
    refto(a_var);
    refto(b_var);

    inttype c_var = refto(intlitrl(5));

    inttype out_var = refto(int__addfn(int__addfn(a_var, b_var), c_var));

    // return routine
    deref(a_var);
    deref(b_var);
    deref(c_var);
    _cmns_gc();
    refreturn(out_var);
}

void mainfn(){
    inttype a_var = refto(intlitrl(100));

    inttype c_var = refto(combsintsfn(a_var, intlitrl(9999)));

    printfn(int__tostr(c_var));
    //return routine
    deref(c_var);
    deref(a_var);

    _cmns_gc();
    return;

}
