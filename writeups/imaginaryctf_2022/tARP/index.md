---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: tARP
genre: forensics
solved_date: 2022-07-18
during_ctf: true
tag: [pcap]
fav: false
difficulty: easy
---

### 概要

パケットキャプチャが与えられる。

### 解法

問題名から ARP が怪しいと考え ARP リクエストに絞り込むと、探索する IP アドレスでファイルを送信していることが分かった。これをまとめるとフラグが記された画像ファイルになった。
