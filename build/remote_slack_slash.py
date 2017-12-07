### DESCRIPTION ###
# This script builds out the Slack slash commands for the MySmartFridge slack app.
# This script initializes a Flask app, setup the necessary databases
# The majority of this script defines the functionality of the Slack commands, processes the information recieved from the user,
# and sends a response back to Slack for the user to view.


# Imports for DB #
from tinydb import TinyDB, Query

# Imports for FLask server #
from flask import Flask
from flask import request
from flask import jsonify

#Declare DBs
command_db = TinyDB ('command_db.json') #DB to store Slash command info received via POST Request from Slack
log_db = TinyDB ('log_db.json') #DB to store parsed command text
fridge_db = TinyDB ('fridge_db.json') # DB to store fridge contents

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

#Define a database query variable
        Food = Query()

#Define functions based on commands

        def add_item ():
            # Add an item that's already in the fridge
            if fridge_db.contains((Food.item == log_item) & (Food.expire_date == log_date)):
                db_entry = fridge_db.search((Food.item == log_item) & (Food.expire_date == log_date))
                db_quant= int(db_entry[0]['quantity'])
                new_quant = db_quant + int(log_quant)
                fridge_db.update ({'quantity': new_quant}, (Food.item == log_item) & (Food.expire_date == log_date))
                return jsonify (
                    response_type="in_channel", 
                    attachments = [
                        {
                         "fallback": "Updating to add an existing item.",
                         "pretext": "Added!",
                         "color": "ffda00", #Golden Yellow
                         "text": "Updated: " + str(new_quant)+ " " + log_item
                        }
                    ]
                )           
            # Add a new item to the fridge
            else:
                fridge_db.insert(grocery)
                return jsonify (
                    response_type="in_channel", 
                    attachments = [
                        {
                         "fallback": "Updating to add a new item.",
                         "pretext": "Added!",
                         "color": "#ffff00", #Yellow
                         "text": "Added: " + str(log_quant)+ " " + log_item
                        }
                    ]
                )

        def remove_item ():
            if fridge_db.contains (Food.item == log_item):
                #Remove all of an item with a given date or all of an item with no expiration date
                if log_quant == "all":
                    if log_date != "none":
                        fridge_db.update ({'quantity': 0}, (Food.item == log_item) & (Food.expire_date == log_date))
                        return jsonify (
                            response_type="in_channel", 
                            attachments = [
                                {
                                 "fallback": "Remove all of an item with a certain date.",
                                 "color": "FF6600", #Red-Orange
                                 "text": "Removed all " + log_item + " with the expiration date " + "*" + log_date + "*" + " from your fridge!",
                                 "mrkdwn_in": ["text"]
                                }
                            ]
                        )     
                    else:
                        fridge_db.update ({'quantity': 0}, (Food.item == log_item))
                        return jsonify (
                            response_type="in_channel", 
                            attachments = [
                                {
                                 "fallback": "Remove all of an item.",
                                 "color": "#FF6103", #Cadmium Orange
                                 "text": "Removed all " + log_item + " from your fridge!"
                                }
                            ]
                        )           
                #Remove a given quantity of an item
                else:
                    db_entry = fridge_db.search((Food.item == log_item) & (Food.expire_date == log_date))
                    db_quant= int(db_entry[0]['quantity'])
                    new_quant = db_quant - int(log_quant)
                    fridge_db.update ({'quantity': new_quant}, (Food.item == log_item) & (Food.expire_date == log_date))
                    if new_quant <= 0:
                        fridge_db.update ({'quantity': 0}, (Food.item == log_item) & (Food.expire_date == log_date))
                        return jsonify (
                        response_type="in_channel", 
                        attachments = [
                            {
                             "fallback": "Remove all of an item.",
                             "color": "#FF6103", #Cadmium Orange
                             "text": "Removed all " + log_item + " from your fridge!"
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
                         "text": "Updated: " + str(new_quant)+ " " + log_item
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
                         "text": "Sorry, " + log_item + " is not in the fridge."
                        }
                    ]
                )

        def search_fridge ():
            #Search and show all contents in fridge
            if log_quant == "all":
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
            elif fridge_db.contains ((Food.item == log_quant) & (Food.quantity > 0)): #Use 'log_quant' and 'log_item' since the "search" command only uses 3 arguments
                db_entry_item = fridge_db.search(Food.item == log_quant)
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
                             "text":"Yes, you have " + log_quant + "!",
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
                         "text": "Oh no, " + log_quant + " is not in the fridge!"
                        }
                    ]
                )

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

        def help_me():
            return jsonify (
                response_type="ephemeral",
                text="How to use */testmysmartfridge*",
                attachments = [
                    {
                     "fallback": "Help with using /testmysmartfridge 'ADD' command",
                     "text": "To track new items or increase the quantity of an existing item in the fridge, use:`/testmysmartfridge add`",
                     "mrkdwn_in": ["text"]
                    },
                    {
                     "fallback": "Help with using /testmysmartfridge 'REMOVE' command",
                     "text": "To decrease the quantity of items in the fridge, use:`/testmysmartfridge remove`",
                     "mrkdwn_in": ["text"]
                    },
                    {
                     "fallback": "Help with using /testmysmartfridge 'SEARCH' command",
                     "text": "To search your fridge for a specific item or its contents, use:`/testmysmartfridge search`",
                     "mrkdwn_in": ["text"]
                    },
                    {
                     "fallback": "Help with using /testmysmartfridge 'CLEAR' command",
                     "text": "To clear your fridge of ALL of the its tracked contents, use:`/testmysmartfridge clear`",
                     "mrkdwn_in": ["text"]
                    },

                    {
                     "fallback": "Help with using /testmysmartfridge 'HELP' command",
                     "text": "You are super smart and already found this... but to access all of this info (again), use:`/testmysmartfridge help`",
                     "mrkdwn_in": ["text"]
                    },
                    {
                     "fallback": "Link to 'README' for additional help with using /testmysmartfridge ",
                     "text": "_*For additional and more detailed help please see our <https://github.com/alyssalew/my-smart-fridge|README>*_",
                     "mrkdwn_in": ["text"]
                    }
                ]
            )

        def non_sense_text():
            return jsonify (
                response_type="ephemeral", 
                text="*The fridge is not THAT smart!*"
            )

#Calling functions based on command keyword

    #ADD COMMAND
        if grocery_log.get ('keyword') == 'add':
            return add_item()

    #REMOVE COMMAND
        if grocery_log.get ('keyword') == 'remove':
            return remove_item()
    #SEARCH COMMAND
        if grocery_log.get ('keyword') == 'search':
           return search_fridge()

    #CLEAR COMMAND
        if grocery_log.get ('keyword') == 'clear':
            return clear_fridge()
            
    #HELP COMMAND
        if grocery_log.get ('keyword') == 'help':
            return help_me()

    #NON-SENSE COMMAND
        if grocery_log.get('keyword') != 'add' or grocery_log.get('keyword') != 'remove' or grocery_log.get('keyword') != 'search' or  grocery_log.get('keyword') != 'clear' or grocery_log.get('keyword') == 'help':
            return non_sense_text()


################################# Response to a "GET" request ####################################################
    else:
        return "Hello, Welcome to the MySmartFridge App! For more information visit: https://github.com/alyssalew/my-smart-fridge"

