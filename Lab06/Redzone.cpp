int main() {
  int a[8] = {0};
  int b[8] = {0};
//   int res = a[8];  // BOOM
  int res = a[16];  // SAFE
  return 0;
}