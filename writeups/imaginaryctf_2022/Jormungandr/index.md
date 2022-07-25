---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: Jormungandr
genre: rev
solved_date: 2022-07-18
during_ctf: true
tag: [python]
fav: false
difficulty: easy
---

### 概要

python のフラグチェッカーが与えられる。

[!details:コード:(!src:jormungandr.py:py)]

### 解法

コードを眺めると自分のコードを読み取って、それを独自形式として解釈して実行するインタプリタのような挙動をしていることが分かった。難読化を解除する際にファイルをいじると動かなくなることが想定されるので、スクリプトを別のファイルにコピーした上で、`open(__FILE__)` として指定されているファイル名を別のファイルの名前に書き換えた。こうして解析を進めると、以下のようなスクリプトでフラグを復元できることが分かった。
[!src:solve.sage:py]
