import time
from run_tracker import run_tracker


def start_worker():

    print("🚀 WORKER STARTED (Level 5)")

    while True:

        try:
            run_tracker()

            print("⏳ Sleeping 3 hours...\n")
            time.sleep(60 * 60 * 3)

        except Exception as e:

            print("❌ Worker error:", e)
            time.sleep(60)  # retry after 1 min


if __name__ == "__main__":
    start_worker()