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
[!details:詳細ルール:(!src:rule.txt:txt)]

### 解法

ゲーム木探索をすればよい。制約よりゲーム木のトポロジカル順序が定まっているため、月日の逆順で辿ると実装が楽である。ただ、存在しない月日でもお構いなく投げてくるため、月毎の最大日数などを考慮して実装すると足元を掬われる。さらに、たまに必勝手段のないものを投げてくる。なので、必勝手段がなくとも悪あがきをするような実装をしておく必要がある。
[!details:スクリプト:(!src:solve.py:py)]
