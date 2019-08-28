# MySmartFridge

MySmartFridge is a refrigerator management web application with Slack slash command integration. The application provides refrigerator contents tracking and food expiration date notifications. Since Slack is a multi-platform application, it gives you the ability to use MySmartFridge on your desktop or mobile device.

The application is written in Python and takes advantage of the capability to create your own Slack apps for integration into Slack workspaces and channels. MySmartFridge is built on receiving and responding to Slack slash commands in the form of HTTP POST requests and sends notifications to Slack as an incoming webhook.

## Prerequisites
 - Necessary downloads/installations (both locally and remotely for
   testing and deployment):
	- Python https://www.python.org/
	- Flask  http://flask.pocoo.org/
	- TinyDB  https://tinydb.readthedocs.io/
	- Requests  http://docs.python-requests.org/
	- Schedule  https://schedule.readthedocs.io/ 
 - AWS EC2 server or equivalent for remote hosting 
 - Slack account with admin permissions

## How to Use

 1. Clone the **mysmartfridge** repository into the desired directory on computer. All the files necessary for running the app can be found in the **"app"** directory in this repository.
 2. Setup EC2
     - Create an instance
     - In your instance security group setting make sure you allow all outbound traffic and set inbound to a port you want to use. These instructions use port range **5000** and source **0.0.0.0/0**
     - Find and note your public IP address for your instance
     - Configure your permissions to SSH onto your EC2 server
 3. Configure Slack for MySmartFridge
    - Create a new Slack app for your workspace. For detailed information and instructions visit Slack’s guides on [Slack Apps](https://api.slack.com/slack-apps). 
		 - You may want to create a new channel in your Slack workspace just for this Slack app
    - Under “Add features and functionality” select “Incoming Webhooks"
		 - Activate the feature, generate a webhook URL for the Slack channel with which you are integrating
		 - You will need this Webhook URL for your fridge notifications scheduler
    - Under “Add features and functionality” select “Slash Commands”
		 - Add a new command --- “***mysmartfridge***”
		 - For the “Request URL” field enter your public IP address at the port you configured (i.e. `http://xx.xxx.xx.x:5000/mysmartfridge`)
    - You may need to reinstall the Slack app after configuring the slash commands
    - By adding both Incoming Webhooks and Slack Slash Commands, your slack app should be installed in your workspace (verify that there is a check mark next to “Install your app to your workspace”)
 4. Configure *"get_expired_items.py"*
    - Set variable **webhook_URL** to the incoming webhook URL generated as part of the Slack setup process
 5. Deploy the **"app"** directory onto your EC2 server
    - My current version is deployed using `scp`
 6. SSH onto your server and run:
```
export FLASK_APP=slack_slash_commands.py
flask run --host=0.0.0.0

python expiration_date_notifications.py
``` 
You can run the Flask app and scheduler in the the background by using `nohup`
```
export FLASK_APP=slack_slash_commands.py
nohup flask run --host=0.0.0.0 &

nohup python expiration_date_notifications.py &

```
All outputs from Flask and the python file will by default be sent to *"nohup.out"*


7. To view and restart the app, SSH onto your server and view the processes currently running:
```
ps -fA 

#  Or find the one we care about:

ps -fA | grep python

# And kill the process for our Flask server by its PID:

kill <PID>
```
To restart go back to step 6.


## Available Commands

### [**ADD**] Adding new item to fridge
```
/mysmartfridge add <number> <item> <expiration_date>

/mysmartfridge add 5 apples 1-1-18
```
(`<expiration_date>` is an optional argument for command)

For items not yet in the fridge `add` adds the item and info (`<number>`, `<expiration_date>`) to the database

 - When items are entered with different expiration dates, the items   
   will be logged in the fridge separately.

Response: Message confirmation about the item and the quantity added

### [**ADD**] Adding more of an existing item to fridge
```
/mysmartfridge add <number> <item> <expiration_date>

/mysmartfridge add 5 apples 1-1-18
```
(`<expiration_date`> is an optional argument for command)

For items with the same expiration date already in the fridge `add` increases the number of the item in the fridge by the `<number>` entered

 - If the item already in the fridge has an expiration date specified, an `<expiration_date>` needs to be specified for subsequent additions.

Response: Message confirmation about the item and the updated quantity

### [**REMOVE**] Updating number of items in fridge from a removal
```
/mysmartfridge remove <number> <item> <expiration_date>

/mysmartfridge remove 2 apples 12-1-17 
/mysmartfridge remove 2 apples 
```
(`<expiration_date>` is an optional argument for command)

Updates the number remaining to reflect consumption

 - If an item has an expiration date, to remove it you must provide the
   `<expiration_date>`. 
 - If you have the same item but with different expiration dates, you
   will need to specify the item and its expiration date to remove it.
   
Response: Message confirmation about the item and the updated quantity

### [**REMOVE**] Updating number of items for finished/eaten item in fridge
```
/mysmartfridge remove all <item> <expiration_date>

/mysmartfridge remove all apples 12-1-17
/mysmartfridge remove all apples
```
(`<expiration_date>` is an optional argument for command)

Removes item (with expiration date) from fridge

 - If you want to remove all of an item with a given expiration date you
   must specify `<expiration_date>`
 - If you want to remove all of an item regardless of expiration date
   leave off `<expiration_date>`

Response: Message confirmation stating the removal all of an item with a `<expiration_date>` or all of an item

### [**SEARCH**] Find out what’s currently in your fridge
`/mysmartfridge search all`

Response: Message with list of all items currently in the fridge with their number remaining and expiration date

### [**SEARCH**] Find out if an item is currently in your fridge
```
/mysmartfridge search <item>

/mysmartfridge search apple
```
Searches fridge database for current contents that match the search `<item>`

Response:

 - When an `<item>` is in the fridge, responds with the number remaining
   and expiration date info.
 - When an `<item>` is not in the fridge, responds with “Sorry, `<item>`
   is not in the fridge.”
 - When there the `<item>`has with multiple expiration dates, responds
   with all logged items that matches entered `<item>`.

### [**CLEAR**] Remove all the contents of fridge
`/mysmartfridge clear`

Removes all the contents from the fridge

Response: “Fridge emptied”

### [**HELP**] Help with built-in Slack slash commands
`/mysmartfridge help`

Response: Provides brief help with the defined Slack slash commands. Links to this Github [README](my-smart-fridge/README.md) for more information.
 

## Additonal Resources
 - [Slash Commands](https://api.slack.com/slash-commands)
 - [Intro to Messages](https://api.slack.com/docs/messages)
 - [Message Formatting](https://api.slack.com/docs/message-formatting)
 - [Message Attachemnts](https://api.slack.com/docs/message-attachments)
 - [Message Builder](https://api.slack.com/docs/messages/builder)
 - [Incoming Webhooks](https://api.slack.com/incoming-webhook)
