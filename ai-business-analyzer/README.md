# AI Business Analyzer

An AI-powered business analytics prototype that:

- Takes a website URL (or text description)
- Scrapes and parses content
- Uses an LLM (OpenAI or local Ollama) to generate insights
- Renders a simple dashboard with structured results

## Features

- Web scraping with requests + BeautifulSoup
- LLM provider abstraction:
  - OpenAI via `OPENAI_API_KEY`
  - Ollama (e.g., `llama3.1:8b`) via local server
  - Heuristic fallback when no model is configured
- FastAPI + Jinja2 UI
- Simple chart via Chart.js

## Quickstart (Windows PowerShell)

### 1) Clone / enter project
Ensure you're in the project folder:

```powershell
cd d:\Users\Public\business-analyze\ai-business-analyzer
```

### 2) Create and activate a virtual environment (optional but recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```powershell
pip install -r requirements.txt
```

### 4) Configure an LLM (optional)
- OpenAI: create a `.env` file and add your key:

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

- Ollama: install and run Ollama, pull a model (e.g., `ollama pull llama3.1:8b`). Optionally set:

```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

If neither is configured, the app uses a heuristic fallback.

### 5) Run the server

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open http://127.0.0.1:8000 in your browser.

## Project Structure

```
ai-business-analyzer/
  app/
    main.py          # FastAPI app
    scraper.py       # Scrape and parse content
    analyzer.py      # LLM/heuristic analysis
    models.py        # Pydantic models
    templates/
      index.html     # UI
    static/
      style.css      # Styling
  requirements.txt
  README.md
```

## Notes
- Respect target website terms and robots.txt (this prototype fetches small content only).
- Add your own sentiment/competitor APIs for Phase 3.
- Production hardening: logging, retries, caching, rate limiting, tests.
