---
layout: chall
ctf_name: DiceCTF_2022
problem_name: interview-opportunity
genre: pwn
solved_date: 2022-02-05
during_ctf: true
tag: [rop, warmup]
---

### 概要

バイナリのみ渡される。自明な bof があり、30 bytes 程度の rop chain が書き込める。

```
[!checksec:interview-opportunity]
```

[!details:コード:(!src:chall.c:c)]

### 解法

puts(puts) で libc のアドレスリークをした後、`rbp` を書き込み可能領域に設定してから `read` を呼ぶ直前に rop で飛ばす。こうすることで、70 byte のデータを既知のアドレスに書き込める。これは `execve` の rop を入れるのに十分な大きさなので、これを書き込む。そして、次の rop で stack pivot をすればよい。

[!details:スクリプト:(!src:solve.py:py)]
