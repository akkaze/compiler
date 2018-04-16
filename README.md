# compiler
A toy compiler for a syntax subset of c++ written in python  
requires python3, antlr4, antlr4-python3-runtime  
in the follwing instructions, you may replace python3 with python and pip3 with pip in your enviroment  
To install antlr4-python3-runtime, run **pip3 install antlr4-python3-runtime==4.6** 
## install
>For installing, run *python3 setup.py install*
## run a demo  
>* First, make a new file, write some codes (like the follwing) in it, name it test.c
```c++
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
>* Then, run *python3 -m compiler -in test.c -out out.asm* 
>* At last, run *cat out.asm*, you may see the follwing assembly codes
