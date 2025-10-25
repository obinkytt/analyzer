from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time

from .analyzer import analyze_site, analyze_text

# App configuration
app = FastAPI(
    title="AI Business Analyzer", 
    version="1.0.0",
    description="Comprehensive business analysis and insights platform",
    docs_url="/api/docs" if os.getenv("DEBUG", "False").lower() == "true" else None,
    redoc_url="/api/redoc" if os.getenv("DEBUG", "False").lower() == "true" else None
)

# Security middleware
allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")
if allowed_hosts != ["*"]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rate limiting simple implementation
request_times = {}

def simple_rate_limit(request: Request) -> bool:
    """Simple rate limiting: max 10 requests per minute per IP"""
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in request_times:
        request_times[client_ip] = []
    
    # Clean old requests (older than 1 minute)
    request_times[client_ip] = [t for t in request_times[client_ip] if current_time - t < 60]
    
    # Check if limit exceeded
    if len(request_times[client_ip]) >= 10:
        return False
    
    # Add current request
    request_times[client_ip].append(current_time)
    return True

base_dir = os.path.dirname(__file__)
static_dir = os.path.join(base_dir, "static")
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "error": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, url: Optional[str] = Form(default=""), description: Optional[str] = Form(default="")):
    # Rate limiting
    if not simple_rate_limit(request):
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "result": None, "error": "Rate limit exceeded. Please wait a minute before trying again."}
        )
    
    url = (url or "").strip()
    description = (description or "").strip()

    if not url and not description:
        return templates.TemplateResponse(
            "index.html", {"request": request, "result": None, "error": "Please provide a URL or a description."}
        )

    try:
        if url:
            # Validate URL format
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("www.")):
                url = "https://" + url
            result = analyze_site(url)
        else:
            result = analyze_text(description, meta={})

        return templates.TemplateResponse("index.html", {"request": request, "result": result, "error": None})
    except Exception as e:
        error_message = f"Failed to analyze: {str(e)}"
        if "timeout" in str(e).lower():
            error_message = "Analysis timed out. Please try again with a simpler request."
        elif "connection" in str(e).lower():
            error_message = "Unable to connect to the website. Please check the URL and try again."
        
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": None, "error": error_message},
        )


# Health endpoint for monitoring
@app.get("/health")
async def health():
    return {"status": "ok", "service": "AI Business Analyzer", "version": "1.0.0"}


# API endpoints for programmatic access
@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "timestamp": time.time()}


# About page
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
