# Smart AI Bot

This repository contains a simple chat-bot web application (`Perplexity`-style) built with:

- **FastAPI** backend (Python)
- **Vanilla HTML/CSS/JS** frontend
- Live search functionality using free sources (DuckDuckGo, Wikipedia, etc.)

## Features

- One-time password (OTP) login flow
- Chat UI with animated typing indicator and polished styling
- Automatic lookup against multiple free search providers
- Results include clickable links and summaries

## Setup

1. **Install Python dependencies** (from the `backend` folder):
   ```powershell
   cd backend
   python -m venv venv          # if not already
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```

2. **Run the backend**:
   ```powershell
   uvicorn server:app --reload
   ```
   The API runs on `http://127.0.0.1:8000` by default.

3. **Open the frontend**
   Simply open `frontend/index.html` in your browser, or serve it from a simple static server.

   _The chat UI will accept full sentences; the backend treats whatever you type as a
   search query and tries to fetch results accordingly. The more descriptive your
   question, the better the output._

4. **Use the bot**
   - Click the chat button, register with a name/email pair
   - Use OTP `123456` (printed in server console)
   - Ask questions; the bot will search the web for answers.

## Customizing search

The backend `server.py` contains several helper functions:

- `real_google_search`: main entry point that tries, in order:
  1. DuckDuckGo instant answer (quick facts)
  2. Bing Web Search API (if you supply a `BING_KEY` environment variable)
  3. Wikipedia search/summary
  4. DuckDuckGo HTML scraping (always produces a list of links/snippets)

  The function always returns some HTML‑formatted text so the frontend can render
  clickable links and snippets.  It also appends DDG links under whatever content
  it fetches, giving the user multiple choices.

- `wiki_search`, `ddg_html_search`, `bing_search` are the individual helpers.

You can extend or replace any of these providers.  For example, add a call to
another free API, or perform your own crawling.  The search logic is deliberately
permissive so that even vague or one‑word queries will return at least a list of
possible links the user can follow.

To enable Bing, set the environment variable before starting the server:

```powershell
# Windows PowerShell
$env:BING_KEY = "your_key_here"
uvicorn server:app --reload
```

Bing offers a small free tier and will enrich the answers when available.

## License

This project is free and open-source. Feel free to modify and extend!
