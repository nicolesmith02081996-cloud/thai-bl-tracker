from searcher import find_urls

urls = find_urls()

print("\nFound URLs:\n")

for url in urls:
    print(url)