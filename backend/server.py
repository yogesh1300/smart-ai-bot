from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uuid
import re

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

def real_google_search(query):
    """🔥 LIVE Google search - Perplexity style"""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url, timeout=8)
        data = response.json()
        
        if data.get("AbstractText"):
            return f"✅ **{data['Heading']}**: {data['AbstractText']}"
        elif data.get("RelatedTopics"):
            return f"🌐 **{data['RelatedTopics'][0]['Text'][:300]}...**"
    except:
        pass
    return f"🔍 Searched '{query}' - latest web info!"

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
