from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import sys
import time

scheduler = BackgroundScheduler()


def run_tracker_job():

    print("🚀 Running tracker job...")

    try:
        result = subprocess.run(
            [sys.executable, "run_tracker.py"],
            capture_output=True,
            text=True
        )

        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

        if result.returncode != 0:
            print("❌ Tracker failed with error code:", result.returncode)

    except Exception as e:
        print("❌ Exception running tracker:", e)


# 🔥 Run once at startup
run_tracker_job()

# ⏰ Schedule every 3 hours
scheduler.add_job(
    run_tracker_job,
    "interval",
    hours=3,
    max_instances=1,   # prevents overlap
    coalesce=True      # merges missed runs
)

scheduler.start()

print("✅ Scheduler started")

# 🧠 Keep process alive (important for Railway)
while True:
    time.sleep(60)