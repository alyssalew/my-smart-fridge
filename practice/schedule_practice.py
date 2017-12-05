import schedule
import time

def job ():
	print "Job is working... 6:30pm"

schedule.every().day.at("18:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

