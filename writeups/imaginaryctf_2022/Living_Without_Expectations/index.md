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
[!details:コード:(!src:lwe.py:py)]

### 解法

ascii の制約より一部の bit が 0 である場所が特定できるので、そこの式について LLL。
[!details:スクリプト:(!src:solve.sage:py)]
