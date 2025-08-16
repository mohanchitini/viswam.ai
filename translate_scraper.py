"""
FastAPI app that:
- /scrape?url=...&lang=te  -> returns PLAIN TEXT (translated if lang != en)
- /view?url=...&lang=te    -> shows a TRANSLATED version of the page (structure preserved)
- /  -> simple UI: paste URL, see translated plain text + a link to open the translated page

Tested with: https://www.india.gov.in/

Run: uvicorn translate_scraper:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from typing import Optional, List
import requests
from bs4 import BeautifulSoup, NavigableString, Comment
from urllib.parse import urljoin, quote
import re

try:
    from deep_translator import GoogleTranslator
except Exception:  # pragma: no cover
    GoogleTranslator = None  # fallback handled at runtime

app = FastAPI(title="Simple Scraper + Translator")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
VISIBLE_RE = re.compile(r"[\w\u0900-\u097F\u0C00-\u0C7F]", re.UNICODE)  # Latin, Devanagari, Telugu


# -------------------- HTTP fetch --------------------

def fetch_html(url: str) -> tuple[str, str]:
    """Fetch raw HTML; return (html, base_url). Raises HTTPException on failure."""
    try:
        resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {e}")
    return resp.text, resp.url  # final URL after redirects


# -------------------- Text extraction --------------------

def extract_plain_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript", "template", "svg", "canvas"]):
        tag.decompose()

    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()

    lines: List[str] = []
    for text in soup.stripped_strings:
        if VISIBLE_RE.search(text):
            lines.append(text)

    cleaned: List[str] = []
    prev = None
    for t in lines:
        if t != prev:
            cleaned.append(t)
        prev = t

    return "\n".join(cleaned).strip()


# -------------------- HTML translation --------------------

def translate_html_preserving_structure(html: str, base_url: str, target_lang: str) -> str:
    if GoogleTranslator is None:
        raise HTTPException(status_code=500, detail="deep-translator not installed")

    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all(True):
        for attr in ("href", "src", "action", "data-src", "poster"):
            if tag.has_attr(attr):
                try:
                    tag[attr] = urljoin(base_url, tag[attr])
                except Exception:
                    pass

    targets: List[NavigableString] = []
    originals: List[str] = []

    skip_parents = {"script", "style", "noscript", "template"}

    for node in soup.find_all(string=True):
        if isinstance(node, Comment):
            continue
        p = node.parent.name.lower() if node.parent and node.parent.name else ""
        if p in skip_parents:
            continue
        text = str(node)
        if VISIBLE_RE.search(text) and text.strip():
            targets.append(node)
            originals.append(text)

    if not originals:
        return str(soup)

    translator = GoogleTranslator(source="auto", target=target_lang)

    try:
        translated: List[str] = translator.translate_batch(originals)  # type: ignore
        if not isinstance(translated, list) or len(translated) != len(originals):
            raise RuntimeError("translate_batch returned unexpected shape")
    except Exception:
        translated = []
        for text in originals:
            try:
                translated.append(translator.translate(text))
            except Exception:
                translated.append(text)

    for node, new_text in zip(targets, translated):
        try:
            node.replace_with(new_text)
        except Exception:
            pass

    return str(soup)


# -------------------- Routes --------------------

@app.get("/", response_class=HTMLResponse)
def home(url: Optional[str] = Query(None), lang: str = Query("te")):
    """Simple UI to paste a URL, preview translated text, and get a translated-page link."""
    preview_text = ""
    trans_link = ""

    if url:
        html, base = fetch_html(url)
        preview_text = extract_plain_text(html)[:10000]

        # Translate preview text if requested
        if lang != "en" and GoogleTranslator:
            try:
                translator = GoogleTranslator(source="auto", target=lang)
                preview_text = translator.translate(preview_text)
            except Exception:
                pass

        trans_link = f"/view?lang={quote(lang)}&url={quote(url, safe='')}"

    return HTMLResponse(
        f"""
        <html>
        <head>
            <meta charset='utf-8'>
            <title>Scrape & Translate</title>
            <style>
                body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem; }}
                .row {{ display: grid; gap: 1rem; grid-template-columns: 1fr; max-width: 980px; }}
                label {{ font-weight: 600; }}
                input, select {{ padding: .6rem; width: 100%; border: 1px solid #ddd; border-radius: .5rem; }}
                button {{ padding: .6rem 1rem; border-radius: .5rem; border: 0; background: #111; color: white; cursor: pointer; }}
                textarea {{ width: 100%; height: 360px; border: 1px solid #ddd; border-radius: .5rem; padding: .6rem; white-space: pre-wrap; }}
                .hint {{ color: #555; font-size: .9rem; }}
                .link {{ margin-top: .5rem; }}
                .card {{ background: #fafafa; border: 1px solid #eee; border-radius: .75rem; padding: 1rem; }}
            </style>
        </head>
        <body>
            <h1>Scrape & Translate</h1>
            <form method="get" action="/">
                <div class="row card">
                    <label for="url">Page URL</label>
                    <input id="url" name="url" type="url" placeholder="https://www.india.gov.in/" value="{url or ''}" required>
                    <label for="lang">Target language</label>
                    <select id="lang" name="lang">
                        <option value="te" {'selected' if lang=='te' else ''}>Telugu (te)</option>
                        <option value="hi" {'selected' if lang=='hi' else ''}>Hindi (hi)</option>
                        <option value="en" {'selected' if lang=='en' else ''}>English (en)</option>
                    </select>
                    <button type="submit">Scrape</button>
                    {f"<div class='link'><a href='{trans_link}' target='_blank'>Open translated page →</a></div>" if trans_link else ''}
                    <div class="hint">Tip: Use the link above to view the translated page with the original layout.</div>
                </div>
            </form>

            <h3>Extracted & Translated text</h3>
            <textarea readonly>{preview_text}</textarea>
        </body>
        </html>
        """
    )


@app.get("/scrape", response_class=PlainTextResponse)
def scrape(url: str = Query(...), lang: str = Query("te")):
    """Return plain text (translated if lang != en)."""
    html, _ = fetch_html(url)
    text = extract_plain_text(html)

    if lang != "en" and GoogleTranslator:
        try:
            translator = GoogleTranslator(source="auto", target=lang)
            text = translator.translate(text)
        except Exception:
            pass

    return PlainTextResponse(text)


@app.get("/api/scrape", response_class=JSONResponse)
def scrape_api(url: str = Query(...), lang: str = Query("te")):
    html, _ = fetch_html(url)
    text = extract_plain_text(html)

    if lang != "en" and GoogleTranslator:
        try:
            translator = GoogleTranslator(source="auto", target=lang)
            text = translator.translate(text)
        except Exception:
            pass

    translated_link = f"/view?lang={quote(lang)}&url={quote(url, safe='')}"
    return {"url": url, "language": lang, "plain_text": text, "translated_link": translated_link}


@app.get("/view", response_class=HTMLResponse)
def view(url: str = Query(...), lang: str = Query("te")):
    html, base = fetch_html(url)
    translated_html = translate_html_preserving_structure(html, base, lang)
    return HTMLResponse(translated_html)


@app.get("/health")
def health():
    return {"status": "ok"}
