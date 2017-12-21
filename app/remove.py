### DESCRIPTION ###
# This is the "REMOVE" command module.
# Specifies the functionality for removing all of a given item, updating (decreasing) the quantity of an item,
# trying to remove an item not in the fridge.

# Imports for DB #
from tinydb import TinyDB, Query

# Import for Flask response #
from flask import jsonify

#Declare DB and Query
fridge_db = TinyDB ('fridge_db.json') # DB to store fridge contents
Food = Query()


def remove_item (thing, quant, date):
    if fridge_db.contains (Food.item == thing):
        #Remove all of an item with a given date or all of an item with no expiration date
        if quant == "all":
            if date != "none":
                fridge_db.update ({'quantity': 0}, (Food.item == thing) & (Food.expire_date == date))
                return jsonify (
                    response_type="in_channel", 
                    attachments = [
                        {
                         "fallback": "Remove all of an item with a certain date.",
                         "color": "FF6600", #Red-Orange
                         "text": "Removed all " + thing + " with the expiration date " + "*" + date + "*" + " from your fridge!",
                         "mrkdwn_in": ["text"]
                        }
                    ]
                )     
            else:
                fridge_db.update ({'quantity': 0}, (Food.item == thing))
                return jsonify (
                    response_type="in_channel", 
                    attachments = [
                        {
                         "fallback": "Remove all of an item.",
                         "color": "#FF6103", #Cadmium Orange
                         "text": "Removed all " + thing + " from your fridge!"
                        }
                    ]
                )           
        #Remove a given quantity of an item
        else:
            db_entry = fridge_db.search((Food.item == thing) & (Food.expire_date == date))
            db_quant= int(db_entry[0]['quantity'])
            new_quant = db_quant - int(quant)
            fridge_db.update ({'quantity': new_quant}, (Food.item == thing) & (Food.expire_date == date))
            if new_quant <= 0:
                fridge_db.update ({'quantity': 0}, (Food.item == thing) & (Food.expire_date == date))
                return jsonify (
                response_type="in_channel", 
                attachments = [
                    {
                     "fallback": "Remove all of an item.",
                     "color": "#FF6103", #Cadmium Orange
                     "text": "Removed all " + thing + " from your fridge!"
                    }
                ]
            )      
        return jsonify (
            response_type="in_channel", 
            attachments = [
                {
                 "fallback": "Removing certain amount of item.",
                 "pretext": "Removed!",
                 "color": "warning", #Orange
                 "text": "Updated: " + str(new_quant)+ " " + thing
                }
            ]
        )        
    #Trying to remove an item that doesn't exist in the fridge
    else:
        return jsonify (
            response_type="in_channel", 
            attachments = [
                {
                 "fallback": "Item to be removed is not in fridge.",
                 "color": "danger", #Red
                 "text": "Sorry, " + thing + " is not in the fridge."
                }
            ]
        )