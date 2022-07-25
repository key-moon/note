find=lambda v:(i:=0,len([(i:=i+1)for(c)in(iter(lambda:text[i].startswith(v), True))]))[1]

# nth_prime(1 indexed)
def p(N):
    Enter =1
    prime=2
    while Enter<N:
        prime+=(1+prime%2)
        s =prime%N
        for( hile)in range(3, prime,int( hex (2),16)):# salt
            if( prime%hile)==0 : break
            j__f = prime
        else:
            Enter+=1
    return(prime)

text=open("jormungandr.py").read().split()

try:
  while 1:
    table = {
      'd':lambda: (text.pop(),text.pop()),
      's':lambda: text.append(text.pop(0)),
      'q':lambda:[text.pop()for(d)in iter(int, 1)],

      'p':lambda:print(text[1],end=' j__f '*0),
      'l':lambda: text.insert(find(text[0][1:])+1,input()),
      'not': lambda: print(' bad... '),

      'i':lambda:(
        b:=text[1],
        print(f" |- {b=}, {('{:0%dx}'%(len(b)))=}"),
        text.pop(1),
        print(f" \- {p(len(text))=}"),
        text.insert(1, ('{:0%dx}'%(len(b))).format((int(b, 16) * (3**p(len(text))) + p(len(text))) % 16 ** (len(b)))),
        text.append(text.pop(0))
      ),

      'w':lambda:(text.pop(find(text[0][1:])+1),text.insert(find(text[0][1:])+1,text[1])),
      'j':lambda:( chile :=text[0][1:],[text.append(text.pop(0))for(i)in(iter(lambda:text[0].startswith(chile),True))]),
      'c':lambda:text.append(text.pop(0))if text[find(text[0][1:])+1][1]==text[1][0]else[text.append(text.pop(0))for(i)in' q'],
      'k':lambda:(
        print(f' \- {text[find(text[0][1:])+1]=}, {text[1]=}'),
        text.append(text.pop(0)) if text[find(text[0][1:])+1]==text[1] else[text.append(text.pop(0))for(i)in' q']
      ),
    }
    if text[0][0] in table:
      print(f'[+] {text[0][0]=}')
      table[text[0][0]]()
    text.append(text.pop(0))
except:
  pass
