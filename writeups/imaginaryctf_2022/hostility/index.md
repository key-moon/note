---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: hostility
genre: web
solved_date: 2022-07-18
during_ctf: false
tag: [directory_traversal,host]
fav: false
difficulty: easy
---

### 概要

[!details:コード:(!src:app.py:py)]

### 解法

自明なディレクトリトラバーサルがある。5 分おきに再起動されるので、まずそのタイミングで読み込まれる何らかのモジュールの `__init__.py` を書き換えることを考えた。

[!details:スクリプト:(!src:solve1.py:py)]

これはローカルだと上手く行ったものの、リモートには刺さらなかった。おそらく再起動時の処理が違ったのだろう。正解は `/etc/hosts` の書き換え。問題名に解法のヒントを含めるの、あまり好きではないのでやめてほしいな……

[!details:スクリプト:(!src:solve2.py:py)]
