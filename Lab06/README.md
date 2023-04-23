# Lab 6 - Program Security Detect  

# Report
Environment:  g++ (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0

## Part 1
* Summary Table:  
    | | Valgrind | ASan|
    |:---:|:---: |:---|
    |Heap out-of-bounds|O |O |
    |Stack out-of-bounds|X |$\Delta$ |
    |Global out-of-bounds|X |O |
    |Use-after-free|O |O |
    |Use-after-return|O |O |  

$\Delta$: sometimes can.  

### Heap out-of-bounds
```
int main() {
  int *array = new int[10];
  array[0] = 0;
  int boom = array[20];  // BOOM
  delete [] array;
  return 0;
}
```

```
// Commands
// g++ -fsanitize=address -g -o heap.o HeapOutOfBounds.cpp (O)
// g++ -fsanitize=address -O1 -g -o heap.o HeapOutOfBounds.cpp (X)
// ./heap.o

// ASan Report
=================================================================
==859==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x604000000060 at pc 0x559bb039c27f bp 0x7fff04d4c410 sp 0x7fff04d4c400
READ of size 4 at 0x604000000060 thread T0
    #0 0x559bb039c27e in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/HeapOutOfBounds.cpp:4
    #1 0x7f82ad26dd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f82ad26de3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x559bb039c124 in _start (/mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/heap.o+0x1124)

0x604000000060 is located 40 bytes to the right of 40-byte region [0x604000000010,0x604000000038)
allocated by thread T0 here:
  0x0c087fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
 ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==859==ABORTING
```

```
// Commands
// valgrind heap.o

// Valgrind Report

==737== Memcheck, a memory error detector
==737== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==737== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==737== Command: ./heap.o
==737== 
==737== Invalid read of size 4
==737==    at 0x109191: main (in /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/heap.o)
==737==  Address 0x4dd2cd0 is 32 bytes before an unallocated block of size 4,121,328 in arena "client"
==737== 
==737== 
==737== HEAP SUMMARY:
==737==     in use at exit: 0 bytes in 0 blocks
==737==   total heap usage: 2 allocs, 2 frees, 72,744 bytes allocated
==737== 
==737== All heap blocks were freed -- no leaks are possible
==737== 
==737== For lists of detected and suppressed errors, rerun with: -s
==737== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
  
### Stack out-of-bounds
```
int main() {
  int stack_array[10];
  stack_array[1] = 0;
  int boom = stack_array[15]; // BOOM
  // int boom = stack_array[20]; // ASan no report
  return 0;
}
```

```
// Commands
// g++ -fsanitize=address -g -o stack.o StackOutOfBounds.cpp (O)
// ./heap.o

// ASan Report
=================================================================
==1029==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffdef1a18c at pc 0x55aa8463135c bp 0x7fffdef1a100 sp 0x7fffdef1a0f0
READ of size 4 at 0x7fffdef1a18c thread T0
    #0 0x55aa8463135b in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/StackOutOfBounds.cpp:3
    #1 0x7f99d8702d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f99d8702e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55aa84631124 in _start (/mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/stack.o+0x1124)

Address 0x7fffdef1a18c is located in stack of thread T0 at offset 108 in frame
    #0 0x55aa846311f8 in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/StackOutOfBounds.cpp:1

  This frame has 1 object(s):
    [48, 88) 'stack_array' (line 2) <== Memory access at offset 108 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/StackOutOfBounds.cpp:3 in main
Shadow bytes around the buggy address:
  0x10007bddb3e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb3f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb410: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb420: 00 00 00 00 f1 f1 f1 f1 f1 f1 00 00 00 00 00 f3
=>0x10007bddb430: f3[f3]f3 f3 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb440: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb450: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb460: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007bddb480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1029==ABORTING
```

```
// Commands
// valgrind stack.o

// Valgrind Report

==1247== Memcheck, a memory error detector
==1247== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1247== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1247== Command: ./stack.o
==1247==
==1247== 
==1247== HEAP SUMMARY:
==1247==     in use at exit: 0 bytes in 0 blocks
==1247==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1247==
==1247== All heap blocks were freed -- no leaks are possible
==1247==
==1247== For lists of detected and suppressed errors, rerun with: -s
==1247== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
  

### Global out-of-bounds
```
int global_array[10] = {0};
int main() {
    int boom = global_array[20]; // BOOM
    return 0;
}
```

```
// Commands
g++ -fsanitize=address -g -o global.o GlobalOutOfBounds.cpp
./global.o

// ASan Report

=================================================================
==994==ERROR: AddressSanitizer: global-buffer-overflow on address 0x560e743540f0 at pc 0x560e74351207 bp 0x7fff090e2b20 sp 0x7fff090e2b10
READ of size 4 at 0x560e743540f0 thread T0
    #0 0x560e74351206 in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/GlobalOutOfBounds.cpp:3
    #1 0x7f93221d5d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f93221d5e3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x560e74351104 in _start (/mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/global.o+0x1104)

0x560e743540f0 is located 40 bytes to the right of global variable 'global_array' defined in 'GlobalOutOfBounds.cpp:1:5' (0x560e743540a0) of size 40
SUMMARY: AddressSanitizer: global-buffer-overflow /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/GlobalOutOfBounds.cpp:3 in main
Shadow bytes around the buggy address:
  0x0ac24e8627c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e8627d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e8627e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e8627f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e862800: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9
=>0x0ac24e862810: 00 00 00 00 00 00 00 00 00 f9 f9 f9 f9 f9[f9]f9
  0x0ac24e862820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e862830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e862840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e862850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0ac24e862860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==994==ABORTING
```

```
// Commands
// valgrind ./global.o

// Valgrind Report

==1229== Memcheck, a memory error detector
==1229== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1229== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1229== Command: ./global.o
==1229==
==1229== 
==1229== HEAP SUMMARY:
==1229==     in use at exit: 0 bytes in 0 blocks
==1229==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1229==
==1229== All heap blocks were freed -- no leaks are possible
==1229==
==1229== For lists of detected and suppressed errors, rerun with: -s
==1229== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
  

### Use-after-free
```
int main() {
  int *array = new int[10];
  delete [] array;
  return array[0]; // BOOM
}
```

```
// Commands
// g++ -fsanitize=address -g -o free.o UseAfterFree.cpp
// ./free.o

// ASan Report
=================================================================
==1107==ERROR: AddressSanitizer: heap-use-after-free on address 0x604000000010 at pc 0x55c2e1e1d22d bp 0x7ffe3d0fa6b0 sp 0x7ffe3d0fa6a0
READ of size 4 at 0x604000000010 thread T0
    #0 0x55c2e1e1d22c in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterFree.cpp:4
    #1 0x7f0b0ee9dd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f0b0ee9de3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55c2e1e1d104 in _start (/mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/free.o+0x1104)

0x604000000010 is located 0 bytes inside of 40-byte region [0x604000000010,0x604000000038)
freed by thread T0 here:
    #0 0x7f0b0f483e37 in operator delete[](void*) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:163
    #1 0x55c2e1e1d1f5 in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterFree.cpp:3
    #2 0x7f0b0ee9dd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

previously allocated by thread T0 here:
    #0 0x7f0b0f483337 in operator new[](unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:102
    #1 0x55c2e1e1d1de in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterFree.cpp:2
    #2 0x7f0b0ee9dd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-use-after-free /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterFree.cpp:4 in main
Shadow bytes around the buggy address:
  0x0c087fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c087fff8000: fa fa[fd]fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c087fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1107==ABORTING
```

```
// Valgrind Report

==1183== Memcheck, a memory error detector
==1183== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1183== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1183== Command: ./free.o
==1183==
==1183== Invalid read of size 4
==1183==    at 0x10919A: main (in /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/free.o)
==1183==  Address 0x4dd2c80 is 0 bytes inside a block of size 40 free'd
==1183==    at 0x484CA8F: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1183==    by 0x109195: main (in /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/free.o)
==1183==  Block was alloc'd at
==1183==    at 0x484A2F3: operator new[](unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1183==    by 0x10917E: main (in /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/free.o)
==1183==
==1183==
==1183== HEAP SUMMARY:
==1183==     in use at exit: 0 bytes in 0 blocks
==1183==   total heap usage: 2 allocs, 2 frees, 72,744 bytes allocated
==1183==
==1183== All heap blocks were freed -- no leaks are possible
==1183==
==1183== For lists of detected and suppressed errors, rerun with: -s
==1183== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```


### Use-after-return
```
int *ptr;

void func() {
  int local[10];
  ptr = &local[0];
}

int main(int argc, char **argv) {
  func();
  return *ptr;
}
```

```
// Commands
// g++ -fsanitize=address -g -o return.o UseAfterReturn.cpp
// ASAN_OPTIONS=detect_stack_use_after_return=1 ./return.o

// ASan Report

=================================================================
==1144==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f2f97820030 at pc 0x55e7fd5d7374 bp 0x7ffe0d25f6f0 sp 0x7ffe0d25f6e0
READ of size 4 at 0x7f2f97820030 thread T0
    #0 0x55e7fd5d7373 in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterReturn.cpp:10
    #1 0x7f2f9adbfd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f2f9adbfe3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55e7fd5d7144 in _start (/mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/return.o+0x1144)

Address 0x7f2f97820030 is located in stack of thread T0 at offset 48 in frame
    #0 0x55e7fd5d7218 in func() /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterReturn.cpp:3

  This frame has 1 object(s):
    [48, 88) 'local' (line 4) <== Memory access at offset 48 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/UseAfterReturn.cpp:10 in main
Shadow bytes around the buggy address:
  0x0fe672efbfb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efbfc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efbfd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efbfe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efbff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe672efc000: f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5 f5
  0x0fe672efc010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efc020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efc030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efc040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe672efc050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1144==ABORTING
```

```
// Valgrind Report

==1166== Memcheck, a memory error detector
==1166== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==1166== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==1166== Command: ./return.o
==1166==
==1166== Syscall param exit_group(status) contains uninitialised byte(s)
==1166==    at 0x494DCA1: _Exit (_exit.c:30)
==1166==    by 0x48A8551: __run_exit_handlers (exit.c:136)
==1166==    by 0x48A860F: exit (exit.c:143)
==1166==    by 0x488CD96: (below main) (libc_start_call_main.h:74)
==1166==
==1166==
==1166== HEAP SUMMARY:
==1166==     in use at exit: 0 bytes in 0 blocks
==1166==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==1166==
==1166== All heap blocks were freed -- no leaks are possible
==1166==
==1166== Use --track-origins=yes to see where uninitialised values come from
==1166== For lists of detected and suppressed errors, rerun with: -s
==1166== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## Part 2 - False Negative

```
// Error case
int main() {
  int a[8] = {0};
  int b[8] = {0};
  int res = a[8];  // BOOM
  return res;
}
```

```
//ASan Report

=================================================================
==1300==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fff8112eb30 at pc 0x562301e28372 bp 0x7fff8112ead0 sp 0x7fff8112eac0
READ of size 4 at 0x7fff8112eb30 thread T0
    #0 0x562301e28371 in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/Redzone.cpp:4
    #1 0x7fe83c44bd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7fe83c44be3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x562301e28124 in _start (/mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/redzone.o+0x1124)

Address 0x7fff8112eb30 is located in stack of thread T0 at offset 64 in frame
    #0 0x562301e281f8 in main /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/Redzone.cpp:1

  This frame has 2 object(s):
    [32, 64) 'a' (line 2) <== Memory access at offset 64 overflows this variable
    [96, 128) 'b' (line 3)
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /mnt/c/Users/bwdon/Desktop/software_testing/311551035-ST-2023/Lab06/Redzone.cpp:4 in main
Shadow bytes around the buggy address:
  0x10007021dd10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dd20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dd30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dd40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dd50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f1 f1
=>0x10007021dd60: f1 f1 00 00 00 00[f2]f2 f2 f2 00 00 00 00 f3 f3
  0x10007021dd70: f3 f3 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dd80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dd90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021dda0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10007021ddb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==1300==ABORTING
```

```
// Safe case
int main() {
  int a[8] = {0};
  int b[8] = {0};
  int res = a[16];  // SAFE
  return res;
}
```

```
// No ASan report
```
------------------------------------------
  
## Valgrind
Valgrind is a powerful open-source tool used for debugging, profiling, and memory management of software applications. It provides a suite of tools that help identify memory leaks, buffer overflows, and other common programming errors. Valgrind can be used with a variety of programming languages and is widely used by developers and software testers. It runs on Unix-based operating systems and can be integrated into a developer's workflow to improve the quality and reliability of their software.

## ASan
 ASan, or AddressSanitizer, is a memory error detector tool that helps identify memory-related bugs in C and C++ programs. It works by intercepting memory access operations and checking them against a shadow memory area to detect errors such as buffer overflows, use-after-free, and other types of memory-related bugs. ASan can be used as a standalone tool or integrated into other tools such as compilers or debuggers. It is part of the LLVM compiler infrastructure and is open-source software, freely available for use by developers. ASan can be an effective tool for improving the quality and reliability of software programs, especially those that handle sensitive or critical data.

|             | Valgrind                          | ASan (AddressSanitizer)          |
|-------------|----------------------------------|---------------------------------|
| Purpose     | Debugging, profiling, memory mgmt | Memory error detection           |
| Language    | C, C++, Java, Python, others      | C, C++                          |
| Tools       | Memcheck, Callgrind, Helgrind     | ASan (AddressSanitizer)         |
| Detection   | Memory leaks, invalid memory use  | Buffer overflows, use-after-free |
| Performance | Slower due to dynamic analysis    | Faster due to compile-time checks |
| Integration | Standalone tool                   | Can be integrated into compilers |
| Availability| Widely available for Unix systems | Part of LLVM compiler infrastructure |