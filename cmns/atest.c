#include "langbase.h"
#include "file.h"

int main(){
    /*printf("1: %d\n", truelitrl);
    printf("2: %d\n", truelitrl->base);
    printf("3: %d\n", truelitrl->base->type);
    printf("4: %d\n", truelitrl->base->type->free);*/
    truelitrl->base->type->free((anytype) truelitrl);
    refto(truelitrl);
    _cmns_gc();
    //_noneclass_struct.free(newany());
    //void (*free)(anytype) = nonelitrl->base->type->free;//->free((anytype)nonelitrl);
    //printf("done litrl:%d  bool->value: %d\n", falselitrl, truelitrl->value);
}
