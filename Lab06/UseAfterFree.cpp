int main() {
  int *array = new int[10];
  delete [] array;
  return array[0];
}