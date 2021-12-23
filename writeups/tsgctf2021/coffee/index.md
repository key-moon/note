---
layout: chall
ctf_name: TSG CTF 2021
problem_name: coffee
genre: pwn
solved_date: 2021-12-18
during_ctf: false
tag: [fsb, rop, fav]
---

## 概要

FSB があるが、一度しかできない(+文字数制限 160 文字)

```
[!checksec:coffee]
```

[!details:コード:(!src:coffee.c:c)]

## 解法

FSB で AAW ができるので、puts に RSP をズラすガジェットを置く。`add rsp, 0x08` 等が使えそうに見えるが、FSB をするためには先頭にFSB 用の文字列を置かなければいけない（FSB ペイロードの前にnull バイトが入ってはいけないので）。
RSP を `0x38` ズラすガジェットがあるので、ズラしきれるだけの FSB のペイロードを作り、その後に ROP のペイロードを置く。

```
0x00401286: add rsp, 0x08 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret  ;  (1 found)
```

書き込める量が限られているので、一旦別のセクションに scanf で書き込んでからそこに pivot する ROP を書く。scanf のアドレスには空白文字があるため直接呼べないが、main の scanf を呼び出している場所に飛ばせば任意アドレスに書き込みができる。

その後は execve する ROP を書き込んで終わり。

[!details:スクリプト:(!src:solve.py:py)]
