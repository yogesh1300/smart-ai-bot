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

4. **Use the bot**
   - Click the chat button, register with a name/email pair
   - Use OTP `123456` (printed in server console)
   - Ask questions; the bot will search the web for answers.

## Customizing search

The backend `server.py` contains several helper functions:

- `real_google_search`: main entry point that tries:
  1. DuckDuckGo instant answer
  2. Wikipedia search/summary
  3. DuckDuckGo HTML results scraping
  
You can add more providers or tweak the formatting there.

## License

This project is free and open-source. Feel free to modify and extend!
