#include "typebase.h"

void freeany(anytype self){
    free(self->base);
    free(self);
}

cmnsclass anyclass = &((cmnsclass){&freeany});

void constructany(anytype self){
}

anytype newany(){
    cmnsbase base = malloc(sizeof(cmnsbase));
    base->refs = 0;
    base->type = anyclass;
    anytype inst = malloc(sizeof(anytype));
    inst->base = base;
    constructany(inst);
    _cmns_record_var_as_alloced(inst);
    return inst;
}


// gc
anytype _cmns_referenceto(anytype inst){
    inst->base->refs += 1;
    return inst;
}

void _cmns_free(anytype inst){
    //printf("freeing: %d\n", inst);
    _cmns_alloced_vars[inst->base->var_index] = NULL;
    inst->base->refs = 0;
    (inst->base->type->free)(inst);
}

void _cmns_dbg_print_vars(){
    printf("allocated_vars: ");
    for (int i=0; i<_cmns_max_vars; i++){
        if (_cmns_alloced_vars[i]){
            printf("%d, ", _cmns_alloced_vars[i]->base->refs);
        }
    }
    printf("\n");
}

void _cmns_record_var_as_alloced(anytype newvar){
    _cmns_alloced_vars[_cmns_next_alloced_var_index] = newvar;
    newvar->base->var_index = _cmns_next_alloced_var_index;
    _cmns_next_alloced_var_index += 1;
    //printf("%d\n", newvar);
}

void _cmns_gc(){
    int moveback = 0;
    //loopvars
    int refs;
    anytype var;
    //_cmns_print_vars();
    for (int i=0; i<_cmns_max_vars; i++){
        var = _cmns_alloced_vars[i];
        //printf("%d: (%d)\n", i, var);
        if (var){
            refs = var->base->refs;
            if (refs == 0){
                //printf("%d ", i);
                _cmns_free(var);
                //_cmns_alloced_vars[i] = NULL;
                moveback += 1;
            } else if (moveback > 1) {
                _cmns_alloced_vars[i-moveback] = var;
                var->base->var_index = i-moveback;
                _cmns_alloced_vars[i] = NULL;
            }
        }
    }
    _cmns_next_alloced_var_index -= moveback;
    return;
}

void _cmns_dereference_var(anytype inst){
    if (inst){ // make tolerable to NULL pointers
        inst->base->refs -= 1;
        if (inst->base->refs == 0){
            //free the inst if there are no other references to it
            _cmns_free(inst);
        }
    } else {
        printf("NULL pointer passed to '_cmns_dereference_var' function!");
    }
}

void dereference_no_gc(anytype inst){
    if (inst){
        inst->base->refs -= 1;
    }
}
