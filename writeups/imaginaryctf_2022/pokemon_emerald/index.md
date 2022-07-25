---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: pokemon_emerald
genre: misc
solved_date: 2022-07-19
during_ctf: true
tag: [ruby,jail]
fav: false
difficulty: easy
---

### 概要

`{}`

[!details:コード:(!src:jail.rb:rb)]

### 解法

`%` が含まれていることから、ruby の [% 文字列](https://docs.ruby-lang.org/ja/latest/doc/spec=2fliteral.html#percent)を用いると推測できる。`%{}` でコマンドの実行結果を文字列として表示できる。`ruby` コマンドは引数を与えなければ標準入力から受け取り、コードとして評価する。なので、`%{ruby}` を送信した後に任意のスクリプトを送り込み、最後にEOF の代わりとなる `\x04` を送信すればよい。`EOF` の代わりは `stream.shutdown()` を使っても実現できる。

[!details:スクリプト:(!src:solve.py:py)]
