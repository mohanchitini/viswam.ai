from scraper import scrape_and_clean

print("\n[TEST] Valid URL:")
result = scrape_and_clean("https://www.india.gov.in")
print(result[:300] + "...\n" if result else "[No Content]")

print("[TEST] Invalid URL:")
print(scrape_and_clean("https://thiswebsitedoesnotexist.example"))

print("[TEST] Timeout URL:")
print(scrape_and_clean("https://www.india.gov.in:81"))
