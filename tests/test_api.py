import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


# --- health endpoint ---

@pytest.mark.asyncio
async def test_health_online(client):
    # patch the internal httpx call inside main.health(), not the test client
    with patch("app.main.httpx.AsyncClient") as mock_cls:
        mock_instance = AsyncMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        mock_instance.get = AsyncMock(return_value=AsyncMock(status_code=200))
        mock_cls.return_value = mock_instance

        resp = await client.get("/health")

    assert resp.status_code == 200
    assert resp.json()["status"] == "online"


@pytest.mark.asyncio
async def test_health_offline(client):
    with patch("app.main.httpx.AsyncClient") as mock_cls:
        mock_instance = AsyncMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        mock_instance.get.side_effect = httpx.ConnectError("down")
        mock_cls.return_value = mock_instance

        resp = await client.get("/health")

    assert resp.status_code == 200
    assert resp.json()["status"] == "offline"


# --- chat endpoint ---

@pytest.mark.asyncio
async def test_chat_returns_reply(client):
    # patch where the name is looked up: app.main imports ask_ghost from app.ghost
    with patch("app.main.ask_ghost", new_callable=AsyncMock, return_value="I linger between your keystrokes."):
        resp = await client.post("/chat", json={"message": "hello", "personality": "friendly", "history": []})
    assert resp.status_code == 200
    assert resp.json()["reply"] == "I linger between your keystrokes."


@pytest.mark.asyncio
async def test_chat_default_personality(client):
    with patch("app.main.ask_ghost", new_callable=AsyncMock, return_value="...") as mock:
        await client.post("/chat", json={"message": "hi"})
    mock.assert_called_once_with("hi", "friendly", [])


@pytest.mark.asyncio
@pytest.mark.parametrize("personality", ["friendly", "cursed", "ancient"])
async def test_chat_all_personalities(client, personality):
    with patch("app.main.ask_ghost", new_callable=AsyncMock, return_value="boo") as mock:
        resp = await client.post("/chat", json={"message": "test", "personality": personality, "history": []})
    assert resp.status_code == 200
    mock.assert_called_once_with("test", personality, [])


@pytest.mark.asyncio
async def test_chat_ollama_offline_returns_warning(client):
    with patch("app.ghost.httpx.AsyncClient") as mock_cls:
        mock_instance = AsyncMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        mock_instance.post.side_effect = httpx.ConnectError("offline")
        mock_cls.return_value = mock_instance

        resp = await client.post("/chat", json={"message": "hello", "personality": "friendly", "history": []})

    assert resp.status_code == 200
    body = resp.json()["reply"]
    assert "Ollama" in body or "ghost" in body


# --- root ---

@pytest.mark.asyncio
async def test_root_serves_html(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
