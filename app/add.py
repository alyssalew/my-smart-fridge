### DESCRIPTION ###
# This is the "ADD" command module.
# Specifies the functionality for updating (increasing) the quantity of an existing item, adding a new item.


# Imports for DB #
from tinydb import TinyDB, Query

# Import for Flask response #
from flask import jsonify

#Declare DB and Query
fridge_db = TinyDB ('fridge_db.json') # DB to store fridge contents
Food = Query()


def add_item (thing, quant, date, info):
    # Add an item that's already in the fridge
    if fridge_db.contains((Food.item == thing) & (Food.expire_date == date)):
        db_entry = fridge_db.search((Food.item == thing) & (Food.expire_date == date))
        db_quant= int(db_entry[0]['quantity'])
        new_quant = db_quant + int(quant)
        fridge_db.update ({'quantity': new_quant}, (Food.item == thing) & (Food.expire_date == date))
        return jsonify (
            response_type="in_channel", 
            attachments = [
                {
                 "fallback": "Updating to add an existing item.",
                 "pretext": "Added!",
                 "color": "ffda00", #Golden Yellow
                 "text": "Updated: " + str(new_quant)+ " " + thing
                }
            ]
        )           
    # Add a new item to the fridge
    else:
        fridge_db.insert(info)
        return jsonify (
            response_type="in_channel", 
            attachments = [
                {
                 "fallback": "Updating to add a new item.",
                 "pretext": "Added!",
                 "color": "#ffff00", #Yellow
                 "text": "Added: " + str(quant)+ " " + thing
                }
            ]
        )