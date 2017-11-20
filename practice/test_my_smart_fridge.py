

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/testmysmartfridge', methods=['GET', 'POST'])
def test_my_smart_fridge():
##Parse necessary command parameters
	token = request.form.get('token', None)
	command = request.form.get('command', None)
	text = request.form.get('text', None)

	#if token == "mK3acodbHoF9Im3UwbIOtqUZ":
	if request.method == 'POST':
		return jsonify(
			response_type="in_channel", 
			text=text,
			)
	else:
		return "Hello, Alyssa! This is a GET request"