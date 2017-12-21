### DESCRIPTION ###
# This script provides the scheduling feature for expiration date notifications in Slack for the MySmartFridge app.
# It notifies users daily when an item in their fridge has expired (a prior date or the current date).
# It also lists items entered without an expiration date.


# Imports for scheudling #
import schedule
import time

# Import module #
import get_expired_items

def expired_notifications():
    get_expired_items.get_expired_items()


#******* Time based on timezone of server -- UTC  (A string in HH:MM format) *******#
    # UTC to PST    -08:00 hr
    # UTC to EST    -05:00 hr
    # UTC to CST    -06:00 hr

# Notify 9:00 am PST with server on UTC
schedule.every().day.at("17:00").do(expired_notifications)

while True:
    schedule.run_pending()
    time.sleep(1)