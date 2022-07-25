---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: Ogre
genre: forensics
solved_date: 2022-07-17
during_ctf: true
tag: [docker]
fav: false
difficulty: easy
---

### 概要

ghcr.io/iciaran/ogre:ctf という Docker イメージが与えられる。

### 解法

まず、Docker イメージの生ファイルをローカルにダウンロードする。

```
docker save ghcr.io/iciaran/ogre:ctf -o ogre.tar
```

これを解凍すると、イメージを構築した操作のリストがある json がある。これを眺めると、`"RUN /bin/sh -c echo aWN0ZntvbmlvbnNfaGF2ZV9sYXllcnNfaW1hZ2VzX2hhdmVfbGF5ZXJzfQo= \u003e /tmp/secret # buildkit"` という怪しいコマンドを発見できる。これをデコードすればよい。
