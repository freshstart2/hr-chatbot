from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HR Analytics Chatbot", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "1.1.0",
        "service": "hr-chatbot-backend"
    }

@app.post("/api/chat")
async def chat_placeholder(body: dict):
    return {
        "answer": f"Echo: {body.get('text', '')}",
        "status": "placeholder - pipeline not yet wired"
    }
