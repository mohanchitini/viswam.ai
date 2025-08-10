# In main.py
urls = [
    "https://www.wikipedia.org/",
    "https://www.python.org/",
    "https://www.bbc.com/"
]

from scrape_module.scraper import scrape_and_clean

for u in urls:
    print(f"\nScraping: {u}")
    result = scrape_and_clean(u)
    if result:
        print(result[:300])  # show first 300 chars
    else:
        print("No content found or request failed.")
