int main()
{
	int a;
	int b;
	int c;
	int d;
	int e;
	int f;
	int g;
	int n = getInt();
  int ans = 0;
	for(a = 0; a < n; ++a)
		for(b = 0; b < n; ++b)
			for(c = 0; c < n; ++c)
				for(d = 0; d < n; ++d)
					for(e = 0; e < n; ++e)
						for(f = 0; f < n; ++f)
							for(g = 0; g < n; ++g)
							{
								bool t1 = (((a == b) && c > 0) || (d == e && f > 0 && g > 0) || (a == g) || (d > 0 && f > 0));
								bool t2 = (((a == b) && c > 0) || (d == e && f > 0 && g > 0) || (a == g) || (d > 0 && f > 0));
								bool t3 = (((a == b) && c > 0) || (d == e && f > 0 && g > 0) || (a == g) || (d > 0 && f > 0));
								bool t4 = (((a == b) && c > 0) || (d == e && f > 0 && g > 0) || (a == g) || (d > 0 && f > 0));
								bool t5 = (((a == b) && c > 0) || (d == e && f > 0 && g > 0) || (a == g) || (d > 0 && f > 0));
								bool t6 = (((a == b) && c > 0) || (d == e && f > 0 && g > 0) || (a == g) || (d > 0 && f > 0));
								if(t1)
									ans++;
								if(t2)
									ans++;
								if(t3)
									ans++;
								if(t4)
									ans++;
								if(t5)
									ans++;
								if(t6)
									ans++;
							}
	print(toString(ans));
	return 0;
}

