/* 
this contains unterminated comments
and variable redeclarations in various scopes. */



int func()
{
    int i;
    i = 5;
    return 1;
}


int foo[6];
char foo;
int foo;
int main(int j, int k, int foo)
{
    char c;
    int j;
    j = 0;
    if (j < 0)
    {
        j = 256 - min(abs(j), 256);
    }
    else
    {
        j = 0;
    }
    
    while (j < 256)
    {
            j = j + 1;
            c = itoa(j);
            putch(c);
    }
    return j;
}
int foo[24];

int jeff()
{
    int b;
    string jdawg;
    jdawg = "Jeff!;
    printf(jdawg);
    return;
    /* some random comment."*/
}
string foo;
/* unterminated comment