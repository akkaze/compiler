class Person {
  Person() { name = ""; }
  string name;
  int age;
}

int init_age = 10;
int work_age = 20;
void work(string st, Person p) {
  string a = st + ", " + p.name + " enjoys this work. XD";
  if (p.age <= 10)
    println(st + ", " + p.name + " enjoys this work. XD");
  else
    println(st + ", " + p.name + " wants to give up!!!!!");
  p.age = p.age + work_age;
}
int main() {
  Person mr;
  Person mars;
  mr = new Person;
  mr.name = "the leading Person" + mr.name;
  mr.age = 0;
  mars = new Person;
  mars.name = "the striking Person";
  mars.age = init_age;
  work("MR", mr);
  work("Mars", mars);
  work("Mars", mars);
  return 0;
}
