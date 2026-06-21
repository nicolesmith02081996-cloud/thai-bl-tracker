from duckduckgo_search import DDGS
import time

QUERIES = [
    "GMMTV fan meeting announcement",
    "Domundi fan meeting official",
    "Be On Cloud event announcement",
    "Thai BL fan meeting tickets",
    "site:facebook.com \"fan meeting\" GMMTV",
    "site:instagram.com \"fan meeting\"",
    "GMMTV official event Bangkok",
    "Thai BL concert announcement"
]


BLACKLIST = [
    "login",
    "privacy",
    "policies",
    "ads",
    "signup"
]


def is_valid(url):
    url = url.lower()
    return not any(b in url for b in BLACKLIST)


def find_urls():

    urls = []

    with DDGS() as ddgs:

        for q in QUERIES:

            print("Searching:", q)

            results = ddgs.text(q, max_results=8)

            for r in results:

                url = r.get("href")

                if url and is_valid(url):
                    urls.append(url)

            time.sleep(2)

    # remove duplicates
    urls = list(set(urls))

    print("\nTOTAL CLEAN URLS:", len(urls))
    return urls