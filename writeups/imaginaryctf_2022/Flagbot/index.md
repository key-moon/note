---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: Flagbot
genre: misc
solved_date: 2022-07-17
during_ctf: true
tag: [discord]
fav: false
difficulty: beginner
---

### 概要

Flagmaster というロールを持っている場合のみ Flag を送信する Discord Bot がある。

### 解法

自分が権限を持っているサーバーに招待し、自身に Flagmaster ロールを付与すればよい。招待は `https://discord.com/oauth2/authorize?client_id={id}&permissions={permissions_id}&scope=bot` で可能。
