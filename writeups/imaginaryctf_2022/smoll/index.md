---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: smoll
genre: crypto
solved_date: 2022-07-16
during_ctf: true
tag: [rsa, smooth]
fav: false
difficulty: easy
---

### 概要

`p`, `q` が smooth な素数の場合の RSA。

<details><summary>コード</summary>

```py
from secret import p, q
from sage.all import factor

for r in [p, q]:
    for s, _ in factor(r - 1):
        assert int(s).bit_length() <= 20

n = p * q
e = 0x10001

with open("flag.txt", "rb") as f:
    flag = int.from_bytes(f.read().strip(), "big")
assert flag < n

ct = pow(flag, e, n)
print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")
```

</details>


### 解法

分からなかったが、factordb に `n` をかけたら素因数があった。

```py
from output import n, e, ct

p = 1314503602874176261160006408736468830398552989268751172636991566212261500942084902638924872933455766527167138778836649666000256787470232570894174402457567851267

pari(f"addprimes({p})")

print(int(mod(ct, n).nth_root(e)).to_bytes(100, "big"))
```

