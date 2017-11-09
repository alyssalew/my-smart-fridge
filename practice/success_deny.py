from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
       return "Success"
    else:
        return "Hello, Alyssa! This is a GET request"