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

[!details:コード:(!src:chall.py:py)]

### 解法

各素数が小さいので、素因数分解が簡単にできそうである。factordb に突っ込むと結果が出てきた。
e と λ(n) が互いに素でないため、複数の結果がありうる。sage の `nth_root` のオプションに `all=True` を指定すると良い。

[!details:スクリプト:(!src:script.sage:py)]
