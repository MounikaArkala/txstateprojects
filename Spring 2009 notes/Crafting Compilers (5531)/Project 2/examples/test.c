ifasds /* this probably isn't valid in the grammar but it's fine for the parser. */

int main()
{
   int a = 4, b = 5;
   while (1)
   {
       /* this should result in Hello, "world!" */
       printf("Hello, \"world!\"");
       /* this is a
       multiline comment.*/
       if (a > b)
       {
            printf("A is greater!\n");
       }
       else
       {
           printf("B is greater!\t");
       }
       
       printf("The world is \\");
       /* This should have an error (unterminated string constant) */
       string a = " some string
       "; /*this one will likely error out as well. */
       
       string foo = "blahblah\";  /* this should have an error as well.*/
       
       string foo2 = "blah\blah"; /* shoudl be an unrecognized sequence. */
       
       /* this is a character literal */
       char a = 'a';
       char b = 'booobalooo'; /* this is an invalid character literal. */
  
       /* and finally an unterminated comment.

   }
}