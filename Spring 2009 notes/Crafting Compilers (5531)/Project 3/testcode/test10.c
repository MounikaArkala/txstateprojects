/* scoping rules : global variable (should pass) */
int i;

int foo() {
  i = 17;
  return 0;
}
