// Target: Spill the variables from the register allocation when there are too many of them.
// Possible optimization: Inline function
// REMARKS: Pay attention to the size of the stack(heap).


int[] count;

int getcount(int[] count) {
    return ++count[0];
}

int main() {
    int v0;
    int v1;
    int v2;
    int v3;
    int v4;
    int v5;
    int v6;
    int v7;
    count = new int[1];
    count[0] = 0;
    v0 = getcount(count);
    v1 = getcount(count);
    v2 = getcount(count);
    v3 = getcount(count);
    v4 = getcount(count);
    v5 = getcount(count);
    v6 = getcount(count);
    v7 = getcount(count);
    print(toString(v0) + " ");
    print(toString(v1) + " ");
    print(toString(v2) + " ");
    print(toString(v3) + " ");
    print(toString(v4) + " ");
    print(toString(v5) + " ");
    print(toString(v6) + " ");
    print(toString(v7) + " ");
    println("");
    return 0;
}

