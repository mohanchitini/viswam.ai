import sys
from scrape_module import scraper

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url> [-g]")
        sys.exit(1)

    url = sys.argv[1]
    only_gov = "-g" in sys.argv  # if -g is given, restrict to government sites

    try:
        text = scraper.scrape_and_clean(url, only_gov=only_gov)
        print(f"\nScraping: {url}\n")
        
        for i, chunk in enumerate(scraper.chunk_text(text), 1):
            print(f"--- Chunk {i} ---")
            print(chunk)
            print()

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
