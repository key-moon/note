---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: polymorphic
genre: rev
solved_date: 2022-07-17
during_ctf: true
tag: [self-modifying-code]
fav: false
difficulty: easy
---

### 概要

フラグチェッカーのバイナリが渡される。試しに何かを入力すると segmentation fault する。

### 解法

デバッガで挙動を追うと、xor 命令を用いて自己書き換えをしていることがわかった。これの挙動も追いかけると、読み取った文字列から 1 byte ずつ `al` レジスタに取り出し、それを定数で減産した結果が 0 になった場合に正常に動作するコードであることが分かった。よって、`sub al, 0xXX` という命令に書き換えられるケースを集めればフラグを得ることができることになる。これは、以下のスクリプトによって行った。

<details><summary>スクリプト</summary>

```py
binary = open("polymorphic", "rb").read()

flag = False

res = ""

last = 0
while True:
  ind = binary.find(b'\x81\x35', last + 2) # xor [rip+0xXX], 0xXX
  if ind == -1: break
  off, arg = int.from_bytes(binary[ind+2:ind+6], "little"), int.from_bytes(binary[ind+6:ind+10], "little")
  if off == 0:
    # decoded instructions
    nxtins = int.from_bytes(binary[ind+10:ind+14], "little") ^ arg
    if flag and nxtins & 0xff == 0x2c: # sub al, 0xXX
      arg = nxtins >> 8 & 0xff
      res += chr((0x60 + arg) & 0xff)
      flag = False
    if nxtins & 0xffff == 0x602c:      # sub al, 0x60
      flag = True
  last = ind

print(res)
```

</details>

