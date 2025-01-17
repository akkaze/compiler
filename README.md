# compiler
A toy compiler for a syntax subset of c++ written in python  
requires python3, antlr4, antlr4-python3-runtime  
in the follwing instructions, you may replace python3 with python and pip3 with pip in your enviroment  
To install antlr4-python3-runtime, 
>* run **pip3 install antlr4-python3-runtime==4.6** 
## install
>* For installing, run **python3 setup.py install**
>* For users don't want to run without installing, run **export PYTHONPATH='dir where the __main__.py file is included'**
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
>* Then, run **python3 -m compiler -in test.c -out out.asm** 
>* At last, run **cat out.asm**, you may see the follwing assembly codes, which is in the nasm format
>* In order to run and debug this asm code, yo may install nasm, ld(which is integrated in the gcc)
>* On the unbuntu system, just run **sudo apt install nasm**
>* To build this asm code, run **nasm -f elf64 out.asm -o out.o**
>* Then,link it using ld or gcc, run **ld -m elf_x86_64 out.o -o out -lc -I /lib64/ld-linux-x86-64.so.2**

>* Or just use asm.bash with the first argument as the asm file, run **./asm.bash out**
```c++
        global main
        section .data

        section .text
        ALIGN 16
sum__func__:

sum_begin0:
        mov rax, 0
        mov rsi, 0
loop_test2:
        cmp rsi, rdi
        jge loop_end3
loop_begin1:
        add rsi, 1
        jmp loop_test2
loop_end3:
sum_end4:
        ret

        ALIGN 16
main:
        sub rsp, 8

main_begin5:
        call A_foo__func__
        mov rdi, 10
        call sum__func__
        mov rax, 0
main_end6:
        add rsp, 8
        ret

        ALIGN 16
A_foo__func__:

foo_begin7:
        mov rsi, qword [rdi]
        cmp rsi, 0
        jge if_else9
if_then8:
        mov rax, qword [rdi]
        mov rsi, rax
        add rsi, 1
        mov qword [rdi], rsi
foo_end11:
        ret
if_else9:
        mov rax, qword [rdi]
        mov rsi, rax
        sub rsi, 1
        mov qword [rdi], rsi
        jmp foo_end11
```
