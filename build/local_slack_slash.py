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

    Food = Query()
    log_item = grocery_log.get('item')
    log_quant = grocery_log.get('quantity')
    log_date = grocery_log.get('expire_date')

#ADD COMMAND
    if grocery_log.get ('keyword') == 'add':
        if fridge_db.contains (Food.item == log_item) & fridge_db.contains (Food.expire_date == log_date):
            db_entry = fridge_db.search((Food.item == log_item) & (Food.expire_date == log_date))
            db_quant= int(db_entry[0]['quantity'])
            new_quant = db_quant + int(log_quant)
            fridge_db.update ({'quantity': new_quant}, (Food.item == log_item) & (Food.expire_date == log_date))
            return jsonify (Updated=fridge_db.all())
     
        else:
            fridge_db.insert(grocery)
            return jsonify (Added=fridge_db.all())
			
#REMOVE COMMAND
    if grocery_log.get ('keyword') == 'remove':
        if fridge_db.contains (Food.item == log_item):
            if log_quant == "all":
                fridge_db.remove ((Food.item == log_item) & (Food.expire_date == log_date))
            else:
                db_entry = fridge_db.search((Food.item == log_item) & (Food.expire_date == log_date))
                db_quant= int(db_entry[0]['quantity'])
                new_quant = db_quant - int(log_quant)
                fridge_db.update ({'quantity': new_quant}, (Food.item == log_item) & (Food.expire_date == log_date))
                if new_quant <= 0:
                    fridge_db.remove ((Food.item == log_item) & (Food.expire_date == log_date))
            return jsonify (Updated=fridge_db.all())
        else:
            return jsonify ("Sorry, " + log_item + " is not in the fridge.")

#SEARCH COMMAND
    if grocery_log.get ('keyword') == 'search':
        if log_quant == "all":
            return jsonify (fridge_db.all())
        elif fridge_db.contains (Food.item == log_quant): #Use 'log_quant' since the "search" command only uses 2 arguments
            db_entry_item = fridge_db.search(Food.item == log_quant)
            return jsonify ("Yes, you have " + log_quant + ":" , db_entry_item)
        else:
            return jsonify ("Oh no, " + log_quant + " is not in the fridge!")

#CLEAR COMMAND
    if grocery_log.get ('keyword') == 'clear':
        fridge_db.purge()
        return jsonify ("Fridge emptied!")
