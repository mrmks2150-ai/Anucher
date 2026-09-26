from duckduckgo_search import DDGS


def search_web(query, max_results=4):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception:
        return []


def format_results(results):
    if not results:
        return ""
    text = ""
    for i, r in enumerate(results, 1):
        text += f"{i}. {r.get('title', '')}\n{r.get('body', '')}\n\n"
    return text.strip()


def needs_web_search(query):
    keywords = [
        "latest", "news", "current", "today", "aaj", "abhi", "2025", "2026",
        "price", "weather", "score", "who won", "kaun jita", "kab hoga",
    ]
    q = query.lower()
    return any(k in q for k in keywords)
