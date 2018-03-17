from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def boo_boo():
    return 'feuu'

@app.route('/hello')
def hello_world():
    return render_template('test.html')

