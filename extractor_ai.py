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
    "ticket",
    "ticket sale",
    "live in",
    "stage appearance",
    "appearance",
    "special stage",
    "press conference"
]

THAI_BL_COMPANIES = [
    "GMMTV",
    "Domundi",
    "Be On Cloud",
    "Studio Wabi Sabi",
    "Me Mind Y",
    "Change2561",
    "Copy A Bangkok",
    "Mandee",
    "M Flow Entertainment",
    "Star Hunter",
    "Idol Factory"
]

KNOWN_LOCATIONS = [
    "Bangkok",
    "Thailand",
    "Siam Paragon",
    "Paragon Hall",
    "CentralWorld",
    "ICONSIAM",
    "EmQuartier",
    "Union Mall",
    "Impact Arena",
    "Thunder Dome",
    "Samyan Mitrtown",
    "One Bangkok"
]


# ==========================================
# LOGGING
# ==========================================

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


# ==========================================
# STANDARD EVENT FORMAT
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

def fetch_text(url):

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:
            log(f"⚠️ HTTP {response.status_code}")
            return ""

        text = trafilatura.extract(response.text)

        if text:
            return text

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return soup.get_text(
            separator=" ",
            strip=True
        )

    except Exception as e:
        log(f"❌ Fetch failed: {e}")
        return ""


# ==========================================
# EVENT DETECTION
# ==========================================

def is_event(text):

    lower = text.lower()

    return any(
        keyword in lower
        for keyword in EVENT_KEYWORDS
    )


# ==========================================
# COMPANY DETECTION
# ==========================================

def detect_company(text):

    for company in THAI_BL_COMPANIES:

        if company.lower() in text.lower():
            return company

    return "Unknown"


# ==========================================
# LOCATION DETECTION
# ==========================================

def detect_location(text):

    for location in KNOWN_LOCATIONS:

        if location.lower() in text.lower():
            return location

    return ""


# ==========================================
# DATE DETECTION
# ==========================================

def detect_date(text):

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
# ACTOR DETECTION
# ==========================================

def detect_actors(text):

    matches = re.findall(
        r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b",
        text
    )

    ignore = {
        "Thailand",
        "Bangkok",
        "Tickets",
        "Official",
        "Event",
        "Concert",
        "Tour",
        "Fan"
    }

    actors = []

    for name in matches:

        if name not in ignore:
            actors.append(name)

    return list(dict.fromkeys(actors))[:10]


# ==========================================
# SINGLE PAGE ANALYSIS
# ==========================================

def analyze_page(url):

    text = fetch_text(url)

    if not text:
        return None

    if not is_event(text):
        return None

    event = {

        "source": url.split("/")[2],

        "company": detect_company(text),

        "actors": detect_actors(text),

        "date": detect_date(text),

        "location": detect_location(text),

        "ticket_sale":
            "ticket" in text.lower(),

        "summary": text[:500],

        "url": url,

        "embedding": ""
    }

    return clean_event(event)


# ==========================================
# MAIN ENTRY POINT
# ==========================================

def extract_events_from_urls(urls):

    events = []

    log("🧠 AI extraction started")

    for index, url in enumerate(urls, start=1):

        try:

            log(
                f"🔎 Processing {index}/{len(urls)}"
            )

            event = analyze_page(url)

            if event:

                events.append(event)

                log(
                    f"✅ Event found: "
                    f"{event['company']}"
                )

        except Exception as e:

            log(
                f"❌ Error processing {url}: {e}"
            )

    log(
        f"📥 Total events extracted: "
        f"{len(events)}"
    )

    return events


# ==========================================
# LOCAL TEST
# ==========================================

if __name__ == "__main__":

    sample_urls = [
        "https://www.gmmtv.com"
    ]

    results = extract_events_from_urls(
        sample_urls
    )

    print(results)