import schedule
import time

def job ():
	print "Job is working..."

schedule.every(1).second.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

