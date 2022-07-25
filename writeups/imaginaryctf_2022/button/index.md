---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: button
genre: web
solved_date: 2022-07-17
during_ctf: true
tag: [obfuscation]
fav: false
difficulty: beginner
---

### 概要

以下のように button が連なった HTML が与えられる。
[!src:index_truncate.html:html]

### 解法

グローバル変数の一覧見ると、`notSusFunction` の他に `motSusfunclion` という変数がある。これを開発者ツールで表示すると、`motSusfunclion(){alert("ictf{y0u_f0und_7h3_f1ag!}")}` という関数であると分かる。
