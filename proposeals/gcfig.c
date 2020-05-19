#include <stdio.h>

#define len 7

void print(int *vars){
    printf("[%d", vars[0]);
    for (int i=1; i<len; i++){
        printf(", %d", vars[i]);
    }
    printf("]\n");
}

int main(){
    int vars[len] = {1, 2, 0, 0, 3, 0, 4};

    print(vars);

    int moveback = 0;
    for (int i=0; i<len; i++){
        if (vars[i] > 0){
            vars[i - moveback] = vars[i];
            if (moveback > 1) {
                vars[i] = 0;
            }
        } else {
            moveback += 1;
        }
    }

    print(vars);
}
