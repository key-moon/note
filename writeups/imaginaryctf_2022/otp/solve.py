from collections import Counter
from pwn import *

REMOTE_ADDR = 'otp.chal.imaginaryctf.org'
REMOTE_PORT = 1337

stream = remote(REMOTE_ADDR, REMOTE_PORT)
l = None
for i in range(200):
  stream.sendline(b"FLAG")
  stream.recvuntil(b"flag: ")
  enc = stream.recvline(keepends=False)
  print(enc)
  if l is None: l = [Counter() for i in range(len(enc) * 4)]
  enc = int(enc, 16)
  for c in l:
    c[enc & 1] += 1
    enc //= 2

  print(f'[+] {i=}')
  res = ""
  for c in l[::-1]:
    res += str(1 ^ c.most_common(1)[0][0])

  print(int(res, 2).to_bytes(len(res) // 8, "little")[::-1])
