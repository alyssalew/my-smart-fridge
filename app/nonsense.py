### DESCRIPTION ###
# This is the non-sense text module.
# Specifies the functionality for responding to a user who enters text that is undefined by the app.


# Import for Flask response #
from flask import jsonify

def non_sense_text():
    return jsonify (
        response_type="ephemeral", 
        text="*The fridge is not THAT smart!*"
    )