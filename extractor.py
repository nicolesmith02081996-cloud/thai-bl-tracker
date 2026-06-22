import json
import requests
from bs4 import BeautifulSoup
import time


# -------------------------------------------------
# SAFE POST STRUCTURE (always returned)
# -------------------------------------------------
def clean_post(post):

    return {
        "source": post.get("source", ""),
        "company": post.get("company", ""),
        "actors": post.get("actors", []),
        "date": post.get("date", ""),
        "location": post.get("location", ""),
        "ticket_sale": post.get("ticket_sale", False),
        "summary": post.get("summary", ""),
        "url": post.get("url", ""),
        "embedding": post.get("embedding", "")
    }


# -------------------------------------------------
# MAIN FUNCTION (USED BY run_tracker.py)
# -------------------------------------------------
def extract_events():

    posts = []

    print("🔍 Extractor started...")

    try:
        # -------------------------------------------------
        # STEP 1: BASIC WEB SCRAPE EXAMPLE (PLACEHOLDER)
        # Replace this later with Facebook / Instagram logic
        # -------------------------------------------------

        url = "https://x.com/GMMTV"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("⚠️ Failed to fetch page")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        # -------------------------------------------------
        # STEP 2: FAKE PARSING (X / FB / IG WILL GO HERE)
        # -------------------------------------------------

        elements = soup.find_all("article")

        for i, el in enumerate(elements[:10]):

            text = el.get_text(strip=True)

            if not text:
                continue

            post = {
                "source": "web",
                "company": "Unknown",
                "actors": [],
                "date": "",
                "location": "",
                "ticket_sale": False,
                "summary": text[:300],
                "url": url,
                "embedding": ""
            }

            posts.append(clean_post(post))

        print(f"📥 Extracted {len(posts)} posts")

        return posts

    except Exception as e:

        print("❌ Extractor error:", e)

        return []