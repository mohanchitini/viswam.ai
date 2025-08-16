# translate_portal.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator
from flask import Flask, Response

app = Flask(__name__)

# ---------- Function to translate HTML ----------
def translate_html(html, target_lang="te"):
    soup = BeautifulSoup(html, "html.parser")
    
    for element in soup.find_all(string=True):
        parent = element.parent
        if parent and parent.name not in ["script", "style", "meta", "link", "head"]:
            text = element.strip()
            if text and len(text) > 2:  # skip empty/very short texts
                try:
                    translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
                    if translated:
                        element.replace_with(NavigableString(translated))
                except Exception:
                    pass
    return soup

# ---------- Function to get page source ----------
def get_page_source(url):
    options = Options()
    options.add_argument("--headless=new")  # modern headless
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/115.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

# ---------- Flask route ----------
@app.route("/")
def show_translated():
    url = "https://services.india.gov.in/"  # test URL
    html = get_page_source(url)
    translated_soup = translate_html(html, target_lang="te")
    # Use Response to return raw HTML (so browser renders properly)
    return Response(str(translated_soup), mimetype="text/html")

# ---------- Run Flask ----------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
