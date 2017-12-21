### DESCRIPTION ###
# This is the "HELP" command module.
# Specifies the functionality for providing help text to the user.


# Import for Flask response #
from flask import jsonify

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