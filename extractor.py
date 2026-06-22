import re
import requests
import trafilatura
from bs4 import BeautifulSoup
from datetime import datetime


# ==========================================
# CONFIG
# ==========================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

EVENT_KEYWORDS = [
    "fan meeting",
    "fanmeet",
    "concert",
    "event",
    "meet and greet",
    "meet & greet",
    "showcase",
    "tour",
    "tickets",
    "ticket sale",
    "live in",
    "stage appearance",
    "appearance"
]

LOCATIONS = [
    "Bangkok",
    "Thailand",
    "Siam Paragon",
    "CentralWorld",
    "ICONSIAM",
    "Union Mall",
    "EmQuartier",
    "Paragon Hall",
    "Impact Arena",
    "Thunder Dome"
]


# ==========================================
# LOGGING
# ==========================================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


# ==========================================
# CLEAN EVENT OBJECT
# ==========================================

def clean_event(event):

    return {
        "source": event.get("source", ""),
        "company": event.get("company", ""),
        "actors": event.get("actors", []),
        "date": event.get("date", ""),
        "location": event.get("location", ""),
        "ticket_sale": event.get("ticket_sale", False),
        "summary": event.get("summary", ""),
        "url": event.get("url", ""),
        "embedding": event.get("embedding", "")
    }


# ==========================================
# FETCH PAGE CONTENT
# ==========================================

def fetch_page_text(url):

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:
            return ""

        # First try trafilatura
        extracted = trafilatura.extract(response.text)

        if extracted:
            return extracted

        # Fallback to BeautifulSoup
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return soup.get_text(
            separator=" ",
            strip=True
        )

    except Exception as e:
        log(f"❌ Failed fetching {url}: {e}")
        return ""


# ==========================================
# EVENT DETECTION
# ==========================================

def is_event(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in EVENT_KEYWORDS
    )


# ==========================================
# DATE EXTRACTION
# ==========================================

def extract_date(text):

    patterns = [

        r"\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}\b",

        r"\b\d{4}-\d{2}-\d{2}\b",

        r"\b\d{1,2}/\d{1,2}/\d{4}\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group()

    return ""


# ==========================================
# LOCATION EXTRACTION
# ==========================================

def extract_location(text):

    for location in LOCATIONS:

        if location.lower() in text.lower():
            return location

    return ""


# ==========================================
# ACTOR EXTRACTION (basic)
# ==========================================

def extract_actors(text):

    names = re.findall(
        r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b",
        text
    )

    ignore = {
        "Bangkok",
        "Thailand",
        "Tickets",
        "Official",
        "Event"
    }

    cleaned = []

    for name in names:

        if name not in ignore:
            cleaned.append(name)

    return list(dict.fromkeys(cleaned))[:10]


# ==========================================
# MAIN EXTRACTION
# ==========================================

def extract_events_from_urls(urls):

    events = []

    for index, url in enumerate(urls, start=1):

        log(f"🔎 Processing {index}/{len(urls)}")

        text = fetch_page_text(url)

        if not text:
            continue

        if not is_event(text):
            continue

        event = {

            "source": url.split("/")[2],

            "company": "",

            "actors": extract_actors(text),

            "date": extract_date(text),

            "location": extract_location(text),

            "ticket_sale":
                "ticket" in text.lower(),

            "summary": text[:500],

            "url": url,

            "embedding": ""
        }

        events.append(
            clean_event(event)
        )

        log("✅ Event detected")

    log(f"📥 Total events extracted: {len(events)}")

    return events


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_urls = [
        "https://www.gmmtv.com"
    ]

    results = extract_events_from_urls(
        test_urls
    )

    print(results)