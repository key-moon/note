---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: hash
genre: crypto
solved_date: 2022-07-17
during_ctf: true
tag: [hash,z3]
fav: false
difficulty: easy
---

### 概要

自前のハッシュ関数が与えられる。ランダムな文字列をハッシュ化した前の値を 50 回連続で正解できればよい。
[!details:コード:(!src:hash.py:py)]

### 解法
線形変換なので、z3 に投げれば良い。いくつかケースがあるので、`multiprocessing` で並列処理をした。
[!details:スクリプト:(!src:solve.py:py)]
