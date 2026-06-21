import time

from searcher import find_urls
from extractor import extract_text
from extractor_ai import analyze_event

from database import (
    create_table,
    save_event
)

from embeddings import get_embedding, is_duplicate

# Ensure DB exists
create_table()

print("\n🔎 Thailand BL Tracker Started...\n")


# STEP 1: Get URLs
urls = find_urls()

print(f"\n📌 Total URLs found: {len(urls)}\n")


# STEP 2: Process each URL
for i, url in enumerate(urls):

    print(f"\n[{i+1}/{len(urls)}] Processing:")
    print(url)

    # STEP 3: Extract text
    text = extract_text(url)

    if not text or len(text) < 300:
        print("❌ Skipped (no useful content)")
        continue

    # STEP 4: AI analysis
    result = analyze_event(text, url)

    if not result:
        continue

    # STEP 5: Must be an event
    if not result.get("event"):
        print("❌ Not an event")
        continue

    # STEP 6: Confidence filter (Level 2.2)
    confidence = result.get("confidence", 0)

    if confidence < 70:
        print(f"❌ Low confidence skipped: {confidence}")
        continue

    # STEP 7: Build embedding text
    embed_text = (
        result.get("summary", "") + " " +
        str(result.get("actors", [])) + " " +
        result.get("company", "")
    )

    embedding = get_embedding(embed_text)
    result["embedding"] = embedding

    # STEP 8: Duplicate detection (Level 2.1)
    if is_duplicate(embedding):
        print("⚠️ Duplicate event detected (semantic match)")
        continue

    # STEP 9: Optional safety boost cap
    if confidence > 100:
        confidence = 100
        result["confidence"] = 100

    # STEP 10: Save metadata
    result["source"] = "internet"

    # STEP 11: Save to database
    save_event(result)

    print("✅ SAVED EVENT")
    print("📌 Summary:", result.get("summary"))
    print("🎯 Confidence:", confidence)

    time.sleep(2)


print("\n🎉 Tracker run complete!\n")