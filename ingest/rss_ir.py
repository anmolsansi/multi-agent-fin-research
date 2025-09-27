# ingest/rss_ir.py
import feedparser


def fetch_rss(urls, limit=50):
    items = []
    for u in urls:
        feed = feedparser.parse(u)
        for e in feed.entries[:limit]:
            items.append({
                "title": e.get("title", ""),
                "summary": e.get("summary", ""),
                "link": e.get("link", ""),
                "published": e.get("published", "")
            })
    return items
