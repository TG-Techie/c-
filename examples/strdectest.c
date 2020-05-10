#include "cmnsbase.c"

/*2: main funcdef*/
void mainfn(){
    /*3: a=""*/
    strtype a;
    a = refto(strlitrl(""));
    /*4: a = "it's not pining"*/
    deref(a);
    a = strlitrl("it's not pining, ");
    /*4:  b = "it's passed on!"*/
    strtype b;
    b = refto(strlitrl("it's passed on!"));
    /*5:  c = a.add(b)*/
    strtype c;
    c = refto(str__addfn(a, b));
    /*6: print(c)*/
    printfn(c);

    //return routine
    deref(c);
    deref(b);
    deref(a);

    _cmns_gc();
    return;
}
