### DESCRIPTION ###
# This is the "CLEAR" command module.
# Specifies the functionality for emptying the fridge and all of its storage history.


# Imports for DB #
from tinydb import TinyDB, Query

# Import for Flask response #
from flask import jsonify

#Declare DB and Query
fridge_db = TinyDB ('fridge_db.json') # DB to store fridge contents


def clear_fridge():
    fridge_db.purge()
    return jsonify (
        response_type="in_channel", 
        attachments = [
            {
             "fallback": "Fridge is emptied.",
             "color": "#025ff5", #Blue
             "text": "Fridge emptied!"
            }
        ]
    )