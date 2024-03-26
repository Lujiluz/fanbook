from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# endpoint for home
@app.route('/')
def home():
    return render_template('index.html')

# endpoint for post request