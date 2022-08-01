---
layout: chall
ctf_name: TetCTF 2022
problem_name: 2X-Service
genre: web
solved_date: 2022-01-04
during_ctf: false
tag: [xml, procfs]
---

### 概要

XML をパースし、 xpath で指定したノードを出力するサービスが与えられる。本質部分はおおよそ以下の通り。

```py
app.config['SECRET_KEY'] = XXXXXXXSECRETXXXXXXXX

xml = input()
if "text" in xml.lower(): exit()
res = ''
root = ElementTree.fromstring()
ElementInclude.include(root)
for elem in root.findall(input()):
    if elem.text != "":
        res += elem.text + ", "
print('result', res[:-2])
```

<details><summary>コード</summary>

```c
import random
import os
from flask import Flask, render_template, render_template_string, url_for, redirect, request
from flask_socketio import SocketIO, emit, send
from xml.etree import ElementTree, ElementInclude

app = Flask(__name__)
app.config['SECRET_KEY'] = XXXXXXXSECREKTXXXXXXXX
socketio = SocketIO(app)

@app.route('/')
def index():
	return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/source')
def source():
	return render_template('source.html')

@app.route('/about')
def about():
	return render_template('about.html')


@socketio.on('message')
def handle_message(xpath, xml):
	if len(xpath) != 0 and len(xml) != 0 and "text" not in xml.lower():
		try:
			res = ''
			root = ElementTree.fromstring(xml.strip())
			ElementInclude.include(root)
			for elem in root.findall(xpath):
				if elem.text != "":
					res += elem.text + ", "
			emit('result', res[:-2])
		except Exception as e:
			emit('result', 'Nani?')
	else:
		emit('result', 'Nani?')


@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8003)
```

</details>


### 解法

まず、`ElementInclude.include(root)` が[何をしているか](https://docs.python.org/ja/3/library/xml.etree.elementtree.html#xinclude-support)確認する。どうやら、特定のタグを用いることで外部の XML ファイルを読み込めるようだ。属性として `parse="text"` を指定するとパースをせずにテキストノードとして読み込んでくれる。サニタイジングは URL エンコードで回避可能である。
FLAG はソースファイルにあるようなので、以下のようにして app.py を読み込んだ。

```
<a xmlns:xi="http://www.w3.org/2001/XInclude"><b><xi:include href="app.py" parse="te&#120;t" /></b></a>
```

すると、秘匿されていた部分は

```
app.config['SECRET_KEY'] = os.environ.get('KEY')
```

であると分かった。環境変数は procfs の /proc/self/environ より読み出せるので、同様にこれを読み込めば良い。
