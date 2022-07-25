---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: The House Always Wins
genre: rev
solved_date: 2022-07-19
during_ctf: true
tag: [rng,bruteforce]
fav: false
difficulty: easy
---

### 概要

期待値が正でない High-Low ゲームがリモートで動いている。一定以上お金を貯めれば勝ち。

### 解法

乱数の初期化処理では、urandom からとってきた 32 bit 整数で `srand` をした上で数万回程度乱数を消費していた。

```c
int set_seed_and_rand(uint seed) {
  int _i;
  srand(seed);
  _i = 0;
  while( 1 ) {
    int iVar1 = rand();
    if (iVar1 >> 0xf <= _i) break;
    rand();
    _i = _i + 1;
  }
  return rand() >> 0xf;
}
```

初期値との対応表を前計算することでシードのクラックをある程度高速化できそうである。2^32 個初期値を求めるのは時間がかかるため、2^28 個求めることにした。これは 8 コアのノート PC を用いて数分で行うことができた。

[!details:スクリプト:(!src:crack.c:c)]

次に、この対応表を用いてシードをクラックし、成功した場合は予測される乱数列を返すプログラムを書いた。前計算したテーブルをテキストファイルからメモリにロードする部分がボトルネックだったため、起動時に一括で読み込むようにした。

[!details:スクリプト:(!src:find.c:c)]

これを用いてリモートにつなぎ、フラグを取得するプログラムは以下の通り:

[!details:スクリプト:(!src:solve.py:py)]
