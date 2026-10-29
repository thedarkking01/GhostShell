import httpx
from app.prompts import PERSONALITIES, DEFAULT_PERSONALITY

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:1b"


async def ask_ghost(message: str, personality: str = DEFAULT_PERSONALITY, history: list = []) -> str:
    system_prompt = PERSONALITIES.get(personality, PERSONALITIES[DEFAULT_PERSONALITY])

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(OLLAMA_URL, json={"model": MODEL, "messages": messages, "stream": False})
            response.raise_for_status()
            return response.json()["message"]["content"]
    except httpx.ConnectError:
        return "⚠ The ghost cannot be reached. Is Ollama running? Try: ollama serve"
    except Exception as e:
        return f"⚠ Something went wrong in the void: {str(e)}"
