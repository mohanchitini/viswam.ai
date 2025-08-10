<<<<<<< HEAD
from scraper import scrape_and_clean

print("\n[TEST] Valid URL:")
result = scrape_and_clean("https://www.india.gov.in")
print(result[:300] + "...\n" if result else "[No Content]")

print("[TEST] Invalid URL:")
print(scrape_and_clean("https://thiswebsitedoesnotexist.example"))

print("[TEST] Timeout URL:")
print(scrape_and_clean("https://www.india.gov.in:81"))
=======
import scraper

def test_scraper():
    test_url = "https://www.india.gov.in"  # Example gov site
    result = scraper.scrape_and_clean(test_url)
    assert isinstance(result, str)
    assert "Error" not in result or result.startswith("Error:")

if __name__ == "__main__":
    test_scraper()
    print("✅ Test passed!")
>>>>>>> 4a4e97b (Optimized scrape_and_clean with timeout & empty content handling, added test)
