---
layout: chall
ctf_name: DiceCTF_2022
problem_name: baby-rsa
genre: crypto
solved_date: 2022-02-05
during_ctf: true
tag: [rsa, warmup, factordb]
---

### 概要

p, q が 128 bit の素数での RSA。e が λ(n) と互いに素でない。

<details><summary>コード</summary>

```py
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def getAnnoyingPrime(nbits, e):
	while True:
		p = getPrime(nbits)
		if (p-1) % e**2 == 0:
			return p

nbits = 128
e = 17

p = getAnnoyingPrime(nbits, e)
q = getAnnoyingPrime(nbits, e)

flag = b"dice{???????????????????????}"

N = p * q
cipher = pow(bytes_to_long(flag), e, N)

print(f"N = {N}")
print(f"e = {e}")
print(f"cipher = {cipher}")
```

</details>


### 解法

各素数が小さいので、素因数分解が簡単にできそうである。factordb に突っ込むと結果が出てきた。
e と λ(n) が互いに素でないため、複数の結果がありうる。sage の `nth_root` のオプションに `all=True` を指定すると良い。

<details><summary>スクリプト</summary>

```py
n = 57996511214023134147551927572747727074259762800050285360155793732008227782157
e = 17
c = 19441066986971115501070184268860318480501957407683654861466353590162062492971
 
p = 337117592532677714973555912658569668821
q = 172036442175296373253148927105725488217
assert p * q == n
 
pari(f"addprimes({p})")
for m in mod(c, n).nth_root(e, all=True):
  m = int(m).to_bytes(100, "big")
  if m.startswith(b'dice{'):
    print(m)
```

</details>

