int main() {
  int a = 10000;
  int b = 0;
  int c = 2800;
  int d = 0;
  int e = 0;
  int[] f = new int[2801];
  int g = 0;

  for (; b - c != 0;)
    f[b++] = a / 5;
  for (;; e = d % a) {
    d = 0;
    g = c * 2;
    if (g == 0)
      break;

    for (b = c;; d = d * b) {
      d = d + f[b] * a;
      g = g - 1;
      f[b] = d % g;
      d = d / g--;
      b = b - 1;
      if (b == 0)
        break;
    }

    c = c - 14;
    print(toString(e + d / a));
  }

  println("");
  return 0;
}
