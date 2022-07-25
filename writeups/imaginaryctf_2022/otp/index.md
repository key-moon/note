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
[!details:コード:(!src:otp.py:py)]

### 解法

乱数に偏りがあるので、各 bit の頻度を解析すればよい。
[!details:スクリプト:(!src:solve.py:py)]
