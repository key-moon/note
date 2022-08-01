---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: neoannophobia
genre: misc
solved_date: 2022-07-17
during_ctf: true
tag: [game]
fav: false
difficulty: easy
---

### 概要

21 を言ったら勝ちゲーム: カレンダーエディション
<details><summary>詳細ルール</summary>

```txt

```

</details>


### 解法

ゲーム木探索をすればよい。制約よりゲーム木のトポロジカル順序が定まっているため、月日の逆順で辿ると実装が楽である。ただ、存在しない月日でもお構いなく投げてくるため、月毎の最大日数などを考慮して実装すると足元を掬われる。さらに、たまに必勝手段のないものを投げてくる。なので、必勝手段がなくとも悪あがきをするような実装をしておく必要がある。
<details><summary>スクリプト</summary>

```py
from collections import deque
from datetime import datetime, timedelta
from pwn import *

REMOTE_ADDR = 'neoannophobia.chal.imaginaryctf.org'
REMOTE_PORT = 1337

stream = remote(REMOTE_ADDR, REMOTE_PORT)

months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
won = set([(12, 31)])

"""
def nxt_days(month, day):
  date = datetime(2022, month, day)
  for dday in range(1, 100):
    ndate = date + timedelta(dday)
    if ndate.month != month: break
    yield (ndate.month, ndate.day)
  for dmonth in range(1, 100):
    nmonth = month + dmonth
    if 12 < nmonth: break
    try:
      datetime(2022, nmonth, day)
    except ValueError:
      continue
    yield (nmonth, day)
"""

def nxt_days(month, day):
  for dday in range(1, 100):
    nday = day + dday
    if 31 < nday: break
    yield (month, nday)
  for dmonth in range(1, 100):
    nmonth = month + dmonth
    if 12 < nmonth: break
    yield (nmonth, day)


for month in range(1, 13)[::-1]:
  for day in range(1, 31)[::-1]:
    won.add((month, day))
    for nxt in nxt_days(month, day):
      if nxt in won:
        won.remove((month, day))

print(won)

for i in range(100):
  stream.recvuntil(b"----------\n")
  print(stream.recvline())
  stream.recvuntil(b"----------\n")
  while True:
    l = stream.recvline().decode().strip()
    month_s, day_s = l.split(' ')
    month = months.index(month_s)
    day = int(day_s)
    print(f'{month} {day}')
    nxts = [nxt for nxt in nxt_days(month, day) if nxt in won]
    if len(nxts) == 0:
      print(f'[!] valid strategy not found.')
      nxts = [next(nxt_days(month, day))]
    nmonth, nday = nxts[-1]
    print(f'> {nmonth} {nday}')
    stream.sendlineafter(b'> ', f'{months[nmonth]} {nday}'.encode())
    if (nmonth, nday) == (12, 31): break


stream.interactive()
```

</details>

