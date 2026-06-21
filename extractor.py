import trafilatura
import requests


def extract_text(url):

    try:

        downloaded = trafilatura.fetch_url(url)

        if downloaded:

            text = trafilatura.extract(downloaded)

            if text and len(text) > 100:
                return text

        # fallback (important for Facebook-like pages)
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        return trafilatura.extract(r.text)

    except:

        return ""