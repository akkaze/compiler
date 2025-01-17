
int N = 15000;
bool[] b = new bool[15001];
int resultCount = 0;

int main()
{
  int i;

  for (i = 1; i <= N; i++) b[i] = true;

  for (i = 2; i <= N; i++) if (b[i])
  {
    int count = 2;
    
    if (i>3 && b[i-2])
    {
      resultCount++;
      println(toString(i-2) + " " + toString(i));
    }
    
    while (i*count <= N)
    {
      b[i*count] = false;
      count++;
    }
  }

  println("Total: " + toString(resultCount));
  return 0;
}
