from extractor import extract_events
from database import save_event, create_table, is_duplicate
import time


create_table()


def run_tracker():

    print("🚀 Starting tracker...")

    posts = extract_events()

    print(f"📥 Posts received: {len(posts)}")

    if not posts:
        print("⚠️ No posts found — extractor returned empty list")
        return

    saved = 0
    skipped = 0

    for post in posts:

        try:
            # -----------------------
            # DUPLICATE CHECK
            # -----------------------
            if post.get("embedding") and is_duplicate(post["embedding"]):
                print("⚠️ Duplicate skipped")
                skipped += 1
                continue

            save_event(post)
            print("✅ Saved:", post.get("company", "Unknown"))
            saved += 1

        except Exception as e:
            print("❌ Error saving post:", e)
            skipped += 1

    print(f"\n📊 DONE → Saved: {saved}, Skipped: {skipped}")


# 🔥 IMPORTANT ENTRY POINT
if __name__ == "__main__":

    run_tracker()