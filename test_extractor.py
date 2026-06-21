from extractor import extract_text
from searcher import find_urls


urls = find_urls()

print("\n--- EXTRACTING FIRST 3 URLs ---\n")

for url in urls[:3]:

    text = extract_text(url)

    print("\nURL:", url)
    print("TEXT SAMPLE:\n")
    print(text[:500])  # only show first 500 characters
    print("\n" + "-"*50)