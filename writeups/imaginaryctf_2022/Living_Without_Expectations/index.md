---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: Living Without Expectations
genre: crypto
solved_date: 2022-07-17
during_ctf: true
tag: [lattice,lll]
fav: false
difficulty: normal
---

### 概要

誤差項がとても小さい `LWE`。
<details><summary>コード</summary>

```py
import numpy as np
import secrets

def rand(seed):
    seeds = [(seed >> (3 * i)) & 7 for i in range(nseeds)]
    a = 5
    b = 7
    while True:
        for i in range(nseeds):
            seeds[i] = (a * seeds[i] + b) & 7
            yield seeds[i]


q = 2**142 + 217
n = 69
nseeds = 142
rng = rand(secrets.randbits(3 * nseeds))
with open("flag.txt", "rb") as f:
    flag = f.read().strip()
bits = f'{int.from_bytes(flag, "big"):0{len(flag) * 8}b}'
s = np.array([secrets.randbits(1) for _ in range(n)])

print([next(rng) for _ in range(n)])

for bit in map(int, bits):
    A = np.array([secrets.randbelow(q) for _ in range(n * n)]).reshape((n, n))
    b = [A @ s + np.array([next(rng) for _ in range(n)]), np.array([secrets.randbelow(q) for _ in range(n)])][bit]
    print(list(map(hex, A.reshape(-1))), list(map(hex, b % q)))
```

</details>


### 解法

ascii の制約より一部の bit が 0 である場所が特定できるので、そこの式について LLL。
<details><summary>スクリプト</summary>

```py
from progressbar import progressbar


with open("output.txt") as f:
  ls = f.readlines()

# "'0x...', '0x...', '0x...'"
def parse_arr(s):
  return [int(elem[3:-1], 16) for elem in s.split(', ')]

q = 2**142 + 217
n = 69

cs = []
for l in progressbar(ls):
  s = l.split('] [')
  assert len(s) == 2
  As, bs = s
  A, b = parse_arr(As[1:]), parse_arr(bs[:-2])
  A = matrix(ZZ, n, n, A)
  b = matrix(ZZ, b)
  cs.append((A, b))

SCALE = 10 ** 20
INF   = 10 ** 50
zs = [0]
block = [
  [*[cs[z][0].transpose() for z in zs], matrix.identity(n) * 2 * SCALE,        matrix(ZZ, n, 1)],
  [*[cs[z][1]             for z in zs],        matrix([1] * n) * SCALE, matrix(ZZ, 1, 1, [INF])],
  [             matrix.identity(n) * q,               matrix(ZZ, n, n),        matrix(ZZ, n, 1)]
]

mat = block_matrix(block)

for row in Matrix(ZZ, mat).LLL():
  if row[-1] == 0: continue
  print(f'[+] {row=}')
  s = matrix(Zmod(q), n, 1, [0 if 0 < elem else 1 for elem in row[n:][:n]])
  binary = ""
  for A, b in cs:
    diff_sum = sum(abs(b1 - b2) for b1, b2 in zip(matrix(ZZ, 1, n, (A * s).list()), b))
    binary += "0" if diff_sum <= 1000 else "1"
  print(f'[+] {binary=}')
  print(int(binary, 2).to_bytes(len(binary) // 8 + 1, "big"))
```

</details>

