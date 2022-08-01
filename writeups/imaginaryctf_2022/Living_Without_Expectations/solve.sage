from progressbar import progressbar


with open("output.txt") as f:
  ls = f.readlines()

# "'0x...', '0x...', '0x...'"
def parse_arr(s):
  return [int(elem[3:-1], 16) for elem in s.split(', ')]

q = 2**142 + 217
n = 69

cs = []
for l in progressbar(ls):
  s = l.split('] [')
  assert len(s) == 2
  As, bs = s
  A, b = parse_arr(As[1:]), parse_arr(bs[:-2])
  A = matrix(ZZ, n, n, A)
  b = matrix(ZZ, b)
  cs.append((A, b))

SCALE = 10 ** 20
INF   = 10 ** 50
zs = [0]
block = [
  [*[cs[z][0].transpose() for z in zs], matrix.identity(n) * 2 * SCALE,        matrix(ZZ, n, 1)],
  [*[cs[z][1]             for z in zs],        matrix([1] * n) * SCALE, matrix(ZZ, 1, 1, [INF])],
  [             matrix.identity(n) * q,               matrix(ZZ, n, n),        matrix(ZZ, n, 1)]
]

mat = block_matrix(block)

for row in Matrix(ZZ, mat).LLL():
  if row[-1] == 0: continue
  print(f'[+] {row=}')
  s = matrix(Zmod(q), n, 1, [0 if 0 < elem else 1 for elem in row[n:][:n]])
  binary = ""
  for A, b in cs:
    diff_sum = sum(abs(b1 - b2) for b1, b2 in zip(matrix(ZZ, 1, n, (A * s).list()), b))
    binary += "0" if diff_sum <= 1000 else "1"
  print(f'[+] {binary=}')
  print(int(binary, 2).to_bytes(len(binary) // 8 + 1, "big"))
