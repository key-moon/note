---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: CyberCook
genre: web
solved_date: 2022-07-18
during_ctf: true
tag: [wasm,xss]
fav: false
difficulty: normal
---

### 概要



### 解法

実験をしていると、変換する文字の長さが 60 字以上のときに戻り値のポインタを base64 でエンコードした後の値によって書き換えることができることが分かった。これを用いて、hex を変換した後のバッファの位置にポインタを
向け、`innerHtml` に書き込まれる値を制御することができた。
[!details:スクリプト:(!src:solve.py:py)]
