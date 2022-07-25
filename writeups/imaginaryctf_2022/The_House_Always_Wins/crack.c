#include <stdio.h>
#include <stdlib.h>

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
  uint n = strtol(argv[1], 0, 10);
  uint j = strtol(argv[2], 0, 10);

  char* name = (char*)malloc(0x20);
  sprintf(name, "res_%d_%d.txt", n, j);

  FILE* f = fopen(name, "w");

  uint cnt = (uint)((1LL << 32) / n);
  uint offset = cnt * j;

  printf("[+] cnt=%u, offset=%u\n", cnt, offset);
  for (uint i = 0; i < cnt; i++) {
    if (!(i % 100000)) {
      printf("[+] %u / %u (%f%%)\n", i, cnt, (float)i / cnt * 100);
      fflush(f);
    }
    fprintf(f, "%x ", set_seed_and_rand(offset + i));
  }
  fflush(f);
  fclose(f);
}
