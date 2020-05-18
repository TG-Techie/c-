
#include "langbase.c" // this contains the struct definitions, etc
#include "types/strtype.c"
/* for reference:

typedef struct str_struct_type{
    cmnsbase base;
    uint length; // length of the char array stored for ease
    char* values; // the char array location
}* strtype;

all objects in c- are heap allocated structs that share have
a cmns base struct as the first member.

the base contains a reference count and a pointer to a class struct

rn, class structs just have pointer to a function that frees
that specific type so the garbase collector doesn't need ot keep
track of type at runtime.

these can be seen in langbase.h and strtype.c
*/

void str_construct(strtype inst, char* values){
    // constructor for the strtype

    // find the length of the str to duplicate it
    int length = strlen(values) + 1;

    //reserve a place in the heap to store the char[]
    char * arr = (char*)malloc(length);

    // copy the contents of the desired string into the heap
    strcpy(arr, values);

    //set the pointer in teh struct equal to the arr location
    inst->values = arr;
}

int main(){
    //an example code to make a c- string (excluding the obj base)
    // every object in c- is a struct

    //here we instantiate a struct and assign its pointers
    // to the local variable inst, an instance of a string
    strtype inst = malloc(sizeof(str_struct_type));

    //skip makeing a cmns base,

    //pass inst to its constructor with the desired contents
    str_construct(inst, "the desired contents");

    //try to print the contents which should now be in values
    printf("%s\n", inst->values);
}
