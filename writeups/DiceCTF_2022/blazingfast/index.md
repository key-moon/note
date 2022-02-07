---
layout: chall
ctf_name: DiceCTF_2022
problem_name: blazingfast
genre: web
solved_date: 2022-02-05
during_ctf: true
tag: [wasm, unicode, jsfuck]
---

### 概要

WASM にて実装されている MoCkINg CaSe 化と、それをラップする HTML アプリケーションが与えられる。Admin Bot に対して XSS できれば勝ち。

```
[!checksec:chall]
```

[!details:コード:(!src:blazingfast.c:c)

(!src:index.js:js)]

### 解法

Unicode には、正規化処理を行う時に複数文字として処理される文字が存在する。例えば、文字 `ﬄ` は `FFL` といったように複数文字になる。これを用いて、wasm モジュール内で行われている XSS チェックをバイパスすることができる。

バイパスした後は、大文字化された文字によってスクリプトを組まなければいけない。また、入力には 1000 文字の文字数制限がある。バイパスのために 1/3 を特殊文字で埋めなければいけないため、実質的に 666 文字制限となっている。

BigInt.toString(36) にて 36 進数としての文字列化ができることを用いるために、toString に必要な文字を `(![]+[])` が `"false"` として評価されるといったことを用いて作った。結果として、スクリプトは特段の文字列削減の工夫をせずともおおよそ 500 文字程度となった。

[!src:payload.js:js]
