#include "nonetype.h"

//since none is a sington of nonetype it shoudl not be collected
void freenone(nonetype self){
    return;
}

const cmnsclass noneclass = &((struct cmns_struct_class){&freenone});

struct cmns_struct_base _nonebase_struct = {0, 0, noneclass};
struct none_struct_type _nonelitrl_struct = {&_nonebase_struct};
const nonetype nonelitrl = &_nonelitrl_struct;
