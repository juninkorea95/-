from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# import requests
# from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.8y9lufi.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/food", methods=["POST"])
def food_post():
    name_receive = request.form['name_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    food_list = list(db.foodie.find({}, {'_id': False}))
    count = len(food_list) + 1

    doc = {
        'num': count,
        'name': name_receive,
        'url': url_receive,
        'star': star_receive,
        'comment': comment_receive
    }
    db.foodie.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

# @app.route("/movie/delete", methods=["POST"])
# def movie_delete():
#     num_receive = request.form['num_give']
#     db.movies.delete_one({'num': int(num_receive)})
#     return jsonify({'msg': '삭제 완료!'} s)

@app.route("/food", methods=["GET"])
def food_get():
    food_list = list(db.foodie.find({}, {'_id': False}))
    food_list.reverse()
    return jsonify({'foods': food_list})
# 회원 가입 / 로그인
@app.route('/signUp')
def signUp():
    return render_template('sigUp.html')
@app.route('/signIn')
def signIn():
    return render_template('sigIn.html')

@app.route('/signUp/give', methods=["POST"])
def signUpPost():
    idReceive = request.form["idGive"]
    nameReceive = request.form["nameGive"]
    passwordReceive = request.form["passwordGive"]

    hashedPassword = bcrypt.hashpw(passwordReceive.encode('utf-8'), bcrypt.gensalt())
    hashedPassword = hashedPassword.decode()

    doc = {
        'id': idReceive,
        'name': nameReceive,
        'password': hashedPassword
    }
    db.users.insert_one(doc)
    return jsonify({'msg': 'complete sign up!'})


@app.route('/signUp/check', methods=["GET"])
def signUpGet():
    userList = list(db.users.find({}, {'_id': False}))
    return jsonify({'users': userList})


@app.route('/signIn/give', methods=["POST"])
def signInGive():
    idReceive = request.form["idGive"]
    passwordReceive = request.form["passwordGive"]

    user = list(db.users.find({'id': idReceive}, {'_id': False}))
    if len(user) > 0 and bcrypt.checkpw(passwordReceive.encode('utf-8'), user[0]['password'].encode('utf-8')):
        doc = {
            'userId': user[0]['id'],
            'userName': user[0]['name']
        }
        return jsonify({'error': None, 'data': doc})
    else:
        return jsonify({'error': 'login-fail'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)