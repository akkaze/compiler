class MemberTester {
    MemberTester next1;
    int x;
    int y;
    MemberTester next2;
}

void testMember(int n) {
    MemberTester root = new MemberTester;
    MemberTester now = root;
    int i;
    for (i = 0; i < n; i++) {
        now.next2 = new MemberTester;
        now = now.next2;
    }

    root.next2.next2.next2.next2.next2.next2.x = 197;
    root.next2.next2.next2.x = 297;

    println("test member: " + toString(root.next2.next2.next2.x + root.next2.next2.next2.next2.next2.next2.x));
}

int main() {
    testMember(10);

    return 0;
}

