---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: secure_encoding_hex
genre: crypto
solved_date: 2022-07-16
during_ctf: true
tag: [decode, randomized]
fav: false
difficulty: beginner
---

### 概要

hex された文字列 flag の hex が置換されて与えられる。

[!src:encode.py:py]
[!src:out.txt:txt]

### 解法
ascii 及び英単語の制約を元に、替字表を手作業で復元した。

[!src:solve.py:py]
