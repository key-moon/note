---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: bsv
genre: forensics
solved_date: 2022-07-17
during_ctf: true
tag: [csv]
fav: false
difficulty: easy
---

### 概要

bsv という独自フォーマットのテキストファイルが渡される。
[!details:コード:(!src:flag.bsv:)]

### 解法

`BEE` という文字を区切り文字にした csv だと解釈する。すると、文字のあるセルの並びを文字として解釈できる。
![](excel.png)
