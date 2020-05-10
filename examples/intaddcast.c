#include "cmnsbase.c"

void mainfn(){
    /*3: x = 100*/
    inttype x = NULL;
    rerefto(x, intlitrl(100));
    /*4: y = 9999*/
    inttype y = NULL;
    rerefto(y, intlitrl(9999));
    /*6: z = x._add(y)*/
    inttype z = NULL;
    rerefto(z, int__addfn(x, y));
    /*7: print(z._tostr())*/
    printfn(str__addfn(strlitrl("x + y = "), int__tostr(z)));
    //printf("%d\n", 999/100);
    /*18: implicit: FIXME: alloc? deallloc?*/
    //printfn(int__tostr(intlitrl(_next_alloced_var_index)));



    //dereference(z);
    //z = referenceto(intlitrl(5));
    rerefto(z, intlitrl(5));

    printfn(str__addfn(strlitrl("new z is: "), int__tostr(z)));

    deref(z);
    deref(y);
    deref(x);

    _cmns_gc();
    return;
}
