from searcher import find_urls
from extractor import extract_events
from database import save_event, is_duplicate, create_table


def run_tracker():

    print("\n🚀 RUNNING TRACKER PIPELINE")

    create_table()

    # STEP 1: FIND SOURCES
    urls = find_urls()
    print(f"🔎 URLs found: {len(urls)}")

    saved = 0
    skipped = 0

    # STEP 2: EXTRACT EVENTS
    for url in urls:

        try:
            posts = extract_events(url)

            for post in posts:

                # STEP 3: DUPLICATE CHECK
                if post.get("embedding") and is_duplicate(post["embedding"]):
                    print("⚠️ Duplicate skipped")
                    skipped += 1
                    continue

                # STEP 4: SAVE
                save_event(post)
                saved += 1

                print("✅ Saved event")

        except Exception as e:
            print("❌ Error processing URL:", e)
            skipped += 1

    print(f"\n📊 DONE → Saved: {saved}, Skipped: {skipped}")