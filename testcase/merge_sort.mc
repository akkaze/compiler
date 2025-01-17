int[] b;

void sort(int[] a, int l, int r) {
  if (r - l == 1)
    return;
  int m = (l + r) / 2;
  sort(a, l, m);
  sort(a, m, r);
  int p = l;
  int q = m;

  int i = 0;
  while (p < m && q < r)
    if (a[p] > a[q])
      b[i++] = a[q++];
    else
      b[i++] = a[p++];
  while (p < m)
    b[i++] = a[p++];
  while (q < r)
    b[i++] = a[q++];
  for (i = l; i < r; i++)
    a[i] = b[i - l];
  return;
}
int main() {
  int n;
  int[] a;
  n = getInt();
  a = new int[n];
  b = new int[n];
  int i;
  for (i = 0; i < n; i++)
    a[i] = n - i;
  sort(a, 0, n);
  i = 0;
  for (i = 0; i < n; i++)
    println(toString(a[i]));
  return 0;
}
