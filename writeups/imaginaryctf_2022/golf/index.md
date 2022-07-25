---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: golf
genre: pwn
solved_date: 2022-07-17
during_ctf: true
tag: [fsb]
fav: false
difficulty: normal
---

### 概要

`strlen` が 11 未満ならば、その文字列を用いて `printf` を呼ぶことができるバイナリがリモートで動いている。

```
[!checksec:golf]
```

[!details:元コード:(!src:golf.c:c)]
[!details:整形済みコード:(!src:golf_formatted.c:c)]

### 解法
文字数制限が厳しいので、引数によって書き込む文字数を指定することにした。これで、AAR/AAW が可能となった。これを用いて、まずは `exit` の got を main に向けた。ここからはいろいろな手法で shell が取れるが、今回は one gadget を用いることとした。libc のバージョンが与えられていなかったので、まずは libc のバージョンを決定した。その後に `setvbuf` の got に one gadget を書き込み、`exit` の got を初期化処理に向けることで one gadget を発火させた。

[!details:スクリプト:(!src:solve.py:py)]
