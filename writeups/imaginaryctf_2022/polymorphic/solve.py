binary = open("polymorphic", "rb").read()

flag = False

res = ""

last = 0
while True:
  ind = binary.find(b'\x81\x35', last + 2) # xor [rip+0xXX], 0xXX
  if ind == -1: break
  off, arg = int.from_bytes(binary[ind+2:ind+6], "little"), int.from_bytes(binary[ind+6:ind+10], "little")
  if off == 0:
    # decoded instructions
    nxtins = int.from_bytes(binary[ind+10:ind+14], "little") ^ arg
    if flag and nxtins & 0xff == 0x2c: # sub al, 0xXX
      arg = nxtins >> 8 & 0xff
      res += chr((0x60 + arg) & 0xff)
      flag = False
    if nxtins & 0xffff == 0x602c:      # sub al, 0x60
      flag = True
  last = ind

print(res)
