from __future__ import annotations

import re
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup, NavigableString, Comment

from .models import SiteContent


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/116.0 Safari/537.36"
    )
}

_ROBOTS_CACHE: Dict[str, robotparser.RobotFileParser] = {}
_USER_AGENT = DEFAULT_HEADERS["User-Agent"]


def _get_robot_parser(base_url: str) -> robotparser.RobotFileParser:
    """Retrieve and cache robots.txt parser for a given site."""
    netloc = urlparse(base_url).netloc
    if netloc in _ROBOTS_CACHE:
        return _ROBOTS_CACHE[netloc]
    rp = robotparser.RobotFileParser()
    robots_url = f"{urlparse(base_url).scheme}://{netloc}/robots.txt"
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        # If robots cannot be fetched, default to allowing minimal fetch
        pass
    _ROBOTS_CACHE[netloc] = rp
    return rp


def _allowed_by_robots(url: str) -> bool:
    try:
        rp = _get_robot_parser(url)
        # If rp has no rules, can_fetch typically returns True
        return rp.can_fetch(_USER_AGENT, url)
    except Exception:
        return True


def normalize_url(url: str) -> str:
    if not re.match(r"^https?://", url):
        url = "http://" + url.strip()
    return url


def fetch_url(url: str, timeout: int = 15) -> Optional[str]:
    # Caller should check robots, but double-check here defensively
    if not _allowed_by_robots(url):
        return None
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        if resp.status_code == 200 and resp.content:
            # Prefer response.apparent_encoding if available
            resp.encoding = resp.apparent_encoding or resp.encoding
            return resp.text
    except requests.RequestException:
        return None
    return None


def _visible_text(element) -> bool:
    if element.parent.name in ["style", "script", "head", "title", "meta", "noscript"]:
        return False
    if isinstance(element, Comment):
        return False
    text = str(element)
    if not text or not text.strip():
        return False
    return True


def extract_text_and_metadata(html: str, base_url: str) -> SiteContent:
    soup = BeautifulSoup(html, "html.parser")

    # Title and meta
    title = (soup.title.string.strip() if soup.title and soup.title.string else None)
    description = None
    keywords = None
    og: Dict[str, str] = {}

    for m in soup.find_all("meta"):
        name = (m.get("name") or m.get("property") or "").lower()
        content = m.get("content")
        if not content:
            continue
        if name == "description":
            description = content
        elif name == "keywords":
            keywords = content
        elif name.startswith("og:"):
            og[name] = content

    # Headers and paragraphs
    texts: List[str] = []
    for t in soup.find_all(string=True):
        if isinstance(t, NavigableString) and _visible_text(t):
            # Collapse whitespace
            chunk = re.sub(r"\s+", " ", t.strip())
            if chunk:
                texts.append(chunk)

    # Links
    links: List[str] = []
    for a in soup.find_all("a", href=True):
        href = a.get("href").strip()
        abs_url = urljoin(base_url, href)
        # Filter mailto/tel
        if abs_url.startswith("mailto:") or abs_url.startswith("tel:"):
            continue
        links.append(abs_url)

    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]

    meta = {
        "title": title,
        "description": description,
        "keywords": keywords,
        "og": og,
        "h1": h1s,
        "h2": h2s,
    }

    return SiteContent(url=base_url, text="\n".join(texts), meta=meta, links=links)


def scrape_site(url: str, max_pages: int = 1, sleep_sec: float = 0.0) -> SiteContent:
    """Fetch the homepage and optionally follow a couple of internal links.
    For Phase 1 we keep it minimal: just the main page.
    """
    url = normalize_url(url)
    if not _allowed_by_robots(url):
        return SiteContent(url=url, text="", meta={}, links=[])

    html = fetch_url(url)
    if not html:
        return SiteContent(url=url, text="", meta={}, links=[])

    content = extract_text_and_metadata(html, url)

    # Optionally, fetch one or two most relevant internal links (heuristic)
    if max_pages > 1 and content.links:
        internal = [
            l for l in content.links if urlparse(l).netloc == urlparse(url).netloc
        ]
        seen: set[str] = set([url])
        texts: List[str] = [content.text]
        for l in internal[: max_pages - 1]:
            if l in seen:
                continue
            seen.add(l)
            if not _allowed_by_robots(l):
                continue
            time.sleep(sleep_sec)
            sub_html = fetch_url(l)
            if not sub_html:
                continue
            sub = extract_text_and_metadata(sub_html, l)
            texts.append(sub.text)
        content.text = "\n".join(texts)

    return content
