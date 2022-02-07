---
layout: chall
ctf_name: DiceCTF_2022
problem_name: flagle
genre: rev
solved_date: 2022-02-05
during_ctf: true
tag: [wasm, obfuscate]
---

### 概要

[wordle](https://wordle.wekele.com/) の顔をしたフラグチェッカー 裏は wasm で動いているらしい。

### 解法

wasm2c で C にトランスパイルした後にコンパイルして、ghidra などで気合で読む。押忍!

```sh
bin/wasm2c ../flag-checker.wasm -o ../flag-checker.c
gcc -O3 main.c flag-checker.c wasm-rt-impl.c
```

wasm2c は -o オプションで吐き出し先を指定しないと変な依存関係が必要になるので注意。
