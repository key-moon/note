---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: Jormungandr
genre: rev
solved_date: 2022-07-18
during_ctf: true
tag: [python]
fav: false
difficulty: easy
---

### 概要

python のフラグチェッカーが与えられる。

<details><summary>コード</summary>

```py
find=lambda v:(i:=0,len([(i:=i+1)for(c)in(iter(lambda:text[i].startswith(v), True))]))[1]

def p(N):
    Enter =1
    prime=2# flag
    while Enter<N:
        prime+=(1+prime%2)
        s =prime%N
        for( hile)in range(3, prime,int( hex (2),16)):# salt
            if( prime%hile)==0 : break
            j__f = prime
        else:
            Enter+=1
    return(prime)

text=open( __file__).read().split()

try:
    while False:0
    while 1:
        {**{chr(i):lambda:0for(i)in range(32,127)},**{
            'l':lambda:text.insert(find(text[0][1:])+1,input()),
            's':lambda:text.append(text.pop(0)),
            'd':lambda:(text.pop(),text.pop()),
            'w':lambda:(text.pop(find(text[0][1:])+1),text.insert(find(text[0][1:])+1,text[1])),
            'i':lambda:(b:=text[1],text.pop(1),text.insert(1,('{:0%dx}'%(len(b))).format((int(b[:len(b)],16)*(3**p(len(text)))+p(len(text)))%16**(len(b)))),text.append(text.pop(0))),# lit
            'q':lambda:[text.pop()for( d)in iter(int,1)],
            'j':lambda:( chile :=text[0][1:],[text.append(text.pop(0))for(i)in(iter(lambda:text[0].startswith(chile),True))]),'p':lambda:print(text[1],end=' j__f '*0),# kite ce10e59f40c8d954d9dad1ea81811a834d26580107149d16c3a769198fb158f0cb0e33dbd98f8dc8bb874105974b71719790b23c971736e8fe8ec88e8695 p
            'not' :lambda: print(' bad... '),
            'c':lambda:text.append(text.pop(0))if text[find(text[0][1:])+1][1]==text[1][0]else[text.append(text.pop(0))for(i)in' q'],
            'k':lambda:text.append(text.pop(0))if text[find(text[0][1:])+1]==text[1]else[text.append(text.pop(0))for(i)in' q'],
        }
        }[text[0][0]]()
        text.append(text.pop(0))
except:
    pass
```

</details>


### 解法

コードを眺めると自分のコードを読み取って、それを独自形式として解釈して実行するインタプリタのような挙動をしていることが分かった。難読化を解除する際にファイルをいじると動かなくなることが想定されるので、スクリプトを別のファイルにコピーした上で、`open(__FILE__)` として指定されているファイル名を別のファイルの名前に書き換えた。こうして解析を進めると、以下のようなスクリプトでフラグを復元できることが分かった。
```py
ps = [347, 331, 313, 307, 283, 277]

s = "ce10e59f40c8d954d9dad1ea81811a834d26580107149d16c3a769198fb158f0cb0e33dbd98f8dc8bb874105974b71719790b23c971736e8fe8ec88e8695"
m = 16**len(s)
res = mod(int(s, 16), m)

for p in ps[::-1]:
  res = (res - p) / (3**p)

print(int(res).to_bytes(len(s) // 2, "big"))
```

