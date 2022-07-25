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
[!details:コード:(!src:chal.py:py)]

### 解法

素因数分解が可能なので phi が求まる。自前でやってもよいが、sage に頼ると楽。
[!src:solve.sage:py]
