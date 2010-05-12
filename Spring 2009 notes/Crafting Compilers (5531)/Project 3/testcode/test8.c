/* function signature mismatch - mistyped actual parameter : line 8 */
int foo(int i) {
  return 0;
}

int bar() {
  char c;
  foo(c);
}

