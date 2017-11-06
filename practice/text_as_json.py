from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/info', methods=['GET', 'POST'])
def get_info():
	if request.method == 'POST':
		#d = ["String1","String2"]
		d =  request.get_json()
		return jsonify(Success=d)
	else:
		return "Hello, Alyssa! This is a GET request"