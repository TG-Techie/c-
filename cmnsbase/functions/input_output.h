#include "../langbase.h"
#include "../types/alltypes.h"

#ifndef cmns_input_output_define
    #define cmns_input_output_define

    #define _io_buffer_chunk_size 30

    nonetype printfn(strtype string);

    strtype inputfn(strtype prompt);
#endif
