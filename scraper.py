import requests
from bs4 import BeautifulSoup

def scrape_and_clean(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not response.text.strip():
            print("[ERROR] Empty page content.")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        text = ' '.join(soup.stripped_strings)

        if not text:
            print("[ERROR] No visible text found.")
            return ""

        return text

    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out.")
        return ""

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return ""
