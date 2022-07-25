ps = [347, 331, 313, 307, 283, 277]

s = "ce10e59f40c8d954d9dad1ea81811a834d26580107149d16c3a769198fb158f0cb0e33dbd98f8dc8bb874105974b71719790b23c971736e8fe8ec88e8695"
m = 16**len(s)
res = mod(int(s, 16), m)

for p in ps[::-1]:
  res = (res - p) / (3**p)

print(int(res).to_bytes(len(s) // 2, "big"))
