---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: The House Always Wins
genre: rev
solved_date: 2022-07-19
during_ctf: true
tag: [rng,bruteforce]
fav: false
difficulty: easy
---

### 概要

期待値が正でない High-Low ゲームがリモートで動いている。一定以上お金を貯めれば勝ち。

### 解法

乱数の初期化処理では、urandom からとってきた 32 bit 整数で `srand` をした上で数万回程度乱数を消費していた。

```c
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
```

初期値との対応表を前計算することでシードのクラックをある程度高速化できそうである。2^32 個初期値を求めるのは時間がかかるため、2^28 個求めることにした。これは 8 コアのノート PC を用いて数分で行うことができた。

<details><summary>スクリプト</summary>

```c
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
```

</details>


次に、この対応表を用いてシードをクラックし、成功した場合は予測される乱数列を返すプログラムを書いた。前計算したテーブルをテキストファイルからメモリにロードする部分がボトルネックだったため、起動時に一括で読み込むようにした。

<details><summary>スクリプト</summary>

```c
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
```

</details>


これを用いてリモートにつなぎ、フラグを取得するプログラムは以下の通り:

<details><summary>スクリプト</summary>

```py
from pwn import *

REMOTE_ADDR = 'the-house-always-wins.chal.imaginaryctf.org'
REMOTE_PORT = 1337
LOCAL = False

find = process(["./find", "128", "8"])
find.recvuntil(b'LOAD\n', drop=True)
print(f'[+] loaded.')

stream = None
def reconnect():
  global stream
  if stream is not None: stream.close()
  if LOCAL: stream = process("./casino")
  else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

def game(bet, choice):
  stream.sendlineafter(b'>>> ', str(bet).encode())
  stream.recvuntil(b'The first number is ')
  fst = int(stream.recvuntil(b'.', drop=True).decode())
  stream.sendlineafter(b'>>> ', str(choice).encode())
  stream.recvuntil(b'The second number is ')
  snd = int(stream.recvuntil(b'!', drop=True).decode())
  return (fst, snd)

def money():
  stream.recvuntil(b'Current money: ')
  return int(stream.recvline(keepends=False).decode())

while True:
  reconnect()
  v1, v2 = game(5, 1)
  v3, v4 = game(5, 1)
  find.sendline(f'{v1} {v2} {v3} {v4}'.encode())
  res = find.recvuntil(b'END\n', drop=True)
  if len(res) == 0: continue
  l = [*map(int, res.decode().strip().split())]
  for i in range(0, len(l), 2):
    fst, snd, m = l[i], l[i + 1], money()
    print(f'[+] {m=}')
    if 1000000000 <= m: break
    game(m if fst != snd else 5, 1 if fst < snd else 2) 
  stream.interactive()
  break
```

</details>

