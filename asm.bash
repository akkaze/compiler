nasm -felf64 $1.asm && gcc $1.o -lc -static && ./a.out
