from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uuid
import re
from bs4 import BeautifulSoup  # for HTML parsing of DuckDuckGo results

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class OTPRequest(BaseModel):
    name: str
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str

users = {}
otps = {}

def wiki_search(query: str) -> str | None:
    """Try Wikipedia search and return a summary of the top hit."""
    try:
        # first perform a search to get the title
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
        }
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        hits = data.get("query", {}).get("search", [])
        if not hits:
            return None
        title = hits[0]["title"]

        # fetch summary of the page
        r2 = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
            timeout=5,
        )
        r2.raise_for_status()
        summary = r2.json().get("extract")
        if summary:
            return f"📚 **Wikipedia – {title}**\n{summary}"
    except Exception:  # any failure just return None so callers can try other sources
        pass
    return None


def ddg_html_search(query: str) -> str | None:
    """Scrape DuckDuckGo's lightweight HTML page and return top few results with title/snippet."""
    try:
        url = "https://html.duckduckgo.com/html/"
        resp = requests.post(url, data={"q": query}, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # collect up to 3 results
        entries = []
        for result in soup.select("div.result"):
            a = result.select_one("a.result__a")
            snippet_el = result.select_one("a.result__snippet, div.result__snippet")
            if not a:
                continue
            title = a.get_text(strip=True)
            href = a.get("href")
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            if title and href:
                # build html link with optional snippet
                if snippet:
                    entries.append(f"<a href='{href}' target='_blank'>{title}</a><br><small>{snippet}</small>")
                else:
                    entries.append(f"<a href='{href}' target='_blank'>{title}</a>")
            if len(entries) >= 3:
                break
        if entries:
            return "<div>" + "<br><br>".join(entries) + "</div>"
    except Exception:
        pass
    return None


def real_google_search(query):
    """🔥 attempt a live lookup using free sources with fallbacks"""
    # 1. DuckDuckGo instant answer (lightweight JSON service)
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url, timeout=8)
        data = response.json()

        abstract = data.get("AbstractText", "").strip()
        if abstract and abstract.lower() != query.lower():
            heading = data.get('Heading', query)
            return f"✅ <strong>{heading}</strong>: {abstract}"

        # sometimes instant answer returns just the query; ignore that
        if data.get("RelatedTopics"):
            text = data['RelatedTopics'][0].get('Text', '')
            if text:
                return f"🌐 {text}"
    except Exception:
        pass

    # 2. Wikipedia fallback
    wiki = wiki_search(query)
    if wiki:
        # also include some DDG links beneath wiki result for context
        ddg_html = ddg_html_search(query)
        if ddg_html:
            return wiki + "<br><br>" + ddg_html
        return wiki

    # 3. HTML DuckDuckGo scrape (always try at least links)
    ddg_html = ddg_html_search(query)
    if ddg_html:
        return ddg_html

    # last resort
    return f"🔍 Searched '{query}' - here's whatever I could find online."
def get_smart_ai_response(message):
    msg_lower = message.lower().strip()
    
    # Smart knowledge first
    knowledge = {
        "who r u": "🤖 **Smart AI Bot** - Your frontend dev assistant! FastAPI + Google Search.",
        "who are you": "I'm your AI coding coach. Ask about JavaScript, React, interviews, or ANYTHING!",
        "hi": "👋 **Hey Yogesh!** Ready for coding, interviews, or portfolio help?",
        "hello": "Hello! 🚀 Your Perplexity clone is live. Ask anything!",
        "python": "🐍 **Python**: Backend king! FastAPI (this project), Django, Flask.",
        "fastapi": "⚡ **FastAPI**: Modern Python API. Async, auto-docs, type-safe. THIS BOT!",
        "president usa": "🇺🇸 **Donald Trump** - Current US President (2025).",
        "prime minister india": "🇮🇳 **Narendra Modi** - PM since 2014.",
        "chennai": "🏙️ **Chennai**: IT hub! TCS, Infosys, startups. Weather 28-35°C.",
    }
    
    if msg_lower in knowledge:
        return knowledge[msg_lower]
    
    # Google search everything else
    return real_google_search(message)

@app.get("/")
def home():
    return {"status": "🚀 PERPLEXITY CLONE + GOOGLE SEARCH ✅"}

@app.post("/chat")
async def chat(request: ChatRequest):
    for email in users:
        if users[email].get("session_id") == request.session_id:
            return {"reply": get_smart_ai_response(request.message)}
    return {"reply": "🔐 Login first! Name → Email → 123456"}

@app.post("/send-otp")
def send_otp(request: OTPRequest):
    otp = "123456"
    otps[request.email] = {"otp": otp, "name": request.name}
    print(f"\n🎉 OTP: 123456 → {request.email}")
    return {"success": True, "otp": "123456", "message": "OTP sent!"}

@app.post("/verify-otp")
def verify_otp(request: OTPVerify):
    if request.email in otps and otps[request.email]["otp"] == request.otp:
        session_id = str(uuid.uuid4())
        users[request.email] = {"name": otps[request.email]["name"], "session_id": session_id}
        print(f"✅ LOGGED IN: {request.email}")
        del otps[request.email]
        return {"success": True, "message": "✅ AI Ready! Ask anything:", "session_id": session_id}
    return {"success": False, "message": "❌ Wrong OTP (123456)"}

print("🚀 Starting Perplexity Clone...")
