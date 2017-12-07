### DESCRIPTION ###
# This script provides the scheduling feature for expiration date notifications in Slack for the MySmartFridge app.
# It notifies users daily when an item in their fridge is expired (a prior date or the current date)
# It also lists inventoried items entered without a date.


import requests

# Imports for scheudling #
import schedule
import time
import datetime

# Imports for DB #
from tinydb import TinyDB, Query
fridge_db = TinyDB ('fridge_db.json')

webhook_URL = 'https://hooks.slack.com/services/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'

# Get and define current date
now=datetime.datetime.now()
now_day = now.day
now_month = now.month
now_year = now.year


def check_expire_date():
    expired_list = []
    no_date_list = []
    i = 1
    while i <= len(fridge_db):
        db_entry = fridge_db.get(doc_id = i)
        if db_entry['quantity'] != 0:   #Doesn't notify about "removed" items
            if db_entry['expire_date'] != 'none':
                exp_date_array = db_entry['expire_date'].split ("-")
                db_month = int(exp_date_array [0])
                db_day = int(exp_date_array [1])
                db_year = int('20'+ exp_date_array [2])
                if db_year <= now_year:     #Gets date earier than current date
                    if db_month < now_month:
                        expired_list.append (db_entry['item']+ ": *_Expired_* ~ Expiration Date: " + "*"+ db_entry['expire_date'] +"*" + "\n")
                    if db_month == now_month:
                        if db_day <= now_day:
                            expired_list.append (db_entry['item']+ ": *_Expired_* ~ Expiration Date: " + "*"+ db_entry['expire_date'] +"*" + "\n")
                expired_str =''.join (expired_list)
            else:
                no_date_list.append (db_entry['item'] + ": No expiration date\n")
                no_date_str =''.join(no_date_list)
        i = i+1

    payload= {
        'attachments':[
            #Attachment for expired items
            {
             "fallback": "Expiration notification - Expired items.",
             "pretext": "*NOTIFICATION*",
             "color": "#ff69b4", #Pink
             "text": expired_str,
             "mrkdwn_in": ["text","pretext"]
            },
            #Attachment for items with no expiration date
            {
             "fallback": "Expiration notification - No Date Item.",
             "text": no_date_str
            }
        ]
    }

    r = requests.post(webhook_URL, json=payload)


#******* Time based on timezone of server -- UTC  (A string in HH:MM format) *******#
    # UTC to PST    -08:00 hr
    # UTC to EST    -05:00 hr
    # UTC to CST    -06:00 hr

# Notify 9:00 am PST with server on UTC
schedule.every().day.at("17:00").do(check_expire_date)

while True:
    schedule.run_pending()
    time.sleep(1)