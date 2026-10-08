"""Synthetic lexical retrieval. No embeddings or remote provider calls."""
import json
import re
from pathlib import Path


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Adapted from the private ERP source; validate bounds and guarantee progress."""
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Require size > overlap >= 0")
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            for sep in ("\n\n", "\n", ". ", " "):
                pos = text.rfind(sep, start, end)
                if pos > start + overlap:
                    end = pos + len(sep)
                    break
        part = text[start:end].strip()
        if part:
            chunks.append(part)
        if end == len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks


class SyntheticRetriever:
    def __init__(self):
        self.documents = json.loads((Path(__file__).parents[1] / "demo/knowledge.json").read_text())

    def search(self, query: str, tenant: str, module: str) -> list[dict]:
        words = {w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 3 and w not in {"demo", "this", "that", "with", "from", "your", "handle"}}
        ranked = []
        for doc in self.documents:
            if doc["tenant"] != tenant or doc["module"] != module:
                continue
            terms = set(re.findall(r"[a-z0-9]+", (doc["title"] + " " + doc["text"]).lower()))
            hits = len(words & terms)
            if hits:
                ranked.append((hits, doc))
        return [dict(doc) for _, doc in sorted(ranked, key=lambda pair: (-pair[0], pair[1]["id"]))[:2]]
