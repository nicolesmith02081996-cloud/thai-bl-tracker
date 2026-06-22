from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from datetime import datetime
import traceback

from run_tracker import run_tracker


# ==========================================
# LOGGING
# ==========================================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


# ==========================================
# JOB FUNCTION
# ==========================================

def tracker_job():

    log("🚀 Starting tracker run")

    try:
        run_tracker()

        log("✅ Tracker run completed")

    except Exception as e:
        log(f"❌ Tracker failed: {e}")
        traceback.print_exc()


# ==========================================
# APSCHEDULER EVENT LISTENER
# ==========================================

def job_listener(event):

    if event.exception:
        log("❌ Scheduled job crashed")

    else:
        log("✅ Scheduled job finished successfully")


# ==========================================
# MAIN
# ==========================================

scheduler = BlockingScheduler(
    job_defaults={
        "coalesce": True,      # Merge missed runs
        "max_instances": 1     # Prevent overlap
    }
)

scheduler.add_listener(
    job_listener,
    EVENT_JOB_EXECUTED | EVENT_JOB_ERROR
)

# Run every 3 hours
scheduler.add_job(
    tracker_job,
    trigger="interval",
    hours=3,
    id="bl_tracker_job",
    replace_existing=True
)


if __name__ == "__main__":

    log("🟢 Thailand BL Tracker Scheduler Started")
    log("⏰ Tracker scheduled every 3 hours")

    # Run immediately on startup
    tracker_job()

    try:
        scheduler.start()

    except (KeyboardInterrupt, SystemExit):
        log("🛑 Scheduler stopped")

    except Exception as e:
        log(f"❌ Scheduler crashed: {e}")
        traceback.print_exc()