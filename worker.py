from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import sys

scheduler = BlockingScheduler()

def run_tracker_job():
    print("Running tracker...")

    try:
        subprocess.run(
            [sys.executable, "run_tracker.py"],
            check=True

        )
    except Exception as e:
        print("Error:", e)

# Run immediately at startup
run_tracker_job()

# Run every 3 hours
scheduler.add_job(
    run_tracker_job,
    "interval",
    hours=3
)

print("scheduler started")

scheduler.start()