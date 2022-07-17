from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_notification
from datetime import datetime

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_notification, 'interval', seconds=5)
    scheduler.start()
