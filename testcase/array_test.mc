int[] a = new int[4];
int main()
{
    int[][] b = new int[4][];
	int i;
	b[0] = a;
	b[1] = a;
	b[2] = a;
	b[3] = a;
	println(toString(b.size()));
	for (i = 0; i < b[0].size(); i++)
		b[0][i] = getInt();
	for (i = 0; i < b[1].size(); i++)
		print(toString(b[1][i]));
	println("");
	for (i = 0; i < b[2].size(); i++)
		b[2][i] = 0;
	for (i = 0; i < b[3].size(); i++)
		print(toString(b[3][i]));
}
