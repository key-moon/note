s = open("emojis.txt").read()
print((int("".join(['0' if c == '👎' else '1' for c in s]), 2)).to_bytes(50, "big"))
