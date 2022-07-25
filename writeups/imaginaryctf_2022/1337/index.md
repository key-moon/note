---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: 1337
genre: web
solved_date: 2022-07-18
during_ctf: true
tag: [ssti,mojo]
fav: false
difficulty: easy
---

### 概要

[!details:コード:(!src:source.js:js)]

### 解法

SSTI が作り込まれているので、`<%= (await import("child_process")).execSync("ls").toString() %>` のようなペイロードで発火させることができる。しかし、文字列リテラルを含めることはできないので、文字列を `Number.toString(base)` と `String.charCodeAt` で構成した。後から気がついたことだが、正規表現リテラルを用いればもう少々簡略化できたかもしれない。

[!details:スクリプト:(!src:solve.py:py)]
