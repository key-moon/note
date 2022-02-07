---
layout: chall
ctf_name: DiceCTF_2022
problem_name: baby-rop
genre: pwn
solved_date: 2022-02-05
during_ctf: true
tag: [heap, uaf, rop, seccomp]
---

### 概要

自明な UAF のあるアプリケーション。seccomp で諸々が縛られている。open や read などはできるが、execve はできない。

```
[!checksec:babyrop]
```

[!details:コード:(!src:uaf.c:c)]

### 解法

「あなたは `execve('/bin/sh', 0, 0)` 以外の ROP ができますか?」という問題。AAR で libc や stack のアドレスをリークしてから ROP chain を直で書き込んで ROP をする。

[!details:スクリプト:(!src:solve.py:py)]
