---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: desrever
genre: rev
solved_date: 2022-07-17
during_ctf: true
tag: [python]
fav: false
difficulty: beginner
---

### 概要

```py
#!/usr/bin/env python3

cexe = exec
cexe(')]"}0p381o91_flnj_3ycvgyhz_av_tavferire{sgpv"==)]pni ni _ rof _ esle "9876543210_}{" ni ton _ fi ]_[d.siht[(nioj.""[)"tcerroc","gnorw"((tnirp;)" >>>"(tupni=pni;)"?galf eht si tahW"(tnirp;siht tropmi'[::-1])
```


### 解法

`exec` で実行されているスクリプトは以下の通り:

```py
'import this;print("What is the flag?");inp=input(">>> ");print(("wrong","correct")["".join([this.d[_] if _ not in "{}_0123456789" else _ for _ in inp])=="vpgs{erirefvat_va_zhygvcy3_jnlf_19o183p0}"])'
```

`this.D` は rot13 のテーブルなので、`vpgs{erirefvat_va_zhygvcy3_jnlf_19o183p0}` を rot13 にかければよい。
