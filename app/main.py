from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.ghost import ask_ghost

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str
    personality: str = "friendly"
    history: list = []


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/chat")
async def chat(req: ChatRequest):
    reply = await ask_ghost(req.message, req.personality, req.history)
    return {"reply": reply}


@app.get("/health")
async def health():
    import httpx
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            await client.get("http://localhost:11434")
        return {"status": "online"}
    except Exception:
        return {"status": "offline"}