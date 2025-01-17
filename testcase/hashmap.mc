int hashsize = 100;
class node {
	int key;
    int data;
	node next;
}
node[] table;
int getHash(int n) {
	return (n * 237) % hashsize;
}
void put(int key, int data) {
	int p;
	node ptr = null;
	p = getHash(key);
	if (table[p] == null) {
		table[p] = new node;
		table[p].key = key;
		table[p].data = data;
		table[p].next = null;
		return;
	}
	ptr = table[p];
	while (ptr.key != key) {
		if (ptr.next == null) {
			ptr.next = new node;
			ptr.next.key = key;
			ptr.next.next = null;
		}
		ptr = ptr.next;
	}
	ptr.data = data;
}
int get(int key) {
	node ptr = null;
	ptr = table[getHash(key)];
	while (ptr.key != key) {
		ptr = ptr.next;
	}
	return ptr.data;
}
int main() {
	int i;
	table = new node[100];
	for (i = 0;i < hashsize;i++)
		table[i] = null;
	for (i = 0;i < 1000;i++)
		put(i, i);
	for (i = 0;i < 1000;i++)
		println(toString(i) + " " + toString(get(i)));
	return 0;
}
