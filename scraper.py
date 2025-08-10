from scraper import scrape_and_clean

# Test with a working URL
print("Test 1 (Valid URL):")
print(scrape_and_clean("https://www.india.gov.in"))

# Test with an invalid URL
print("\nTest 2 (Invalid URL):")
print(scrape_and_clean("https://invalid-url.example"))

# Test with a slow site (simulate timeout)
print("\nTest 3 (Timeout Test):")
print(scrape_and_clean("https://httpstat.us/200?sleep=15000"))
