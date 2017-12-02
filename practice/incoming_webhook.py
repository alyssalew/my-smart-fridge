import requests
import schedule
import time
import datetime


webhook_URL = 'https://hooks.slack.com/services/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'

now=datetime.datetime.now()
now_day = now.day
now_month = now.month
now_year = now.year


def expiration_checker():
	s = "11-1-17"  #(Eventually) Go through the expiration dates in db
	exp_date_array = s.split ("-")
	db_month = int(exp_date_array [0])
	db_day = int(exp_date_array [1])
	db_year = int('20'+ exp_date_array [2])

	def payload_not_exp():
	    payload = {
	        'attachments':[
	            {
	             "fallback": "Expiration notification.",
	             "pretext": "NOTIFICATION",
	             "text": "Your " + db_entry['item']+ " is not expired."
	            }
	        ]
	    }
	    r = requests.post(webhook_URL, json=payload)

	if db_year <= now_year:
		if db_month<= now_month:
			if db_day<=now_day: #Gets date earier than current date
				#def incoming_webhook():
				payload = {
					'attachments':[
				        {
				         "fallback": "Expiration notification.",
				         "pretext": "NOTIFICATION",
				         "color": "#ff69b4", #Pink
				         "text": "Your thing is expired. It expired  " + s
				        }
				    ]
				}
				r = requests.post(webhook_URL, json=payload)
					#print "webhook print"	
				

schedule.every(10).seconds.do(expiration_checker)

while True:
    schedule.run_pending()
    time.sleep(1)



#curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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