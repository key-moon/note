import subprocess

out = open("out.txt", "rb").read()
print(out)
print(2**(len(out) // 8 - 3))

last = int.from_bytes(out[-8:], "little") ^^ int.from_bytes(b'}\n', "little")
print(hex(last))
for key in mod(last, 2**64).nth_root(2**(len(out) // 8 - 1), all=True):
  print(key)
  subprocess.call(["./stream", "out.txt", str(key), "res.txt"])
  with open("res.txt", "rb") as f:
    res = f.read()
    if not res.startswith(b"ictf{"): continue
    print(res)
