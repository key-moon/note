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

[!details:スクリプト:(!src:solve.py:py)]
