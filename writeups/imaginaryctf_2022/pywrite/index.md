---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: pywrite
genre: pwn
solved_date: 2022-07-18
during_ctf: true
tag: [python]
fav: false
difficulty: easy
---

### 概要

[!src:vuln.py:py]

### 解法

`open(input())` が呼ばれた時点で何らかの関数を呼び出してファイルを open しているはずなので、この関数の got を書き換えれば `system(/bin/sh)` ができるはずである。`open` が呼んでいる関数は `open64`  だったので、そこの got を `system` に書き換えた。

[!details:スクリプト:(!src:solve.py:py)]
