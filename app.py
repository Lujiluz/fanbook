import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URL = os.environ.get('MONGODB_URL')
DB_NAME = os.environ.get('DB_NAME')

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]

app = Flask(__name__)

# endpoint for home
@app.route('/')
def home():
    return render_template('index.html')

# endpoint for post request
@app.route('/msg', methods=['POST'])
def post_comment():
    nickname = request.form['nickname']
    message = request.form['msg']
    num = db.fanbook.count_documents({}) + 1
    
    data = {
        'nickname': nickname,
        'comment': message,
        'num': num
    }
    
    db.fanbook.insert_one(data)
    return jsonify({'msg': 'comment posted!'})

# endpoint for get request
@app.route('/msg', methods=['GET'])
def get_comment():
    data = list(db.fanbook.find({}, {'_id': False}))
    return jsonify({
        'data': data
    })

# endpoint for delete request
@app.route('/msg', methods=['DELETE'])
def del_comment():
    data_num = request.form['num']
    db.fanbook.delete_one({'num': int(data_num)})
    return jsonify({'msg': 'comment deleted!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)