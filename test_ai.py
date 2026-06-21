from searcher import find_urls
from extractor import extract_text
from extractor_ai import analyze_event


urls = find_urls()

for url in urls[:3]:

    print("\nURL:", url)

    text = extract_text(url)

    if len(text) < 200:
        print("Too little text, skipping")
        continue

    result = analyze_event(text, url)

    print("\nRESULT:\n")
    print(result)