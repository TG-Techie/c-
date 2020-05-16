#include "nonetype.h"

//since none is a sington of nonetype it shoudl not be collected
void freenone(nonetype self){
    return;
}

const cmnsclass noneclass = &((struct cmns_struct_class){&freenone});

const nonetype nonelitrl = &( (struct none_struct_type){
    &( (struct cmns_struct_base){0, 0, noneclass} )
});

//other implementations:
//struct cmns_struct_class _noneclass_struct = {&freenone,};
//const cmnsclass noneclass = &_noneclass_struct;

/*
struct cmns_struct_base _nonebase_struct = {0, 0, noneclass};
struct none_struct_type _nonelitrl_struct = {&_nonebase_struct};
const nonetype nonelitrl = &_nonelitrl_struct;
*/

/*
struct none_struct_type _nonelitrl_struct = {
    &( (struct cmns_struct_base){0, 0, noneclass} )
};
const nonetype nonelitrl = &_nonelitrl_struct;
*/
