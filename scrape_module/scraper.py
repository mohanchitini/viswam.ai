import requests
from bs4 import BeautifulSoup
import re

def scrape_and_clean(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.exceptions.Timeout:
        print(f"Request timed out for URL: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    text = soup.get_text(separator=" ", strip=True)  # ✅ Space instead of newline

    # Keep only English letters, numbers, punctuation, and spaces
    english_text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'\"()\-]", "", text)

    # Collapse multiple spaces into one
    english_text = re.sub(r"\s+", " ", english_text).strip()

    if not english_text:
        print(f"No English content found for URL: {url}")
        return None

    return english_text
