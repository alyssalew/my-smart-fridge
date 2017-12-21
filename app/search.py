### DESCRIPTION ###
# This is the "SEARCH" command module.
# Specifies the functionality for searching for all current contents of the fridge,
# finding a specific item, trying to search for an item not found in the fridge.


# Imports for DB #
from tinydb import TinyDB, Query

# Import for Flask response #
from flask import jsonify

#Declare DB and Query
fridge_db = TinyDB ('fridge_db.json') # DB to store fridge contents
Food = Query()

def search_fridge (quant):
#Search and show all contents in fridge
	if quant == "all":
	    fridge_list_str = ""
	    i = 1
	    while i <= len(fridge_db):
	        item_list = []
	        db_entry = fridge_db.get(doc_id = i)
	        if db_entry['quantity'] != 0: #Search to show non-zero items
	            db_entry_item = str(db_entry['item'])
	            item_list.append (db_entry_item)
	            db_entry_item_quant = str(db_entry['quantity'])
	            item_list.append (db_entry_item_quant)
	            db_entry_item_expire = str(db_entry['expire_date'])
	            item_list.append (db_entry_item_expire)

	            fridge_list_str += str(item_list) + "\n"

	        i = i+1

	    return jsonify (
	        response_type="in_channel",
	        attachments = [
	            {
	            "fallback": "A listing of the fridge contents.",
	            "pretext": "*Fridge Contents:*\n_[ Item, Quantity, Expiration Date ]_",
	            "color": "#590088", #Purple
	            "text": fridge_list_str,
	            "mrkdwn_in": ["pretext"]
	            }
	        ]
	    )
	#Search for a given item in the fridge
	elif fridge_db.contains ((Food.item == quant) & (Food.quantity > 0)): #Use 'quantity' varibale since the "search" command only uses 3 arguments
	    db_entry_item = fridge_db.search(Food.item == quant)
	    item_match_quant = ""
	    item_match_date = ""
	    for item_match in range (len(db_entry_item)):
	        if db_entry_item [item_match]['quantity'] != 0: #Search display non-zero items
	            db_entry_item_quant = str(db_entry_item [item_match]['quantity'])
	            db_entry_item_expire = str(db_entry_item [item_match]['expire_date'])
	            item_match_quant += db_entry_item_quant + "\n"
	            item_match_date  += db_entry_item_expire + "\n "

	    return jsonify (
	            response_type="in_channel",
	            attachments = [
	                {
	                 "fallback": "Item searched is in fridge.",
	                 "color": "good", #Green
	                 "text":"Yes, you have " + quant + "!",
	                 "fields":[
	                    {
	                    "title": "Amount",
	                    "value": item_match_quant,
	                    "short": True
	                    },
	                    {
	                    "title": "Expiration Date",
	                    "value": item_match_date,
	                    "short": True 
	                    }
	                ]
	                }
	            ] 
	        )
	#Searched item is not in fridge
	else:
	    return jsonify (
	        response_type="in_channel", 
	         attachments = [
	            {
	             "fallback": "Item searched is not in fridge.",
	             "color": "danger", #Red
	             "text": "Oh no, " + quant + " is not in the fridge!"
	            }
	        ]
	    )