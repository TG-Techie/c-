#include <stdio.h>
#include <stdbool.h>
int main () {

    while (true){
        char buff[1];
        scanf("%s", buff);
        printf("%s\n", buff);
    }

   char str1[20];

   printf("Enter name: ");
   scanf("%s", str1);

   char str2[30];
   printf("Enter your website name: ");
   scanf("%s", str2);

   printf("Entered Name: %s\n", str1);
   printf("Entered Website: %s", str2);

   printf("\n");
   return(0);
}
