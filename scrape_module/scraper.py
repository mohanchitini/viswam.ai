import requests
from bs4 import BeautifulSoup

def scrape_and_clean(url):
    try:
        if not url.startswith("http"):
            return "Invalid URL format"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        clean_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        
        return clean_text if clean_text else "No paragraph text found."
    except Exception as e:
        return f"Error: {e}"
