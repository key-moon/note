---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: secure_encoding_hex
genre: crypto
solved_date: 2022-07-16
during_ctf: true
tag: [decode, randomized]
fav: false
difficulty: beginner
---

### 概要

hex された文字列 flag の hex が置換されて与えられる。

```py
#!/usr/bin/env python3

from random import shuffle

charset = '0123456789abcdef'
shuffled = [i for i in charset]
shuffle(shuffled)

d = {charset[i]:v for(i,v)in enumerate(shuffled)}

pt = open("flag.txt").read()
assert all(ord(i)<128 for i in pt)

ct = ''.join(d[i] for i in pt.encode().hex())
f = open('out.txt', 'w')
f.write(ct)
```

```txt
0d0b18001e060d090d1802131dcf011302080ccf0c070b0f080d0701cf00181116
```


### 解法
ascii 及び英単語の制約を元に、替字表を手作業で復元した。

```py
charset = '0123456789abcdef'

known = {
  " ": "0",
  "2": "1", # temp
  "3": "2", # temp
  "b": "3",
  "8": "4",
  "c": "5",
  "0": "6",
  "1": "7",
  " ": "8",
  "d": "9",
  " ": "a",
  "e": "b",
  "9": "c",
  "6": "d",
  "7": "e",
  "f": "f",
}

print(set(charset) - set(known.keys()))

def conv(c):
  h = hex(c)[2:].zfill(2)
  return ''.join([known[b] for b in h]) if all(b in known for b in h) else h

s = open("out.txt", "r").read()
print(bytes.fromhex(''.join(map(conv, bytes.fromhex(s)))))
```

