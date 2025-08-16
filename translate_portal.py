# translate_portal.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from flask import Flask, render_template_string

# ---------- Flask app ----------
app = Flask(__name__)

# ---------- Function to translate HTML ----------
def translate_html(html, target_lang="te"):
    soup = BeautifulSoup(html, "html.parser")
    
    for element in soup.find_all(string=True):  # use string=True to avoid deprecation warning
        parent = element.parent
        if parent and parent.name not in ["script", "style", "meta", "link", "head"]:
            text = element.strip()
            if text:
                try:
                    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
                    if translated and parent:
                        element.replace_with(translated)
                except Exception:
                    pass  # skip if translation fails
    return soup

# ---------- Function to get page source ----------
def get_page_source(url):
    options = Options()
    options.add_argument("--headless")
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
    url = "https://services.india.gov.in/"  # replace with any URL
    html = get_page_source(url)
    translated_soup = translate_html(html, target_lang="te")
    return render_template_string(str(translated_soup))

# ---------- Run Flask ----------
if __name__ == "__main__":
    app.run(debug=True)