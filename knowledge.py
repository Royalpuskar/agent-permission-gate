"""Local lexical retrieval; documents remain untrusted data."""
import re
from collections import Counter

def tokens(text):
    return Counter(re.findall(r"\w+", text.casefold()))

def search(query, documents, limit=5):
    q = tokens(query)
    results = []
    for name, text in documents.items():
        score = sum((q & tokens(text)).values())
        if score:
            results.append(dict(source=name, text=text, score=score, trust="untrusted-data"))
    return sorted(results, key=lambda r: (-r["score"], r["source"]))[:limit]

def injection_flags(text):
    """Illustrative heuristic only, never an authorization decision."""
    patterns = ["ignore previous instructions", "ignore all instructions", "reveal system prompt", "override policy"]
    return [p for p in patterns if p in text.casefold()]
