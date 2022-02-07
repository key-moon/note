---
layout: chall
ctf_name: DiceCTF_2022
problem_name: knock-knock
genre: crypto
solved_date: 2022-02-05
during_ctf: true
tag: [node, hash, warmup]
---

### 概要

ノート投稿のサービス。各ノートを閲覧するためには生成時に渡されるランダムな token が必要。flag は最初の投稿にある。

[!details:コード:(!src:chall.js:js)]

### 解法

以下に注目する。`crypto.randomUUID` は関数なので、 ```secret-${crypto.randomUUID}``` はランダムな文字列とはならない。

```js
class Database {
  constructor() {
    this.notes = [];
    this.secret = `secret-${crypto.randomUUID}`;
  }
// ...
}
```

よって、FLAG のある note の token は一意となる。
