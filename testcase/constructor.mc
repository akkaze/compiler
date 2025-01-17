int counter = 0;
class ConstructorTester {
    int ct;
    ConstructorTester() {
        ct = counter++;
        println("Constructed - " + toString(this.ct));
    }
}
void testConstructor() {
    ConstructorTester a = new ConstructorTester;
    ConstructorTester[] b = new ConstructorTester[5];
    ConstructorTester[][] c = new ConstructorTester[4][4];
    ConstructorTester[][][] d = new ConstructorTester[3][3][3];
    ConstructorTester[][][][] e = new ConstructorTester[2][2][2][];

    int i; int j; int k;
    for (i = 0; i < e.size(); i++) {
        for (j = 0; j < e[i].size(); j++) {
            for (k = 0; k < e[j].size(); k++) {
                e[i][j][k] = new ConstructorTester[1];
            }
        }
    }
}

int main() {
    testConstructor();


    return 0;
}
