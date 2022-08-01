---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: hidden
genre: rev
solved_date: 2022-07-17
during_ctf: true
tag: []
fav: false
difficulty: beginner
---

### 概要

フラグチェッカーが渡される。

### 解法

デバッガで動きを追うことで、以下のようなスクリプトによってフラグを復元できることがわかった。
```py
r8 = 0x39e324b32f573c94
st = [0x7870148bf499d6f9, 0x435e9c9331495b55, 0x910a96fdf83deb08]
res = b''
for d in st:
  r8 = (r8 * r8) % (2 ** 64)
  print(hex(r8))
  res += (d ^ r8).to_bytes(8, "little")
  r8 = d
print(res)
```

