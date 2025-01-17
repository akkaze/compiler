class point {
	int x;
	int y;
	int z;
	point() {
		x = 0;
		y = 0;
		z = 0;
	}
	void set(int a_x, int a_y, int a_z){
		x = a_x;
		y = a_y;
		z = a_z;
	}
	int sqrLen(){
		return x * x + y * y + z * z;
	}
	int sqrDis(point other) {
		return (x - other.x) * (x - other.x) + (y - other.y) * (y - other.y) + (z - other.z) * (z - other.z);
	}
	int dot(point other) {
		return x * other.x + y * other.y + z * other.z;
	}
	point cross(point other) {
		point retval = new point;
		retval.set(y * other.z - z * other.y, z * other.x - x * other.z, x * other.y - y * other.x);
		return retval;
	}
	point add(point other) {
		x = x + other.x;
		y = y + other.y;
		z = z + other.z;
		return this;
	}
	point sub(point other) {
		x = x - other.x;
		y = y - other.y;
		z = z - other.z;
		return this;
	}
	void printPoint() {
		println("(" + toString(x) + ", " + toString(y) + ", " + toString(z) + ")");
	}
}

int main() {
	point a = new point;
	point b = new point;
	point c = new point;
	point d = new point;
	a.printPoint();
	a.set(849, -463, 480);
	b.set(-208, 585, -150);
	c.set(360, -670, -742);
	d.set(-29, -591, -960);
	a.add(b);
	b.add(c);
	d.add(c);
	c.sub(a);
	b.sub(d);
	d.sub(c);
	c.add(b);
	a.add(b);
	b.add(b);
	c.add(c);
	a.sub(d);
	a.add(b);
	b.sub(c);
	println(toString(a.sqrLen()));
	println(toString(b.sqrLen()));
	println(toString(b.sqrDis(c)));
	println(toString(d.sqrDis(a)));
	println(toString(c.dot(a)));
	b.cross(d).printPoint();
	a.printPoint();
	b.printPoint();
	c.printPoint();
	d.printPoint();
}
