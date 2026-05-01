# =====================================================
# 🌐 LAYER 1: IMPORTS (DEPENDENCIES)
# =====================================================
# Purpose: Bring required tools to run FastAPI server

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.agent import run_agent


# =====================================================
# 🚀 LAYER 2: CREATE FASTAPI APP
# =====================================================
# Purpose: This is the main web server object

app = FastAPI()


# =====================================================
# 📦 LAYER 3: REQUEST MODEL (INPUT FORMAT)
# =====================================================
# Purpose: Define how frontend sends data to backend

class ChatRequest(BaseModel):
    message: str


# =====================================================
# 🤖 LAYER 4: CHAT API ENDPOINT
# =====================================================
# Purpose: Receive user message → send to AI agent → return response

@app.post("/chat")
def chat(request: ChatRequest):

    # Send user input to AI agent
    response = run_agent(request.message)

    # Return AI response to frontend
    return {"response": response}


# =====================================================
# 🌐 LAYER 5: SERVE FRONTEND STATIC FILES
# =====================================================
# Purpose: Allow browser to access HTML/JS UI

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# =====================================================
# 🏠 LAYER 6: HOME PAGE (UI ENTRY POINT)
# =====================================================
# Purpose: Open chat UI in browser

@app.get("/")
def home():
    return FileResponse("app/static/index.html")