---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: maas
genre: web
solved_date: 2022-07-18
during_ctf: true
tag: [random,uuid]
fav: false
difficulty: easy
---

### 概要

[!details:コード:(!src:app.py:py)]

### 解法

UUID1 にはタイムスタンプの情報が載っているので、seed 設定時刻がある程度予測できる。よって、それを探索してパスワードを予測すればよい。

[!details:スクリプト:(!src:solve.py:py)]
