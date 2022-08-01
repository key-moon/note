---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: hash
genre: crypto
solved_date: 2022-07-17
during_ctf: true
tag: [hash,z3]
fav: false
difficulty: easy
---

### 概要

自前のハッシュ関数が与えられる。ランダムな文字列をハッシュ化した前の値を 50 回連続で正解できればよい。
<details><summary>コード</summary>

```py
#!/usr/bin/env python3

import string
import random

# 30x42
config = [[int(a) for a in n.strip()] for n in open("jbox.txt").readlines()] # sbox pbox jack in the box

# secure hashing algorithm 42
def sha42(s: bytes, rounds=42):
  out = [0]*21
  for round in range(rounds):
    for c in range(len(s)):
      if config[((c//21)+round)%len(config)][c%21] == 1:
        out[(c+round)%21] ^= s[c]
  return bytes(out).hex()

def main():
  print("Can you guess my passwords?")
  for trial in range(50):
    print(f"--------ROUND {trial}--------")
    password = "".join([random.choice(string.printable) for _ in range(19)]).encode()
    hash = sha42(password)
    print(f"sha42(password) = {hash}")
    guess = bytes.fromhex(input("hex(password) = ").strip())
    if sha42(guess) == hash:
      print("Correct!")
    else:
      print("Incorrect. Try again next time.")
      exit(-1)
  flag = open("flag.txt", "r").read()
  print(f"Congrats! Your flag is: {flag}")

if __name__ == "__main__":
  main()
```

</details>


### 解法
線形変換なので、z3 に投げれば良い。いくつかケースがあるので、`multiprocessing` で並列処理をした。
<details><summary>スクリプト</summary>

```py
import queue
from pwn import *
from z3 import *
import multiprocessing

BIN_NAME = './hoge.py'
REMOTE_ADDR = 'hash.chal.imaginaryctf.org'
REMOTE_PORT = 1337


# stream = process(["python", "hash.py"])
stream = remote(REMOTE_ADDR, REMOTE_PORT)

config = [[int(a) for a in n.strip()] for n in open("jbox.txt").readlines()] # sbox pbox jack in the box

# secure hashing algorithm 42
def sha42_bv(s, rounds=42):
  out = [0]*21
  for round in range(rounds):
    for c in range(len(s)):
      if config[((c//21)+round)%len(config)][c%21] == 1:
        out[(c+round)%21] ^= s[c]
  return out
def sha42(s: bytes, rounds=42):
  return bytes(sha42_bv(s, rounds)).hex()

def solve(l, length, q):
  print(f'[+] {length=}')
  vals = [BitVec(f"s_{i}", 8) for i in range(length)]
  hash_res = sha42_bv(vals)
  s = Solver()
  for stmt, val in zip(hash_res, bytes.fromhex(l)):
    s.add(stmt == val)
  while True:
    if s.check() != sat: return None

    m = s.model()
    res = bytes([m[val].as_long() for val in vals])
    print(f'[+] {res=}')

    while res[-1] == 0: res = res[:-1]
    if any(chr(c) not in string.printable for c in res):
      print(f'[!] invalid')
      cond = False
      for val, c in zip(vals, res):
        cond = Or(cond, val != c)
      s.add(cond)
      continue

    print(f'[+] valid. {res=}')
    assert sha42(res) == l
    q.put(res.hex().encode())
    return

  

for i in range(50):
  stream.recvuntil(b'sha42(password) = ')
  l = stream.recvline(keepends=False).decode()
  print(f'[+] {i=}, {l=}')
  q = multiprocessing.Queue()
  ts = []
  for length in [15, 16, 17, 18, 19, 20]:
    t = multiprocessing.Process(target=solve, args=(l, length, q))
    t.start()
    ts.append(t)
  res = q.get()
  print(f'[+] res: {res}')
  for t in ts: t.terminate()
  stream.sendline(res)
  


stream.interactive()
```

</details>

