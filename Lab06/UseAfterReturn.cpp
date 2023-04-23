int *ptr;

void func() {
  int local[10];
  ptr = &local[0];
}

int main(int argc, char **argv) {
  func();
  return *ptr;
}
