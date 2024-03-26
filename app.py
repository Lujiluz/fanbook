from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.gowux15.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

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
    app.run('0.0.0.0', port=5000, debug=True)