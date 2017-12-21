### DESCRIPTION ###
# This script builds out the Slack slash commands for the MySmartFridge slack app.
# This script initializes a Flask app, sets up the necessary databases.

# The majority of this script processes the information recieved from the user,
# calls the appropriate methods from imported modules,
# and responds in Slack for the user to view.


# Imports for DB #
from tinydb import TinyDB, Query

# Imports for FLask server #
from flask import Flask
from flask import request

# Import modules #
import add
import remove
import search
import clear
import helper
import nonsense

#Declare DBs
command_db = TinyDB ('command_db.json') #DB to store Slash command info received via POST Request from Slack
log_db = TinyDB ('log_db.json') #DB to store parsed command text

#Declare Flask app
app = Flask(__name__)
@app.route('/testmysmartfridge', methods=['GET', 'POST'])

def slash_command():
##Parse necessary command parameters
    token = request.form.get('token', None) 
    command = request.form.get('command', None)
    text = request.form.get('text', None)

    d = {'token': token, 'command': command, 'text': text}

    #Add commmnd info to database
    command_db.insert(d)

############################### Response to "POST" request #############################################
    if request.method == 'POST':   
#Parse the text from command
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
            
#Add grocery info to log database and assign labels
        log_db.insert(grocery_log)
        log_item = grocery_log.get('item')
        log_quant = grocery_log.get('quantity')
        log_date = grocery_log.get('expire_date')

#Calling modules based on command keyword

    #ADD COMMAND
        if grocery_log.get ('keyword') == 'add':
            return add.add_item(log_item, log_quant, log_date, grocery)

    #REMOVE COMMAND
        if grocery_log.get ('keyword') == 'remove':
            return remove.remove_item(log_item, log_quant, log_date)
    #SEARCH COMMAND
        if grocery_log.get ('keyword') == 'search':
           return search.search_fridge(log_quant)

    #CLEAR COMMAND
        if grocery_log.get ('keyword') == 'clear':
            return clear.clear_fridge()
            
    #HELP COMMAND
        if grocery_log.get ('keyword') == 'help':
            return helper.help_me()

    #NON-SENSE COMMAND
        if grocery_log.get('keyword') != 'add' or grocery_log.get('keyword') != 'remove' or grocery_log.get('keyword') != 'search' or  grocery_log.get('keyword') != 'clear' or grocery_log.get('keyword') == 'help':
            return nonsense.non_sense_text()


################################# Response to a "GET" request ####################################################
    else:
        return "Hello, Welcome to the MySmartFridge App! For more information visit: https://github.com/alyssalew/my-smart-fridge"

