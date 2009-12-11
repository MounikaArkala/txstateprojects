
#include "unp.h"
#include <stdlib.h>
#include <stdio.h>
int main (int argc, char **argv)
{
    union
    {
        int s;
        char c[sizeof(int)];
    } un;
    
    un.s = 0x01020304;
    if (sizeof(int) == 4)
    {
        if (un.c[0] == 1 && un.c[1] == 2 && un.c[2] == 3 && un.c[3] == 4 )
        {
            printf("big-endian\n");
        }
        else if(un.c[0] == 4 && un.c[1] == 3 && un.c[2] == 2 && un.c[3] == 1)
        {
            printf("little-endian\n");
        }
        else
        {
            printf("unknown\n");
        }
    }
    else
    {
        printf("sizeof(short) = %d\n", sizeof(short));
    }
    exit(0);
}
