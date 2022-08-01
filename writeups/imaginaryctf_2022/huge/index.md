---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: huge
genre: crypto
solved_date: 2022-07-16
during_ctf: true
tag: [rsa, small_prime]
fav: false
difficulty: beginner
---

### 概要

`N` が小さい素数の積のときの RSA。
<details><summary>コード</summary>

```py
from Crypto.Util.number import bytes_to_long, getPrime
from random import randint

flag = open("flag.txt", "rb").read()

def get_megaprime():
  primes = [getPrime(10) for _ in range(200)]
  out = 1
  for n in range(100):
    if randint(0,1) == 0:
      out *= primes[n]
  return out

p = get_megaprime()
q = get_megaprime()
n = p*q
e = 65537
m = bytes_to_long(flag)

c = pow(m, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
```

</details>


### 解法

素因数分解が可能なので phi が求まる。自前でやってもよいが、sage に頼ると楽。
```py
from out import n, e, c

print(int(mod(c, n).nth_root(e)).to_bytes(100, "big"))
```

