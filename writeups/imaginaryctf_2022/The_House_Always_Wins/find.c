#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define uint unsigned int

int set_seed_and_rand(uint seed) {
  int _i;
  srand(seed);
  _i = 0;
  while( 1 ) {
    int iVar1 = rand();
    if (iVar1 >> 0xf <= _i) break;
    rand();
    _i = _i + 1;
  }
  return rand() >> 0xf;
}

int get_rand() {
  rand();
  return rand() >> 0xf;
}

void main(int argc, char** argv) {
  char buf[0x100];

  uint n = strtol(argv[1], 0, 10);
  uint j = strtol(argv[2], 0, 10);

  uint chunk = (uint)((1LL << 32) / n);
  uint cnt = chunk * j;
  uint* table = (uint*)malloc(cnt * sizeof(uint));

  for (int i = 0; i < j; i++) {
    char* name = (char*)malloc(0x20);
    sprintf(name, "res_%d_%d.txt", n, i);
    FILE* f = fopen(name, "r");
    for (uint ind = 0; ind < chunk; ind++) {
      fscanf(f, "%10s", buf);
      table[chunk * i + ind] = strtol(buf, 0, 16);
    }
  }

  puts("LOAD");

  while (1) { 
    int val1, val2, val3, val4;
    scanf("%d %d %d %d", &val1, &val2, &val3, &val4);
    for (uint seed = 0; seed < cnt; seed++) {
      int res1 = table[seed];
      if (val1 != res1) continue;
      assert(set_seed_and_rand(seed) == res1);
      int res2 = get_rand();
      if (res2 != val2) continue;
      int res3 = get_rand();
      if (res3 != val3) continue;
      int res4 = get_rand();
      if (res4 != val4) continue;

      for (int k = 0; k < 100; k++) {
        printf("%d ", get_rand());
      }
    }
    puts("END");
  }
}
