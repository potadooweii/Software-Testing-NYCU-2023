int main() {
  int *array = new int[10];
  array[0] = 0;
  int boom = array[20];  // BOOM
  delete [] array;
  return 0;
}