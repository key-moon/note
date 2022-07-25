from pwn import *

REMOTE_ADDR = 'the-house-always-wins.chal.imaginaryctf.org'
REMOTE_PORT = 1337
LOCAL = False

find = process(["./find", "128", "8"])
find.recvuntil(b'LOAD\n', drop=True)
print(f'[+] loaded.')

stream = None
def reconnect():
  global stream
  if stream is not None: stream.close()
  if LOCAL: stream = process("./casino")
  else: stream = remote(REMOTE_ADDR, REMOTE_PORT)

def game(bet, choice):
  stream.sendlineafter(b'>>> ', str(bet).encode())
  stream.recvuntil(b'The first number is ')
  fst = int(stream.recvuntil(b'.', drop=True).decode())
  stream.sendlineafter(b'>>> ', str(choice).encode())
  stream.recvuntil(b'The second number is ')
  snd = int(stream.recvuntil(b'!', drop=True).decode())
  return (fst, snd)

def money():
  stream.recvuntil(b'Current money: ')
  return int(stream.recvline(keepends=False).decode())

while True:
  reconnect()
  v1, v2 = game(5, 1)
  v3, v4 = game(5, 1)
  find.sendline(f'{v1} {v2} {v3} {v4}'.encode())
  res = find.recvuntil(b'END\n', drop=True)
  if len(res) == 0: continue
  l = [*map(int, res.decode().strip().split())]
  for i in range(0, len(l), 2):
    fst, snd, m = l[i], l[i + 1], money()
    print(f'[+] {m=}')
    if 1000000000 <= m: break
    game(m if fst != snd else 5, 1 if fst < snd else 2) 
  stream.interactive()
  break
