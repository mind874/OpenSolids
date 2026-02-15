from __future__ import annotations


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def matches_query(query: str, *fields: str | None) -> bool:
    q = normalize_text(query)
    if not q:
        return False
    for field in fields:
        if field and q in normalize_text(field):
            return True
    return False
