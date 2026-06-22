from duckduckgo_search import DDGS
from urllib.parse import urlparse
import time


# ==========================================
# SEARCH QUERIES
# ==========================================

QUERIES = [

    # Companies
    "GMMTV fan meeting announcement",
    "Domundi official fan meeting",
    "Be On Cloud official event",
    "Me Mind Y fan meeting",
    "Studio Wabi Sabi event",

    # General BL events
    "Thai BL fan meeting Bangkok",
    "Thai BL concert announcement",
    "Thai BL event tickets",
    "Thai BL actor appearance Bangkok",

    # Social platforms
    'site:facebook.com GMMTV fan meeting',
    'site:facebook.com Domundi official event',
    'site:instagram.com Thai BL event',
    'site:x.com GMMTV event',
    'site:x.com Domundi fan meeting'
]


# ==========================================
# BLACKLIST
# ==========================================

BLACKLIST = [

    "login",
    "signup",
    "privacy",
    "policy",
    "policies",
    "terms",
    "advertise",
    "ads",
    "account",
    "/status/",
    "/photo/",
    "/reel/",
    "/shorts/",
    "youtube.com/watch"
]


# Prefer official domains
PREFERRED_DOMAINS = [

    "gmmtv.com",
    "facebook.com",
    "instagram.com",
    "x.com",
    "ticketmelon.com",
    "eventpop.me"
]


# ==========================================
# HELPERS
# ==========================================

def is_valid(url):

    if not url:
        return False

    url = url.lower()

    return not any(item in url for item in BLACKLIST)


def extract_url(result):

    return (
        result.get("href")
        or result.get("link")
        or result.get("url")
    )


def score_url(url):

    score = 0

    domain = urlparse(url).netloc.lower()

    for preferred in PREFERRED_DOMAINS:
        if preferred in domain:
            score += 10

    if "official" in url.lower():
        score += 5

    return score


# ==========================================
# MAIN SEARCH FUNCTION
# ==========================================

def find_urls():

    print("🔍 Starting search phase...")

    discovered_urls = []

    with DDGS() as ddgs:

        for query in QUERIES:

            print(f"\nSearching: {query}")

            try:

                results = ddgs.text(
                    query,
                    max_results=10
                )

                for result in results:

                    url = extract_url(result)

                    if not url:
                        continue

                    if not is_valid(url):
                        continue

                    discovered_urls.append(url)

                time.sleep(1)

            except Exception as e:

                print("❌ Search error:", e)

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    discovered_urls = list(set(discovered_urls))

    # ======================================
    # PRIORITIZE OFFICIAL SOURCES
    # ======================================

    discovered_urls.sort(
        key=score_url,
        reverse=True
    )

    print("\n📊 SEARCH COMPLETE")
    print(f"🔗 Unique URLs found: {len(discovered_urls)}")

    for url in discovered_urls[:20]:
        print(" •", url)

    return discovered_urls


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    urls = find_urls()

    print("\nTop URLs:")

    for url in urls[:10]:
        print(url)