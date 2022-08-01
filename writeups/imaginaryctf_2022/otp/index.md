---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: otp
genre: crypto
solved_date: 2022-07-16
during_ctf: true
tag: [random]
fav: false
difficulty: beginner
---

### 概要

ランダムなバイトに xor された flag を何度でも取得できる。
<details><summary>コード</summary>

```py
#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes, bytes_to_long
import random
import math

def secureRand(bits, seed):
  jumbler = []
  jumbler.extend([2**n for n in range(300)])
  jumbler.extend([3**n for n in range(300)])
  jumbler.extend([4**n for n in range(300)])
  jumbler.extend([5**n for n in range(300)])
  jumbler.extend([6**n for n in range(300)])
  jumbler.extend([7**n for n in range(300)])
  jumbler.extend([8**n for n in range(300)])
  jumbler.extend([9**n for n in range(300)])
  out = ""
  state = seed % len(jumbler)
  for _ in range(bits):
    if int(str(jumbler[state])[0]) < 5:
      out += "1"
    else:
      out += "0"
    state = int("".join([str(jumbler[random.randint(0, len(jumbler)-1)])[0] for n in range(len(str(len(jumbler)))-1)]))
    print(out)
  return long_to_bytes(int(out, 2)).rjust(bits//8, b'\0')

def xor(var, key):
  return bytes(a ^ b for a, b in zip(var, key))

def main():
  print("Welcome to my one time pad as a service!")
  flag = open("flag.txt", "rb").read()
  seed = random.randint(0, 100000000)
  while True:
    inp = input("Enter plaintext: ").encode()
    if inp == b"FLAG":
      print("Encrypted flag:", xor(flag, secureRand(len(flag)*8, seed)).hex())
    else:
      print("Encrypted message:", xor(inp, secureRand(len(inp)*8, seed)).hex())

if __name__ == "__main__":
  main()
```

</details>


### 解法

乱数に偏りがあるので、各 bit の頻度を解析すればよい。
<details><summary>スクリプト</summary>

```py
from collections import Counter
from pwn import *

REMOTE_ADDR = 'otp.chal.imaginaryctf.org'
REMOTE_PORT = 1337

stream = remote(REMOTE_ADDR, REMOTE_PORT)
l = None
for i in range(200):
  stream.sendline(b"FLAG")
  stream.recvuntil(b"flag: ")
  enc = stream.recvline(keepends=False)
  print(enc)
  if l is None: l = [Counter() for i in range(len(enc) * 4)]
  enc = int(enc, 16)
  for c in l:
    c[enc & 1] += 1
    enc //= 2

  print(f'[+] {i=}')
  res = ""
  for c in l[::-1]:
    res += str(1 ^ c.most_common(1)[0][0])

  print(int(res, 2).to_bytes(len(res) // 8, "little")[::-1])
```

</details>

