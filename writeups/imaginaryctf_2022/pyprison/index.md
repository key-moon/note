---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: pyprison
genre: misc
solved_date: 2022-07-17
during_ctf: true
tag: [pyjail]
fav: false
difficulty: beginner
---

### 概要

```py
#!/usr/bin/env python3

while True:
  a = input(">>> ")
  assert all(n in "()abcdefghijklmnopqrstuvwxyz" for n in a)
  exec(a)
```


### 解法

`eval(input())` としてから、実行したいコードを入力すればよい。

ちなみに任意の python コードをこの制約で書くこともできる。（参考: [Python 2/3 で小文字アルファベットと丸括弧だけでプログラムを書く](https://shinh.hatenablog.com/entry/2015/05/11/012223)）
