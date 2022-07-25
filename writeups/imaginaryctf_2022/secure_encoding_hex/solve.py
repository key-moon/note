charset = '0123456789abcdef'

known = {
  " ": "0",
  "2": "1", # temp
  "3": "2", # temp
  "b": "3",
  "8": "4",
  "c": "5",
  "0": "6",
  "1": "7",
  " ": "8",
  "d": "9",
  " ": "a",
  "e": "b",
  "9": "c",
  "6": "d",
  "7": "e",
  "f": "f",
}

print(set(charset) - set(known.keys()))

def conv(c):
  h = hex(c)[2:].zfill(2)
  return ''.join([known[b] for b in h]) if all(b in known for b in h) else h

s = open("out.txt", "r").read()
print(bytes.fromhex(''.join(map(conv, bytes.fromhex(s)))))
