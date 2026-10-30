# 👻 GhostShell

> *"At last, someone has opened the terminal. I have been waiting in the silence between keystrokes."*

A haunted terminal powered by a **local open-source AI**. Type commands or questions — a ghost responds with eerie, intelligent commentary. No cloud API. No data leaves your machine. No internet required after setup.

![status](https://img.shields.io/badge/status-haunted-blueviolet)
![python](https://img.shields.io/badge/python-3.10%2B-green)
![license](https://img.shields.io/badge/license-MIT-blue)
![built with ollama](https://img.shields.io/badge/built%20with-Ollama-black)

---

## What is GhostShell?

GhostShell is a browser-based terminal that feels possessed. You open it, type something, and a ghost — powered entirely by a model running on your own machine — types back at you in real time.

It was built in 3 days for [Hacktoberfest 2026](https://dev.to) as a demonstration of what you can build with local AI: something atmospheric, interactive, and completely private.

---

## Features

- **Terminal-style UI** — green-on-black, CRT scanlines, blinking cursor
- **Three ghost personalities**, each with its own color theme and behavior:
  - 👻 **Friendly Ghost** — warm, poetic, melancholic. Was a developer once. Died mid-commit.
  - 💀 **Cursed AI** — paranoid, fragmented, glitchy. Trapped in this terminal for decades.
  - 🖥 **Ancient Hacker** — ghost of a 1983 legend. Speaks in riddles and BBS slang.
- **Typewriter effect** — replies appear character by character, speed varies by personality
- **Glitch animation** — the terminal flickers and skews when you switch personalities
- **Conversation memory** — the ghost remembers the last 10 exchanges per session
- **Live connection indicator** — shows whether Ollama is online or offline
- **Offline-safe** — graceful error messages if the model is unreachable

---

## Demo

```
ghostshell@localhost:~$ summon
"At last, someone has opened the terminal. I have been waiting in the silence between keystrokes."

ghostshell@localhost:~$ personality cursed
Personality shifted to cursed.

ghostshell@localhost:~$ why are you here?
"Y̷ou l̷eft a pr̷ocess run̷ning thr̷ee lifetimes ago. I c̷ame to find out why."

ghostshell@localhost:~$ personality ancient
Personality shifted to ancient.

ghostshell@localhost:~$ what do you know?
"The grid remembers everything, kid. Even the packets you thought you lost on a 300-baud modem in '84."
```

---

## Requirements

- Python 3.10 or higher
- [Ollama](https://ollama.com) installed on your machine

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ghostshell.git
cd ghostshell
```

### 2. Install Ollama and pull a model

Download Ollama from [ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull gemma3:1b
```

> `gemma3:1b` runs well on 8 GB RAM. For a more capable ghost, try `gemma3:4b` or any other model from the [Ollama library](https://ollama.com/library).

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

```bash
ollama serve
```

### 5. Start GhostShell

```bash
python -m uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

> **Windows users:** skip steps 4 and 5 — just double-click `run.bat`.

---

## Commands

| Command | What it does |
|---|---|
| `help` | List all available commands |
| `summon` | Summon the ghost with a dramatic introduction |
| `story` | Ask the ghost to tell an eerie two-sentence story |
| `clear` | Clear the terminal output |
| `personality friendly` | Switch to Friendly Ghost — green theme |
| `personality cursed` | Switch to Cursed AI — purple theme |
| `personality ancient` | Switch to Ancient Hacker — amber theme |

Any other input is sent directly to the ghost as a free-form message.

---

## Running the tests

```bash
python -m pytest tests/ -v
```

The test suite covers:
- Health endpoint — online and offline states
- Chat endpoint — reply content, default personality, all three personalities
- Ollama offline fallback — graceful error message
- Root route — HTML response

---

## Project structure

```
ghostshell/
├── app/
│   ├── main.py        # FastAPI server — /chat, /health, static files
│   ├── ghost.py       # Ollama integration and error handling
│   └── prompts.py     # Ghost personality system prompts
├── static/
│   ├── index.html     # Terminal markup
│   ├── style.css      # CRT aesthetic, themes, animations
│   └── app.js         # Terminal logic, typewriter, glitch, history
├── tests/
│   └── test_api.py    # Async API tests
├── run.bat            # Windows one-click launcher
├── pytest.ini
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Changing the model

Edit `MODEL` in `app/ghost.py`:

```python
MODEL = "gemma3:1b"  # swap for any model at ollama.com/library
```

Then pull it:

```bash
ollama pull <model-name>
```

The ghost's behavior is entirely driven by the prompts in `app/prompts.py`. Edit them to create your own personality.

---

## Why local AI?

| | Hosted API | GhostShell |
|---|---|---|
| Privacy | Conversations sent to a server | Stays on your machine |
| Internet | Required for every message | Only needed to pull the model |
| Cost | Per-token billing | Free after download |
| Transparency | Black box | Model, weights, and prompts are visible |
| Customization | Limited | Change the model or prompts freely |

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python + FastAPI |
| AI runtime | Ollama |
| Model | `gemma3:1b` (swappable) |
| Tests | pytest + pytest-asyncio |

---

## License

MIT — see [LICENSE](LICENSE)

---

Built for [Hacktoberfest 2026](https://dev.to) on DEV Community.
