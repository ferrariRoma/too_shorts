# mongoDB
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
# .env
from dotenv import load_dotenv
import os
# 크롤링
import requests
from bs4 import BeautifulSoup
import certifi
import jwt
import datetime
import hashlib

# Flask
app = Flask(__name__)
# .env
load_dotenv()
DB_URL = os.environ.get('DB_URL')
# SECRET_KEY .env에 추가
SECRET_KEY = os.environ.get('SECRET_KEY')

client = MongoClient(DB_URL, tlsCAFile=certifi.where())
db = client.dbtooshorts

# home handler
@app.route('/')
def home():
    # 토큰이 있을 때 nickname을 넘겨줌
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    # 토큰이 없을 때 그냥 index.html렌더링
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

# login page rendering
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# signup page rendering
@app.route('/register')
def register():
    return render_template('register.html')

# signup post handler
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    nickname_receive = request.form['nickname_give']
    pw_receive = request.form['pw_give']
    checked_pw_receive = request.form['checked_pw_give']

    # 예외처리1: Id중복
    checked_id = db.user.find_one({'id': id_receive})
    if checked_id is not None:
        return jsonify({'msg': '이미 존재하는 ID입니다.'})

    # 예외처리2: PW불일치
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    checked_pw_hash = hashlib.sha256(checked_pw_receive.encode('utf-8')).hexdigest()
    if pw_hash!=checked_pw_hash:
        return jsonify({'msg': 'PW가 일치하지 않습니다.'})

    # 예외처리3: Username중복
    checked_nickname = db.user.find_one({'id': nickname_receive})
    if checked_nickname is not None:
        return jsonify({'msg': '이미 존재하는 Username 입니다.'})

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})
    return jsonify({'result': 'success'})

# [로그인 API]
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입과 같은 방법으로 pw를 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # 해당 유저 탐색
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    # 찾으면 JWT 토큰을 만들어 발급
    if result is None:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    payload = {
        'id': id_receive,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*24),
        'username': result['nick']
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # token을 줍니다.
    return jsonify({'result': 'success', 'token': token})        

# posting rendering
@app.route('/posting')
def posting():
    return render_template("posting.html")


# [포스팅 API]
# 프론트에서 shorts URL, description을 받아오고, 크롤링으로 받아온 title과 next_id, username을 DB에 저장
@app.route('/api/posting', methods=['POST'])
def submit_posting():
    temp_title = "tempTitle"
    # 프론트에서 body로 받아오는 데이터
    url_receive = request.form['URL']
    desc_receive = request.form['description']
    username_receive = request.form['username']

    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')

    # 크롤링(bs4)를 사용하기 위한 작업
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 크롤링하여 shorts의 title을 받아옴
    # title = soup.select('#overlay > ytd-reel-player-header-renderer > h2 > yt-formatted-string')[0]

    # payload 추출
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    all_posting = list(db.postings.find({}, {'_id': False}))
    next_id = len(all_posting) + 1
    doc = {
        "id": next_id,
        "username": username_receive,
        "title": temp_title,
        "description": desc_receive,
        "URL": url_receive
    }

    db.postings.insert_one(doc)
    return jsonify({'msg': "성공!!"})


# 토큰이 필요한 작업을 하는데 토큰이 만료되어 있으면 아래(try-except문) 코드를 쓰면 될 거 같음
# try:
#     # token을 시크릿키로 디코딩합니다.
#     # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
#     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#     print(payload)

#     # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
#     # 여기에선 그 예로 닉네임을 보내주겠습니다.
#     userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
#     return jsonify({'result': 'success', 'nickname': userinfo['nick']})
# except jwt.ExpiredSignatureError:
#     # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
#     return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
# except jwt.exceptions.DecodeError:
#     return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)