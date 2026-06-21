from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import sys

scheduler = BlockingScheduler()

def run_job():
    print("Running tracker...")
    subprocess.run([sys.executable, "run_tracker.py"])

# Run every 3 hours
scheduler.add_job(run_job, "interval", hours=3)

# Run once at startup
run_job()

scheduler.start()