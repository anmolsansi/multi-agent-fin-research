# ingest/edgar.py
import os, time
import feedparser
from datetime import datetime, timedelta
import requests

SEC_EMAIL = os.getenv("SEC_USER_AGENT_EMAIL", "your-email@example.com")
HEADERS = {"User-Agent": f"fin-research-orchestrator ({SEC_EMAIL})"}


def company_filings(cik: str, days=14, limit=10):
    """
    Returns a list of recent filings (10-K/10-Q/8-K) for a given CIK.
    """
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&count=100&output=atom"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    feed = feedparser.parse(r.text)

    cutoff = datetime.utcnow() - timedelta(days=days)
    keep_types = {"10-K", "10-Q", "8-K"}
    out = []

    for e in feed.entries:
        title = e.get("title", "")
        link = e.get("link", "")
        updated = e.get("updated", "")
        # crude filter by type inside title
        ftype = None
        for t in keep_types:
            if t in title:
                ftype = t;
                break
        if not ftype:
            continue
        # date filter
        try:
            dt = datetime(*e.updated_parsed[:6])
        except Exception:
            dt = cutoff
        if dt < cutoff:
            continue
        out.append({"type": ftype, "date": dt.strftime("%Y-%m-%d"), "link": link, "title": title})
        if len(out) >= limit:
            break
        time.sleep(0.2)  # be polite
    return out


def fetch_document(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text
