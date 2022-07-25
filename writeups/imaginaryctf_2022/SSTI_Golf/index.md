---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: SSTI Golf
genre: web
solved_date: 2022-07-17
during_ctf: true
tag: [flask,ssti]
fav: false
difficulty: easy
---

### 概要

SSTI できる flask のアプリケーションが与えられる。ペイロードは48 文字以下しか許可されていない。

[!details:コード:(!src:app.py:py)]

### 解法

まず、 `{{self._TemplateReference__context}}` というペイロードを送って有用なオブジェクトを探した。その結果、`joiner` というオブジェクトがクラスであることが分かった。これを用いれば、`{{joiner.__init__.__globals__.__builtins__.eval(request.arg.q)}}` といった形で任意コード実行ができるはずである。このままでは文字数が長すぎるため、`config.__setitem__` を用いて式の途中経過を逐次保存することで制限をバイパスした。。

[!details:スクリプト:(!src:solve.py:py)]
