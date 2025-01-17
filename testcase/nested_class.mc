class A {
  int a;
  int b;
}

class B {
  B() { a = new A; }
  A a;
  int b;
}

int main() {
  B b = new B;
  b.a.b = 1;
  println(toString(b.a.b));
  return 0;
}
