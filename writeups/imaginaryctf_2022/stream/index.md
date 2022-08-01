---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: stream
genre: crypto
solved_date: 2022-07-17
during_ctf: true
tag: []
fav: false
difficulty: easy
---

### 概要

ファイルを暗号化するバイナリと、暗号化後のフラグが渡される。バイナリは整数をキーとして取っている。

### 解法

バイナリを読むと、暗号化は大まかに以下のような処理を行っていることがわかった。

```c
uint64_t *buf;
for (int i = 0; i < n; i++) {
  buf[i] ^= key;
  key *= key;
}
```

最初のチャンクが `ictf{` から始まることを利用すると `key` の下位 40 bit が判明し、それを用いると全チャンクの下位 40 bit が分かった。これを用いると、最後のチャンクが `}\n` であることが分かった。これで `key^32` が判明したので、`key` の候補を絞り込むことができるようになった。これは高々 32 通りなので、全て試せばよい。

<details><summary>スクリプト</summary>

```py
import subprocess

out = open("out.txt", "rb").read()
print(out)
print(2**(len(out) // 8 - 3))

last = int.from_bytes(out[-8:], "little") ^^ int.from_bytes(b'}\n', "little")
print(hex(last))
for key in mod(last, 2**64).nth_root(2**(len(out) // 8 - 1), all=True):
  print(key)
  subprocess.call(["./stream", "out.txt", str(key), "res.txt"])
  with open("res.txt", "rb") as f:
    res = f.read()
    if not res.startswith(b"ictf{"): continue
    print(res)
```

</details>

