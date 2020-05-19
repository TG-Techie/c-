#include "input_output.h"

nonetype printfn(strtype string){
    printf("%s\n", (string->values));
    return nonelitrl;
}

strtype inputfn(strtype prompt){
    printf("%s", prompt->values);

    uint capactity = _io_buffer_chunk_size; // the max length of the current string
    char * buf = malloc(capactity + 1);

    uint next_index = 0; // the length of the currently buffered string
    char cur_char;
    while (true){
        cur_char = getchar();

        // a newline ends the input function
        if (cur_char == '\n') {
            cur_char = 0;
        }

        // if the buffer is full realloc (may be leaving some little space)
        if ((next_index + 1) == capactity){
            capactity += _io_buffer_chunk_size;
            buf = realloc(buf, capactity + 1);
        }

        // store the input character and set to write into the next char
        buf[next_index] = cur_char;
        next_index += 1;

        // if done stop
        if (cur_char == 0){
            break;
        }
    }

    // make the new str and free the buffer
    strtype ret = newstr(buf);
    free(buf);

    return ret;
}
