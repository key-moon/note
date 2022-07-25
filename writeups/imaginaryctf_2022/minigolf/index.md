---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: minigolf
genre: web
solved_date: 2022-07-17
during_ctf: true
tag: [flask,ssti]
fav: false
difficulty: easy
---

### 概要

SSTI ができる flask のアプリケーションが与えられる。なお、`{{`, `}}`, `_`, `[`, `]` が縛られ、ペイロードに 69 文字の文字数制限がかかっている。また、ペイロードは挿入前に HTML エンコードされる。なので、`"` や `'` といった文字も実質的に縛られている。

[!details:コード:(!src:app.py:py)]

### 解法

[minigolf](../minigolf) と方針はほぼ同じ。今回は `{{` および `}}` を用いることができないため、外部に HTTP リクエストを送信することでデータを取得することにする。

[!details:スクリプト:(!src:solve.py:py)]
