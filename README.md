# compiler
A toy compiler for subset of c++ written in python  
requires python3, antlr4, anlr4-python3-runtime
## install
>For installing, run python3 setup.py install
## run a demo  
>* First, make a new file, write some codes (like the follwing) in it, name it test.c
```c++
@requires_authorization
class A {
  int foo() {
    if (a < 0) {
      return a++;
    }
    else {
      return a--;
    }
  }
  int a;
}
int sum(int i) {
    int s = 0;
    int j;
    for (j = 0; j < i; j++) {
      s += j;
    }
    return s;
}
int main() {
  A a;
  a.foo();
  int s = sum(10);
  return 0;
}
```  
>* Then, run python3 -m compiler -in test.c -out out.asm 
