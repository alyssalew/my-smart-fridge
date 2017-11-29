import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig()

sched = BackgroundScheduler()

#@sched.scheduled_job('interval', seconds=10)
#def timed_job():
    #print('This job is run every 10 seconds.')

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
#def scheduled_job():
    #print('This job is run every weekday at 5pm.')

def job_func():
	print('This job is at 7:45pm.')



month = 11
day = 28
year = 2017

hour = 17
minute = 45

sched.add_job(job_func, trigger='cron', year= year, month= month, day= day, hour= hour, minute= minute)

sched.start()


print("Waiting to exit")
while True:
	time.sleep(1)