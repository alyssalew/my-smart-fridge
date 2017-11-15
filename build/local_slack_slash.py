from tinydb import TinyDB, Query

from flask import Flask
from flask import request
from flask import jsonify

command_db = TinyDB ('command_db.json')
log_db = TinyDB ('log_db.json')
fridge_db = TinyDB ('fridge_db.json')

app = Flask(__name__)

@app.route('/fridge-slash', methods=['POST'])

def slash_command():
##Parse necessary command parameters
    token = request.form.get('token', None) 
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    
    d = {'token': token, 'command': command, 'text': text}

#Add commmnd info to database
    command_db.insert(d)   

##Parse the text from command
    text_array = text.split()
    grocery_log = {}
    grocery = {}
    labels = ['keyword','quantity', 'item', 'expire_date']
    if len(text_array) == 3:
    	text_array.append ("none")
    for i in range(len(text_array)):
        grocery_log[labels[i]] = text_array [i]
        if labels[i] != 'keyword':
        	grocery[labels[i]] = text_array [i]
            
#Add grocery info to database
    log_db.insert(grocery_log)
    fridge_db.insert(grocery)

    return jsonify(InsideTheFridge=fridge_db.all())
			

    





